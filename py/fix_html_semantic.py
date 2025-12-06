#!/usr/bin/env python3
"""
Fix HTML semantic structure for RDG language files:
1. Change first h2 chapter to h1
2. Remove <h3 class="id-tag">PARAGRAPH_ID</h3> and add id to following <p> tag
3. Transform <p class="inquiryheading"> to <h4 class="inquiryheading">
"""

import re
import sys

def fix_html_semantic(input_file, output_file, first_h2_text):
    """
    Fix HTML semantic structure.

    Args:
        input_file: Path to input HTML file
        output_file: Path to output HTML file
        first_h2_text: Text content of first H2 to convert to H1 (for language matching)
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Change first matching <h2 class="chaptermain"> to <h1>
    # For Thai, match any h2 with class="chaptermain" that appears first
    pattern_h1 = r'<h2 class="chaptermain"([^>]*)>([^<]+)</h2>'

    def replace_first_h2(match):
        # Only replace the first occurrence
        if not hasattr(replace_first_h2, 'replaced'):
            replace_first_h2.replaced = True
            return f'<h1 class="chaptermain"{match.group(1)}>{match.group(2)}</h1>'
        return match.group(0)

    content = re.sub(pattern_h1, replace_first_h2, content)

    # Step 2: Transform <h3 class="id-tag">pX-Y</h3> followed by <p> to <p id="pX-Y">
    pattern_id = r'<h3 class="id-tag">([^<]+)</h3>\s*\n\s*<p((?:\s+[^>]*)?)>'
    replacement_id = r'<p id="\1"\2>'
    content = re.sub(pattern_id, replacement_id, content)

    # Step 3: Transform <p ...class="inquiryheading"...>TEXT</p> to <h4 ...class="inquiryheading"...>TEXT</h4>
    # Match <p> tags with class="inquiryheading" (with any other attributes)
    pattern_inquiry = r'<p([^>]*class="inquiryheading"[^>]*)>([^<]+)</p>'
    replacement_inquiry = r'<h4\1>\2</h4>'
    content = re.sub(pattern_inquiry, replacement_inquiry, content)

    # Write the fixed content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Fixed HTML semantic structure")
    print(f"✓ Changed first chapter to <h1>")
    print(f"✓ Removed <h3 class='id-tag'> elements and added id attributes to paragraphs")
    print(f"✓ Transformed inquiry headings to <h4>")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 fix_html_semantic.py <input_file> [output_file]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file

    fix_html_semantic(input_file, output_file, first_h2_text=None)
