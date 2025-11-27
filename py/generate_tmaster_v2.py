#!/usr/bin/env python3
"""
Generate Translation Master HTML v2
Uses workmaster.json as structural guide + markdown source files for content
"""

import re
import json
from datetime import datetime
import html as html_module

def extract_paragraphs_from_markdown(md_file):
    """Extract paragraphs by ID from markdown file"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    paragraphs = {}

    # Pattern: ### ID: pX-Y followed by paragraph text
    # The text continues until the next ### or ##
    pattern = r'### ID: (p[\d\.-]+)\s*\n((?:(?!###|##).)*?)(?=###|##|$)'

    for match in re.finditer(pattern, content, re.DOTALL):
        pid = match.group(1)
        text = match.group(2).strip()
        # Clean up extra whitespace
        text = ' '.join(text.split())
        paragraphs[pid] = text

    return paragraphs

def extract_chapter_titles_from_markdown(md_file):
    """Extract chapter titles from markdown file"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    titles = {}

    # Pattern: ## Chapter X: TITLE (where X can be integer or decimal like 16.1)
    pattern = r'## Chapter ([\d\.]+): (.+?)$'

    for match in re.finditer(pattern, content, re.MULTILINE):
        chapter_num_str = match.group(1)
        title = match.group(2).strip()

        # Convert to int if it's a whole number, otherwise keep as string
        if '.' in chapter_num_str:
            chapter_num = chapter_num_str  # Keep as string "16.1"
        else:
            chapter_num = int(chapter_num_str)  # Convert to int 16

        titles[chapter_num] = title

    return titles

def generate_tmaster_v2(workmaster_json, english_md, thai_md, output_file, language_name="Thai"):
    """Generate translation master using workmaster.json structure"""

    print(f"Reading {workmaster_json}...")
    with open(workmaster_json, 'r', encoding='utf-8') as f:
        workmaster = json.load(f)

    print(f"Reading {english_md}...")
    english_paragraphs = extract_paragraphs_from_markdown(english_md)
    english_titles = extract_chapter_titles_from_markdown(english_md)
    print(f"  Found {len(english_paragraphs)} English paragraphs")
    print(f"  Found {len(english_titles)} English chapter titles")

    print(f"Reading {thai_md}...")
    thai_paragraphs = extract_paragraphs_from_markdown(thai_md)
    thai_titles = extract_chapter_titles_from_markdown(thai_md)
    print(f"  Found {len(thai_paragraphs)} Thai paragraphs")
    print(f"  Found {len(thai_titles)} Thai chapter titles")

    # Build content list from workmaster structure
    content_items = []

    for chapter in workmaster['chapters']:
        chapter_num = chapter.get('chapter_number')
        chapter_title_en = chapter.get('chapter_title', '')

        # Skip chapter 1 (front matter) if it has no useful content
        if chapter_num == 1:
            continue

        # Normalize chapter_num for dictionary lookup (handle both int and str types)
        # workmaster.json has some chapters as strings, but title dicts use int keys
        try:
            ch_num_for_lookup = int(float(str(chapter_num))) if '.' not in str(chapter_num) else chapter_num
        except (ValueError, TypeError):
            ch_num_for_lookup = chapter_num

        # Get chapter titles
        title_en = english_titles.get(ch_num_for_lookup, chapter_title_en)
        title_th = thai_titles.get(ch_num_for_lookup, '')

        # Add chapter heading
        if title_en or title_th:
            content_items.append({
                'type': 'heading',
                'chapter_num': chapter_num,
                'id': f'chapter-{chapter_num}',
                'english_text': title_en,
                'thai_text': title_th
            })

        # Add paragraphs from this chapter
        if 'content' in chapter:
            for item in chapter['content']:
                if item.get('type') == 'paragraph':
                    pid = item.get('id')
                    if pid:
                        text_en = english_paragraphs.get(pid, '')
                        text_th = thai_paragraphs.get(pid, '')

                        # Only include if we have both English and Thai text
                        if text_en and text_th:
                            content_items.append({
                                'type': 'paragraph',
                                'chapter_num': chapter_num,
                                'id': pid,
                                'english_text': text_en,
                                'thai_text': text_th
                            })

    print(f"\n✓ Built content structure:")
    headings_count = sum(1 for item in content_items if item['type'] == 'heading')
    paragraphs_count = sum(1 for item in content_items if item['type'] == 'paragraph')
    print(f"  {headings_count} chapter headings")
    print(f"  {paragraphs_count} paragraphs")
    print(f"  {len(content_items)} total items")

    # Generate HTML
    html = f'''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{language_name} Translation Master - Correction Tool</title>
    <link rel="stylesheet" href="ada3.css">
    <style>
        body {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            font-family: Arial, sans-serif;
        }}

        header {{
            background: #2c5282;
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}

        header h1 {{
            margin: 0 0 15px 0;
        }}

        .reviewer-section {{
            background: #90cdf4;
            background: linear-gradient(135deg, #90cdf4 0%, #63b3ed 100%);
            color: #1a365d;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 2px solid #2c5282;
        }}

        .reviewer-section h2 {{
            margin: 0 0 10px 0;
            font-size: 1.3em;
            border-bottom: 2px solid #2c5282;
            padding-bottom: 10px;
            color: #1a365d;
        }}

        .reviewer-section p {{
            margin: 0 0 20px 0;
            color: #2d3748;
        }}

        .editor-info {{
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }}

        .editor-info input {{
            flex: 1;
            padding: 10px;
            border-radius: 4px;
            border: 2px solid #2c5282;
            background: white;
            font-size: 15px;
        }}

        .editor-info input:required {{
            border-left: 4px solid #2c5282;
        }}

        .editor-info input:focus {{
            outline: none;
            border-color: #2c5282;
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
        }}

        .reviewer-section label {{
            display: block;
            font-weight: bold;
            margin-bottom: 8px;
            font-size: 15px;
            color: #1a365d;
        }}

        .reviewer-section textarea {{
            width: 100%;
            padding: 12px;
            border-radius: 4px;
            border: 2px solid #2c5282;
            background: white;
            font-size: 14px;
            font-family: inherit;
            resize: vertical;
            box-sizing: border-box;
            margin-bottom: 15px;
        }}

        .reviewer-section textarea:focus {{
            outline: none;
            border-color: #2c5282;
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
        }}

        .field-note {{
            font-size: 13px;
            color: #4a5568;
            font-style: italic;
            margin-top: -10px;
            margin-bottom: 15px;
        }}

        .paragraph-block {{
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }}

        .paragraph-block.modified {{
            border-left: 4px solid #48bb78;
            background: #f0fff4;
        }}

        .heading-block {{
            background: #90cdf4;
            border: 2px solid #2c5282;
        }}

        .heading-block.modified {{
            background: #4299e1;
            border-left: 4px solid #2b6cb0;
        }}

        .para-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}

        .para-id {{
            font-family: monospace;
            font-size: 14px;
            background: #4a5568;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
        }}

        .chapter-num {{
            font-family: monospace;
            font-size: 16px;
            font-weight: bold;
            background: #2c5282;
            color: white;
            padding: 6px 12px;
            border-radius: 4px;
        }}

        .modified-badge {{
            display: none;
            background: #48bb78;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }}

        .paragraph-block.modified .modified-badge {{
            display: inline-block;
        }}

        .english-ref, .thai-edit, .comment {{
            margin-bottom: 15px;
        }}

        .english-ref {{
            background: white;
            padding: 15px;
            border-radius: 4px;
            border-left: 3px solid #3182ce;
        }}

        .english-ref label {{
            display: block;
            font-weight: bold;
            color: #2d3748;
            margin-bottom: 8px;
            font-size: 14px;
        }}

        .english-ref p {{
            margin: 0;
            color: #4a5568;
            line-height: 1.6;
        }}

        .thai-edit label {{
            display: block;
            font-weight: bold;
            color: #2d3748;
            margin-bottom: 8px;
            font-size: 14px;
        }}

        .thai-edit textarea {{
            width: 100%;
            min-height: 80px;
            padding: 12px;
            border: 2px solid #cbd5e0;
            border-radius: 4px;
            font-size: 16px;
            font-family: inherit;
            resize: vertical;
            box-sizing: border-box;
        }}

        .thai-edit textarea:focus {{
            outline: none;
            border-color: #4299e1;
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
        }}

        .comment input {{
            width: 100%;
            padding: 8px;
            border: 1px solid #cbd5e0;
            border-radius: 4px;
            font-size: 14px;
            box-sizing: border-box;
        }}

        footer {{
            position: sticky;
            bottom: 0;
            background: white;
            padding: 20px;
            border-top: 2px solid #e2e8f0;
            box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 30px;
        }}

        #download-btn {{
            background: #48bb78;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            transition: background 0.2s;
        }}

        #download-btn:hover {{
            background: #38a169;
        }}

        #download-btn:active {{
            background: #2f855a;
        }}

        #stats {{
            display: flex;
            gap: 20px;
            font-size: 14px;
            color: #4a5568;
        }}

        #stats span {{
            padding: 6px 12px;
            background: #edf2f7;
            border-radius: 4px;
        }}

        #edited-count {{
            font-weight: bold;
            background: #bee3f8;
            color: #2c5282;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Recovery Dharma - {language_name} Translation Correction Tool</h1>
    </header>

    <div class="reviewer-section">
        <h2>👤 About You</h2>
        <p>Please provide your information before starting the review. This helps us track contributions and contact you if needed.</p>

        <div class="editor-info">
            <input type="text" id="editor-name" placeholder="Your Full Name *" required>
            <input type="email" id="editor-email" placeholder="Your Email Address *" required>
        </div>

        <label for="about-yourself">Tell us about yourself (optional):</label>
        <p class="field-note">Your background, qualifications, or relevant experience (e.g., "Native Thai speaker", "Buddhist scholar", "Professional translator")</p>
        <textarea id="about-yourself" rows="3" placeholder="Example: Native Thai speaker with 10 years translation experience. Studied Buddhist texts at university..."></textarea>

        <label for="overall-notes">Overall review notes (optional):</label>
        <p class="field-note">General observations about the entire translation</p>
        <textarea id="overall-notes" rows="4" placeholder="Example: Overall quality is good. Found some inconsistent terminology in Chapter 24. Recommend second review for Buddhist technical terms..."></textarea>
    </div>

    <main>
        <form id="correction-form">
'''

    # Generate content blocks
    for item in content_items:
        item_type = item['type']
        item_id = item['id']
        chapter_num = item.get('chapter_num', '')
        english_text = item['english_text']
        thai_text = item['thai_text']

        # Escape quotes for HTML attributes
        thai_text_escaped = thai_text.replace('"', '&quot;').replace("'", '&#39;')

        if item_type == 'heading':
            # Chapter heading block
            html += f'''            <div class="paragraph-block heading-block" data-id="{item_id}" data-chapter="{chapter_num}">
                <div class="para-header">
                    <span class="modified-badge">MODIFIED</span>
                </div>

                <div class="english-ref">
                    <label>English Chapter Title:</label>
                    <p style="font-size: 1.2em; font-weight: bold;">{english_text}</p>
                </div>

                <div class="thai-edit">
                    <label>Thai Chapter Title (editable):</label>
                    <textarea
                        name="{item_id}"
                        data-original="{thai_text_escaped}"
                        data-chapter="{chapter_num}"
                        style="font-size: 1.1em; font-weight: bold; min-height: 60px;"
                    >{thai_text}</textarea>
                </div>

                <div class="comment">
                    <label>Comment (optional):</label>
                    <input type="text" name="{item_id}-comment" placeholder="Notes about this chapter title">
                </div>
            </div>

'''
        else:
            # Regular paragraph block
            html += f'''            <div class="paragraph-block" data-id="{item_id}" data-chapter="{chapter_num}">
                <div class="para-header">
                    <span class="para-id">{item_id}</span>
                    <span class="modified-badge">MODIFIED</span>
                </div>

                <div class="english-ref">
                    <label>English (reference):</label>
                    <p>{english_text}</p>
                </div>

                <div class="thai-edit">
                    <label>Thai (editable):</label>
                    <textarea
                        name="{item_id}"
                        data-original="{thai_text_escaped}"
                        data-chapter="{chapter_num}"
                    >{thai_text}</textarea>
                </div>

                <div class="comment">
                    <label>Comment (optional):</label>
                    <input type="text" name="{item_id}-comment" placeholder="Notes or explanation for this correction">
                </div>
            </div>

'''

    # Add footer and JavaScript
    html += f'''        </form>
    </main>

    <footer>
        <button type="button" id="download-btn">📥 Download Corrections JSON</button>
        <div id="stats">
            <span id="total-count">{len(content_items)} items ({headings_count} chapters + {paragraphs_count} paragraphs)</span>
            <span id="edited-count">0 edited</span>
        </div>
    </footer>

    <script>
        // Track modifications
        let editedCount = 0;

        // Add change listeners to all textareas
        document.querySelectorAll('textarea[name]').forEach(textarea => {{
            textarea.addEventListener('input', function() {{
                const original = this.dataset.original;
                const current = this.value;
                const block = this.closest('.paragraph-block');

                if (current !== original) {{
                    block.classList.add('modified');
                }} else {{
                    block.classList.remove('modified');
                }}

                // Update count
                editedCount = document.querySelectorAll('.paragraph-block.modified').length;
                document.getElementById('edited-count').textContent = editedCount + ' edited';
            }});
        }});

        // Download button handler
        document.getElementById('download-btn').addEventListener('click', function() {{
            // Validate required fields
            const editorName = document.getElementById('editor-name').value.trim();
            const editorEmail = document.getElementById('editor-email').value.trim();

            if (!editorName || !editorEmail) {{
                alert('⚠️ Please fill in your name and email address before downloading corrections.');
                // Focus on first empty field
                if (!editorName) {{
                    document.getElementById('editor-name').focus();
                }} else {{
                    document.getElementById('editor-email').focus();
                }}
                return;
            }}

            // Validate email format
            const emailPattern = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
            if (!emailPattern.test(editorEmail)) {{
                alert('⚠️ Please enter a valid email address.');
                document.getElementById('editor-email').focus();
                return;
            }}

            // Get optional fields
            const aboutYourself = document.getElementById('about-yourself').value.trim();
            const overallNotes = document.getElementById('overall-notes').value.trim();

            const corrections = [];

            // Collect all modified items
            document.querySelectorAll('.paragraph-block.modified').forEach(block => {{
                const itemId = block.dataset.id;
                const chapterNum = block.dataset.chapter;
                const textarea = block.querySelector('textarea');
                const commentInput = block.querySelector('input[name$="-comment"]');

                const correction = {{
                    id: itemId,
                    chapter: parseInt(chapterNum),
                    original: textarea.dataset.original,
                    edited: textarea.value,
                    status_update: 'corrected'
                }};

                // Add comment if provided
                const comment = commentInput.value.trim();
                if (comment) {{
                    correction.comment = comment;
                }}

                corrections.push(correction);
            }});

            // Build JSON output
            const output = {{
                metadata: {{
                    language: 'thai',
                    editor: editorName,
                    editor_email: editorEmail,
                    timestamp: new Date().toISOString(),
                    source_file: 'RDGBook_Thai.md',
                    total_items: {len(content_items)},
                    edited_items: corrections.length,
                    chapters_covered: [...new Set(corrections.map(c => c.chapter))].sort((a,b) => a-b)
                }},
                corrections: corrections
            }};

            // Add optional fields if provided
            if (aboutYourself) {{
                output.metadata.about_reviewer = aboutYourself;
            }}
            if (overallNotes) {{
                output.metadata.overall_notes = overallNotes;
            }}

            // Create download
            const jsonStr = JSON.stringify(output, null, 2);
            const blob = new Blob([jsonStr], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.href = url;
            const timestamp = new Date().toISOString().split('T')[0];
            a.download = `thai_corrections_${{timestamp}}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            alert(`✓ Downloaded corrections for ${{corrections.length}} items across ${{output.metadata.chapters_covered.length}} chapters!`);
        }});

        // Warn before leaving if there are unsaved edits
        window.addEventListener('beforeunload', function(e) {{
            if (editedCount > 0) {{
                e.preventDefault();
                e.returnValue = '';
                return '';
            }}
        }});
    </script>
</body>
</html>
'''

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n✓ Generated {output_file}")
    print(f"✓ Ready for translation correction")

if __name__ == '__main__':
    import sys

    # Default to Thai if no arguments provided (backward compatibility)
    if len(sys.argv) > 1:
        language = sys.argv[1].lower()
    else:
        language = 'thai'

    # Language name mapping (for display)
    language_names = {
        'thai': 'Thai',
        'japanese': 'Japanese',
        'vietnamese': 'Vietnamese',
        'korean': 'Korean',
        'simplified_chinese': 'Simplified Chinese',
        'traditional_chinese': 'Traditional Chinese'
    }

    # File name mapping
    language_files = {
        'thai': 'RDGBook_Thai.md',
        'japanese': 'RDGBook_Japanese.md',
        'vietnamese': 'RDGBook_Vietnamese.md',
        'korean': 'RDGBook_Korean.md',
        'simplified_chinese': 'RDGBook_SimplifiedChinese.md',
        'traditional_chinese': 'RDGBook_TraditionalChinese.md'
    }

    # Output file mapping
    output_files = {
        'thai': 'tmasterThai.html',
        'japanese': 'tmasterJapanese.html',
        'vietnamese': 'tmasterVietnamese.html',
        'korean': 'tmasterKorean.html',
        'simplified_chinese': 'tmasterSimplifiedChinese.html',
        'traditional_chinese': 'tmasterTraditionalChinese.html'
    }

    if language not in language_files:
        print(f"Error: Unknown language '{language}'")
        print(f"Available languages: {', '.join(language_files.keys())}")
        sys.exit(1)

    workmaster_json = '/home/scott/gitrepos/rdgtrans/workmaster.json'
    english_md = '/home/scott/gitrepos/rdgtrans/lmasters/RDGBook_English.md'
    language_md = f'/home/scott/gitrepos/rdgtrans/lmasters/{language_files[language]}'
    output_file = f'/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/{output_files[language]}'
    language_name = language_names[language]

    print(f"\n{'='*60}")
    print(f"Generating {language_name} Translation Master")
    print(f"{'='*60}\n")

    generate_tmaster_v2(workmaster_json, english_md, language_md, output_file, language_name)
