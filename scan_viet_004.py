#!/usr/bin/env python3
"""
SCAN-VIET-004: Scan-only classification of Vietnamese tmaster paragraphs.
Produces SCAN-VIET-004_scan_report.json with authority classification.
NO edits to source files.
"""

import json
import re
from pathlib import Path
from collections import defaultdict

# File paths
TARGET_HTML = "/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/tmasterVietnamese.html"
PRESAUTH_JSON = "/mnt/c/Users/scott/Documents/AIProjects/Markdown/RDGTranslations/supervisor_updates/pres_tmaster_viet.json"
JMASTER_JSON = "/home/scott/gitrepos/rdgtrans/workmaster.json"
OUTPUT_JSON = "/home/scott/gitrepos/rdgtrans/SCAN-VIET-004_scan_report.json"

def load_presauth_ids(presauth_path):
    """Load presauth and extract all paragraph_ids."""
    with open(presauth_path, 'r', encoding='utf-8') as f:
        presauth = json.load(f)

    ids = set()
    entries = presauth.get('content_volatile', {}).get('entries', [])
    for entry in entries:
        para_id = entry.get('paragraph_id')
        if para_id:
            ids.add(para_id)

    return ids

def load_jmaster_ids(jmaster_path):
    """Load jmaster (workmaster.json) and extract all paragraph IDs."""
    with open(jmaster_path, 'r', encoding='utf-8') as f:
        jmaster = json.load(f)

    ids = set()
    chapters = jmaster.get('chapters', [])
    for chapter in chapters:
        # Add chapter ID if present
        chapter_id = chapter.get('id')
        if chapter_id:
            ids.add(chapter_id)

        # Add paragraph IDs from content
        content = chapter.get('content', [])
        for item in content:
            para_id = item.get('id')
            if para_id:
                ids.add(para_id)

    return ids

def extract_paragraph_ids_from_html(html_path):
    """Extract all data-id values from paragraph-block divs in order."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Find all paragraph blocks with data-id
    pattern = r'<div[^>]+class="paragraph-block"[^>]+data-id="([^"]+)"'
    matches = re.findall(pattern, html_content)

    return matches

def classify_paragraph(para_id, presauth_ids, jmaster_ids):
    """
    Classify a paragraph ID based on authority sources.

    Priority:
    1. If in presauth -> 'presauth'
    2. Else if in jmaster -> 'jmaster'
    3. Else if matches known out-of-scope pattern -> 'out_of_scope'
    4. Else -> 'unaccounted'
    """
    # Exact match in presauth
    if para_id in presauth_ids:
        return 'presauth'

    # Exact match in jmaster
    if para_id in jmaster_ids:
        return 'jmaster'

    # Out of scope patterns (reviewer sections, UI elements, etc.)
    out_of_scope_patterns = [
        'reviewer-', 'footer-', 'header-', 'nav-',
        'btn-', 'modal-', 'form-', 'input-'
    ]
    for pattern in out_of_scope_patterns:
        if para_id.startswith(pattern):
            return 'out_of_scope'

    # Unaccounted
    return 'unaccounted'

def main():
    print("SCAN-VIET-004: Starting scan-only classification")
    print("=" * 60)

    # Load authority sources
    print(f"Loading presauth: {PRESAUTH_JSON}")
    presauth_ids = load_presauth_ids(PRESAUTH_JSON)
    print(f"  Found {len(presauth_ids)} paragraph IDs in presauth")

    print(f"Loading jmaster: {JMASTER_JSON}")
    jmaster_ids = load_jmaster_ids(JMASTER_JSON)
    print(f"  Found {len(jmaster_ids)} paragraph IDs in jmaster")

    # Extract paragraph IDs from target HTML
    print(f"Scanning target HTML: {TARGET_HTML}")
    paragraph_ids = extract_paragraph_ids_from_html(TARGET_HTML)
    print(f"  Found {len(paragraph_ids)} paragraph blocks")

    # Classify each paragraph
    print("\nClassifying paragraphs...")
    by_paragraph = []
    counts = defaultdict(int)

    for para_id in paragraph_ids:
        authority = classify_paragraph(para_id, presauth_ids, jmaster_ids)
        by_paragraph.append({
            "paragraph_id": para_id,
            "authority": authority
        })
        counts[authority] += 1

    # Build summary
    summary = {
        "total": len(paragraph_ids),
        "presauth_covered": counts['presauth'],
        "jmaster_covered": counts['jmaster'],
        "out_of_scope": counts['out_of_scope'],
        "unaccounted": counts['unaccounted']
    }

    # Build report
    report = {
        "run_id": "SCAN-VIET-004",
        "target_file": TARGET_HTML,
        "authority_files": {
            "presauth": PRESAUTH_JSON,
            "jmaster": JMASTER_JSON
        },
        "summary": summary,
        "by_paragraph": by_paragraph
    }

    # Write report
    print(f"\nWriting report: {OUTPUT_JSON}")
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Print summary
    print("\n" + "=" * 60)
    print("SCAN-VIET-004 Summary:")
    print("=" * 60)
    print(json.dumps(summary, indent=2))
    print("=" * 60)
    print(f"\nReport written to: {OUTPUT_JSON}")
    print("Scan complete. No files were modified.")

if __name__ == "__main__":
    main()
