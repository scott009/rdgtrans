#!/usr/bin/env python3
"""
Fix HTML hierarchy in rdgBook2.html:
1. Change first h2 "RECOVERY DHARMA" to h1
2. Remove <h3 class="id-tag">PARAGRAPH_ID</h3> and add id to following <p> tag
"""

import re
import sys

def fix_hierarchy(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Change first <h2 class="chaptermain">RECOVERY DHARMA</h2> to <h1>
    content = content.replace(
        '<h2 class="chaptermain">RECOVERY DHARMA</h2>',
        '<h1 class="chaptermain">RECOVERY DHARMA</h1>',
        1  # Only replace first occurrence
    )

    # Step 2: Transform <h3 class="id-tag">PARAGRAPH_ID</h3>\n<p> to <p id="PARAGRAPH_ID">
    # Pattern: <h3 class="id-tag">pX-Y</h3> followed by newline and <p (with optional attributes)
    pattern = r'<h3 class="id-tag">([^<]+)</h3>\s*\n\s*<p((?:\s+[^>]*)?)>'
    replacement = r'<p id="\1"\2>'

    content = re.sub(pattern, replacement, content)

    # Write the fixed content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Fixed HTML hierarchy")
    print(f"✓ Changed first RECOVERY DHARMA to <h1>")
    print(f"✓ Removed <h3 class='id-tag'> elements and added id attributes to paragraphs")

if __name__ == '__main__':
    input_file = '/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/rdgBook2.html'
    output_file = input_file  # Overwrite the same file

    fix_hierarchy(input_file, output_file)
