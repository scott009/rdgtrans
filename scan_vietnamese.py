#!/usr/bin/env python3
"""
SCAN-VIET-003: Vietnamese target vs presauth consistency scan
READ-ONLY | DETECTION-ONLY | NO MODIFICATIONS
"""

import json
import re
from pathlib import Path
from html.parser import HTMLParser
from typing import List, Dict, Any

# Bound inputs from manifest
TARGET = "/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/tmasterVietnamese.html"
PRESAUTH = "/mnt/c/Users/scott/Documents/AIProjects/Markdown/RDGTranslations/supervisor_updates/pres_tmaster_viet.json"
RUN_ID = "SCAN-VIET-003"

class ParagraphExtractor(HTMLParser):
    """Extract paragraphs with data-pr-id attributes from HTML"""
    def __init__(self):
        super().__init__()
        self.paragraphs = []
        self.current_pr_id = None
        self.current_content = []
        self.in_paragraph = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if 'data-pr-id' in attrs_dict:
            self.current_pr_id = attrs_dict['data-pr-id']
            self.current_content = []
            self.in_paragraph = True

    def handle_endtag(self, tag):
        if self.in_paragraph and self.current_pr_id:
            content = ''.join(self.current_content).strip()
            self.paragraphs.append({
                'pr_id': self.current_pr_id,
                'content': content,
                'tag': tag
            })
            self.current_pr_id = None
            self.current_content = []
            self.in_paragraph = False

    def handle_data(self, data):
        if self.in_paragraph:
            self.current_content.append(data)

def normalize_text(text: str) -> str:
    """Basic normalization for comparison"""
    return ' '.join(text.split()).strip()

def scan_document():
    """Execute linear scan per instruction block"""

    print(f"=== {RUN_ID} SCAN START ===\n")

    # Load presauth
    print("Loading presauth...")
    try:
        with open(PRESAUTH, 'r', encoding='utf-8') as f:
            presauth_data = json.load(f)
    except Exception as e:
        print(f"FATAL: Cannot load presauth: {e}")
        return

    # Build presauth lookup
    presauth_lookup = {}
    if isinstance(presauth_data, dict):
        # Check for content_volatile.entries structure
        if 'content_volatile' in presauth_data and 'entries' in presauth_data['content_volatile']:
            for p in presauth_data['content_volatile']['entries']:
                if 'paragraph_id' in p:
                    presauth_lookup[p['paragraph_id']] = p
        # Fallback to direct paragraphs array
        elif 'paragraphs' in presauth_data:
            for p in presauth_data['paragraphs']:
                if 'pr_id' in p:
                    presauth_lookup[p['pr_id']] = p

    print(f"Presauth loaded: {len(presauth_lookup)} paragraphs indexed\n")

    # Load and parse target HTML
    print("Loading target HTML...")
    try:
        with open(TARGET, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"FATAL: Cannot load target: {e}")
        return

    parser = ParagraphExtractor()
    parser.feed(html_content)
    target_paragraphs = parser.paragraphs

    print(f"Target loaded: {len(target_paragraphs)} paragraphs found\n")

    # Scan results
    results = []
    classifications = {
        'MATCH': 0,
        'MISSING_IN_PRESAUTH': 0,
        'CONTENT_MISMATCH': 0,
        'STRUCTURAL_MISMATCH': 0
    }

    print("=== LINEAR SCAN BEGIN ===\n")

    # Linear scan through target
    for idx, para in enumerate(target_paragraphs, 1):
        pr_id = para['pr_id']
        target_content = normalize_text(para['content'])

        # Classify
        if pr_id not in presauth_lookup:
            classification = 'MISSING_IN_PRESAUTH'
            note = f"pr_id '{pr_id}' not found in presauth"
        else:
            presauth_para = presauth_lookup[pr_id]
            # Try different content field names
            presauth_content = normalize_text(
                presauth_para.get('vietnamese_text', '') or
                presauth_para.get('vi', '')
            )

            if target_content == presauth_content:
                classification = 'MATCH'
                note = "content matches"
            else:
                classification = 'CONTENT_MISMATCH'
                note = f"content differs (target:{len(target_content)} chars, presauth:{len(presauth_content)} chars)"

        classifications[classification] += 1

        results.append({
            'ordinal': idx,
            'pr_id': pr_id,
            'classification': classification,
            'note': note
        })

    # Check for paragraphs in presauth but not in target
    target_pr_ids = {p['pr_id'] for p in target_paragraphs}
    missing_in_target = []
    for pr_id in presauth_lookup:
        if pr_id not in target_pr_ids:
            missing_in_target.append({
                'pr_id': pr_id,
                'classification': 'MISSING_IN_TARGET',
                'note': f"pr_id '{pr_id}' in presauth but not in target"
            })

    classifications['MISSING_IN_TARGET'] = len(missing_in_target)

    print("=== LINEAR SCAN COMPLETE ===\n")

    # Write scan report (machine-readable)
    report_file = f"/home/scott/gitrepos/rdgtrans/{RUN_ID}_scan_report.json"
    report_data = {
        'run_id': RUN_ID,
        'target': TARGET,
        'presauth': PRESAUTH,
        'scan_results': results,
        'missing_in_target': missing_in_target,
        'summary': {
            'total_paragraphs_scanned': len(target_paragraphs),
            'classifications': classifications
        }
    }

    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    print(f"Scan report written: {report_file}\n")

    # Write summary note
    summary_file = f"/home/scott/gitrepos/rdgtrans/{RUN_ID}_summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"=== {RUN_ID} SUMMARY ===\n\n")
        f.write(f"Target: {TARGET}\n")
        f.write(f"Presauth: {PRESAUTH}\n\n")
        f.write(f"Total paragraphs scanned: {len(target_paragraphs)}\n\n")
        f.write("Classifications:\n")
        for cls, count in sorted(classifications.items()):
            f.write(f"  {cls}: {count}\n")
        f.write("\n")
        f.write("Notable patterns:\n")

        match_rate = (classifications['MATCH'] / len(target_paragraphs) * 100) if target_paragraphs else 0
        f.write(f"  - Match rate: {match_rate:.1f}%\n")

        if classifications['MISSING_IN_PRESAUTH'] > 0:
            f.write(f"  - {classifications['MISSING_IN_PRESAUTH']} paragraphs in target not found in presauth\n")

        if classifications['MISSING_IN_TARGET'] > 0:
            f.write(f"  - {classifications['MISSING_IN_TARGET']} paragraphs in presauth not found in target\n")

        if classifications['CONTENT_MISMATCH'] > 0:
            f.write(f"  - {classifications['CONTENT_MISMATCH']} paragraphs have content discrepancies\n")

        f.write("\nNo files were modified.\n")
        f.write("No unbound sources were consulted.\n")

    print(f"Summary written: {summary_file}\n")

    # Console output
    print("=== SUMMARY ===")
    print(f"Total paragraphs scanned: {len(target_paragraphs)}")
    print("\nClassifications:")
    for cls, count in sorted(classifications.items()):
        print(f"  {cls}: {count}")
    print(f"\nMatch rate: {match_rate:.1f}%")
    print(f"\nOutputs:")
    print(f"  {report_file}")
    print(f"  {summary_file}")
    print(f"\n=== {RUN_ID} COMPLETE ===")

if __name__ == '__main__':
    scan_document()
