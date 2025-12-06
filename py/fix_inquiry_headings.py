#!/usr/bin/env python3
"""
Fix inquiry headings in rdgBook2.html:
Transform <p class="inquiryheading"> to <h4 class="inquiryheading">
"""

import re

def fix_inquiry_headings(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Transform <p class="inquiryheading">TEXT</p> to <h4 class="inquiryheading">TEXT</h4>
    content = content.replace(
        '<p class="inquiryheading">',
        '<h4 class="inquiryheading">'
    )
    content = content.replace(
        '</p>',
        '</h4>'
    )

    # Wait, this will replace ALL </p> tags. Let me use a better approach with regex
    # Revert and use proper regex

    # Reload the file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern: <p class="inquiryheading">CONTENT</p>
    pattern = r'<p class="inquiryheading">([^<]+)</p>'
    replacement = r'<h4 class="inquiryheading">\1</h4>'

    content = re.sub(pattern, replacement, content)

    # Write the fixed content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Fixed inquiry headings")
    print(f"✓ Transformed <p class='inquiryheading'> to <h4 class='inquiryheading'>")

if __name__ == '__main__':
    input_file = '/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/rdgBook2.html'
    output_file = input_file  # Overwrite the same file

    fix_inquiry_headings(input_file, output_file)
