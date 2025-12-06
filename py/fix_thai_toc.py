#!/usr/bin/env python3
"""
Fix Thai TOC - convert <p class="TOCentry"> to <a href="#id" class="TOCentry">
"""

import re

def fix_toc(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern: <p id="pX-Y" class="TOCentry">TEXT</p>
    # Replace with: <a href="#TEXT" class="TOCentry">TEXT</a>
    # The href should match the chapter id

    def replace_toc_entry(match):
        text = match.group(1)
        # Remove trailing colons and whitespace for the ID
        # Chapter IDs might have slight variations
        return f'<a href="#{text}" class="TOCentry">{text}</a>'

    # Match TOC entries
    pattern = r'<p id="p\d+-\d+" class="TOCentry">([^<]+)</p>'
    content = re.sub(pattern, replace_toc_entry, content)

    # Also fix tocsection entries
    pattern_section = r'<p id="p\d+-\d+" class="tocsection">([^<]+)</p>'
    content = re.sub(pattern_section, lambda m: f'<p class="tocsection">{m.group(1)}</p>', content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Fixed TOC links")
    print(f"✓ Converted <p class='TOCentry'> to <a href='#id' class='TOCentry'>")

if __name__ == '__main__':
    input_file = '/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/rdgThai2.html'
    output_file = input_file

    fix_toc(input_file, output_file)
