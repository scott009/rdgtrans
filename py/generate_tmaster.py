#!/usr/bin/env python3
"""
Generate Translation Master HTML
Creates bilingual correction form from English and Thai HTML sources
"""

import re
import json
from datetime import datetime
import html

def extract_content(html_file):
    """Extract paragraphs and chapter headings from HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    items = {}

    # Extract paragraphs: <p id="pX-Y" ...>CONTENT</p>
    para_pattern = r'<p\s+id="(p[^"]+)"[^>]*>(.*?)</p>'
    for match in re.finditer(para_pattern, content, re.DOTALL):
        pid = match.group(1)
        text_html = match.group(2)

        # Remove HTML tags and decode entities
        text = re.sub(r'<[^>]+>', '', text_html)
        text = html.unescape(text)
        text = ' '.join(text.split())  # Normalize whitespace

        items[pid] = {'type': 'paragraph', 'text': text}

    # Extract chapter headings: <h2 class="chaptermain" id="...">CONTENT</h2>
    heading_pattern = r'<h2\s+class="chaptermain"[^>]*id="([^"]+)"[^>]*>(.*?)</h2>'
    for match in re.finditer(heading_pattern, content, re.DOTALL):
        hid = match.group(1)
        text_html = match.group(2)

        # Remove HTML tags and decode entities
        text = re.sub(r'<[^>]+>', '', text_html)
        text = html.unescape(text)
        text = text.strip()

        items[hid] = {'type': 'heading', 'text': text}

    return items

def generate_tmaster(english_html, thai_html, output_file, language_name="Thai"):
    """Generate translation master HTML"""

    # Manual mapping of English chapter IDs to Thai chapter IDs
    chapter_mapping = {
        "preface": "คำนำ",
        "what-is-recovery-dharma": "การฟื้นฟูด้วยธรรมะคืออะไร?",
        "where-to-begin": "เริ่มต้นจากที่ไหน",
        "the-practice": "การปฏิบัติ",
        "awakening-buddha": "การตื่นรู้-พระพุทธเจ้า",
        "the-story-of-the-original-buddha": "เรื่องราวของพระพุทธเจ้ากำเนิด",
        "walking-in-the-footsteps-of-the-buddha": "เดินตามรอยพระพุทธเจ้า",
        "the-truth-dharma": "ความจริง-ธรรมะ",
        "the-first-noble-truth": "สัจจะข้อแรก",
        "the-second-noble-truth": "สัจจะข้อที่สอง",
        "the-third-noble-truth": "สัจจะข้อที่สาม",
        "the-fourth-noble-truth": "สัจจะข้อที่สี่",
        "the-eightfold-path": "มัฌฌิมาปฏิปทา",
        "wise-understanding": "ความเข้าใจที่ชาญฉลาด",
        "wise-intention": "จิตสำนึกที่ชาญฉลาด",
        "wise-speech": "การพูดที่ชาญฉลาด",
        "wise-action": "การกระทำที่ชาญฉลาด",
        "wise-livelihood": "การประกอบอาชีพที่ชาญฉลาด",
        "wise-effort": "ความพยายามที่ชาญฉลาด",
        "wise-mindfulness": "ความระลึกที่ชาญฉลาด",
        "wise-concentration": "ความเข้มข้นที่ชาญฉลาด",
        "community-sangha": "สถาบัน-สงฆ์",
        "isolation-and-connection": "การแยกตัวและการเชื่อมต่อ",
        "reaching-out": "การเอื้อมมือออกไป",
        "wise-friends-and-mentors": "เพื่อนที่ฉลาดและพี่เลี้ยง",
        "service-and-generosity": "การบริการและความเอื้อเฟื้อเผื่อแผ่",
        "recovery-is-possible": "การฟื้นฟูเป็นไปได้",
    }

    print(f"Reading {english_html}...")
    english_items = extract_content(english_html)
    eng_paras = sum(1 for v in english_items.values() if v['type'] == 'paragraph')
    eng_heads = sum(1 for v in english_items.values() if v['type'] == 'heading')
    print(f"  Found {eng_paras} paragraphs, {eng_heads} headings")

    print(f"Reading {thai_html}...")
    thai_items = extract_content(thai_html)
    thai_paras = sum(1 for v in thai_items.values() if v['type'] == 'paragraph')
    thai_heads = sum(1 for v in thai_items.values() if v['type'] == 'heading')
    print(f"  Found {thai_paras} paragraphs, {thai_heads} headings")

    # Apply chapter mapping: add Thai chapters with English IDs as keys
    mapped_items = {}
    for eng_id, thai_id in chapter_mapping.items():
        if eng_id in english_items and thai_id in thai_items:
            # Create a combined item with English ID as key
            mapped_items[eng_id] = {
                'type': 'heading',
                'english_text': english_items[eng_id]['text'],
                'thai_text': thai_items[thai_id]['text'],
                'thai_id': thai_id  # Keep Thai ID for reference
            }

    # Find common paragraph IDs (these match directly)
    common_para_ids = sorted(set(english_items.keys()) & set(thai_items.keys()))
    for pid in common_para_ids:
        if english_items[pid]['type'] == 'paragraph' and thai_items[pid]['type'] == 'paragraph':
            mapped_items[pid] = {
                'type': 'paragraph',
                'english_text': english_items[pid]['text'],
                'thai_text': thai_items[pid]['text']
            }

    common_ids = sorted(mapped_items.keys())
    matched_heads = sum(1 for v in mapped_items.values() if v['type'] == 'heading')
    matched_paras = sum(1 for v in mapped_items.values() if v['type'] == 'paragraph')
    print(f"  Matched {matched_heads} chapter headings, {matched_paras} paragraphs")
    print(f"  Total: {len(common_ids)} items")

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
            margin-bottom: 30px;
        }}

        header h1 {{
            margin: 0 0 15px 0;
        }}

        .editor-info {{
            display: flex;
            gap: 15px;
            margin-top: 15px;
        }}

        .editor-info input {{
            flex: 1;
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #ddd;
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
        <p>Review and correct Thai translations. Your edits will be saved to a JSON file.</p>
        <div class="editor-info">
            <input type="text" id="editor-name" placeholder="Your Name (optional)">
            <input type="email" id="editor-email" placeholder="Your Email (optional)">
        </div>
    </header>

    <main>
        <form id="correction-form">
'''

    # Generate content blocks (headings and paragraphs)
    for item_id in common_ids:
        item = mapped_items[item_id]
        item_type = item['type']
        english_text = item['english_text']
        thai_text = item['thai_text']

        # Escape quotes for HTML attributes
        thai_text_escaped = thai_text.replace('"', '&quot;').replace("'", '&#39;')

        if item_type == 'heading':
            # Chapter heading block
            html += f'''            <div class="paragraph-block heading-block" data-id="{item_id}">
                <div class="para-header">
                    <span class="para-id">📖 CHAPTER: {item_id}</span>
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
            html += f'''            <div class="paragraph-block" data-id="{item_id}">
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
            <span id="total-count">{len(common_ids)} paragraphs</span>
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
            const editorName = document.getElementById('editor-name').value || 'Anonymous';
            const editorEmail = document.getElementById('editor-email').value || '';

            const corrections = [];

            // Collect all modified paragraphs
            document.querySelectorAll('.paragraph-block.modified').forEach(block => {{
                const pid = block.dataset.id;
                const textarea = block.querySelector('textarea');
                const commentInput = block.querySelector('input[name$="-comment"]');

                const correction = {{
                    id: pid,
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
                    source_file: 'rdgThai2.html',
                    total_paragraphs: {len(common_ids)},
                    edited_paragraphs: corrections.length
                }},
                corrections: corrections
            }};

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

            alert(`Downloaded corrections for ${{corrections.length}} paragraphs!`);
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
    print(f"✓ Contains {len(common_ids)} paragraph pairs")
    print(f"✓ Ready for translation correction")

if __name__ == '__main__':
    english_html = '/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/rdgBook2.html'
    thai_html = '/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/rdgThai2.html'
    output_file = '/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/tmasterThai.html'

    generate_tmaster(english_html, thai_html, output_file)
