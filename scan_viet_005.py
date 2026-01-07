#!/usr/bin/env python3
"""
SCAN-VIET-005: Structural integrity scan of Vietnamese tmaster HTML.
Uses jmaster (workmaster.json) as structural authority.
Produces SCAN-VIET-005_jmaster_structure_report.json.
NO edits to source files.
"""

import json
import re
from collections import defaultdict, Counter

# File paths
TARGET_HTML = "/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/tmasterVietnamese.html"
JMASTER_JSON = "/home/scott/gitrepos/rdgtrans/workmaster.json"
OUTPUT_JSON = "/home/scott/gitrepos/rdgtrans/SCAN-VIET-005_jmaster_structure_report.json"

def load_jmaster_expected_ids(jmaster_path):
    """Load jmaster and extract all structurally expected paragraph IDs."""
    with open(jmaster_path, 'r', encoding='utf-8') as f:
        jmaster = json.load(f)

    expected_ids = []
    chapters = jmaster.get('chapters', [])

    for chapter in chapters:
        # Add chapter ID if present
        chapter_id = chapter.get('id')
        if chapter_id:
            expected_ids.append(chapter_id)

        # Add paragraph IDs from content in order
        content = chapter.get('content', [])
        for item in content:
            para_id = item.get('id')
            if para_id:
                expected_ids.append(para_id)

    return expected_ids

def extract_paragraph_ids_from_html(html_path):
    """Extract all data-id values from paragraph-block divs in order."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Find all paragraph blocks with data-id
    pattern = r'<div[^>]+class="paragraph-block"[^>]+data-id="([^"]+)"'
    matches = re.findall(pattern, html_content)

    return matches

def classify_structural_status(para_id, expected_set, html_id_counts, unexpected_ids):
    """
    Classify structural status of a paragraph ID.

    Returns:
        present_once: ID is expected and appears exactly once
        missing: ID is expected but not in HTML
        duplicate: ID is expected and appears multiple times
        unexpected: ID is in HTML but not expected by jmaster
    """
    if para_id in expected_set:
        count = html_id_counts.get(para_id, 0)
        if count == 0:
            return 'missing'
        elif count == 1:
            return 'present_once'
        else:
            return 'duplicate'
    elif para_id in unexpected_ids:
        return 'unexpected'
    else:
        return 'unexpected'

def main():
    print("SCAN-VIET-005: Starting structural integrity scan")
    print("=" * 60)

    # Load structural authority (jmaster)
    print(f"Loading jmaster: {JMASTER_JSON}")
    expected_ids = load_jmaster_expected_ids(JMASTER_JSON)
    expected_set = set(expected_ids)
    print(f"  Found {len(expected_ids)} structurally expected paragraph IDs")
    print(f"  ({len(expected_set)} unique IDs)")

    # Extract paragraph IDs from target HTML
    print(f"Scanning target HTML: {TARGET_HTML}")
    html_ids = extract_paragraph_ids_from_html(TARGET_HTML)
    print(f"  Found {len(html_ids)} paragraph blocks")

    # Count occurrences of each ID in HTML
    html_id_counts = Counter(html_ids)
    html_set = set(html_ids)

    # Find unexpected IDs (in HTML but not in jmaster)
    unexpected_ids = html_set - expected_set

    print(f"\nStructural analysis:")
    print(f"  Expected IDs: {len(expected_set)}")
    print(f"  Found in HTML: {len(html_set)}")
    print(f"  Unexpected IDs: {len(unexpected_ids)}")

    # Build by_paragraph list for all expected IDs
    by_paragraph = []
    counts = defaultdict(int)

    # Process all expected IDs
    for para_id in expected_ids:
        status = classify_structural_status(para_id, expected_set, html_id_counts, unexpected_ids)
        by_paragraph.append({
            "paragraph_id": para_id,
            "structural_status": status
        })
        counts[status] += 1

    # Process unexpected IDs found in HTML
    for para_id in unexpected_ids:
        status = 'unexpected'
        by_paragraph.append({
            "paragraph_id": para_id,
            "structural_status": status
        })
        counts[status] += 1

    # Build summary
    summary = {
        "expected_total": len(expected_ids),
        "present_once": counts['present_once'],
        "missing": counts['missing'],
        "duplicate": counts['duplicate'],
        "unexpected": counts['unexpected']
    }

    # Build report
    report = {
        "run_id": "SCAN-VIET-005",
        "target_file": TARGET_HTML,
        "authority_file": JMASTER_JSON,
        "summary": summary,
        "by_paragraph": by_paragraph
    }

    # Write report
    print(f"\nWriting report: {OUTPUT_JSON}")
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Print summary
    print("\n" + "=" * 60)
    print("SCAN-VIET-005 Summary:")
    print("=" * 60)
    print(json.dumps(summary, indent=2))
    print("=" * 60)
    print(f"\nReport written to: {OUTPUT_JSON}")
    print("Scan complete. No files were modified.")

if __name__ == "__main__":
    main()
