#!/usr/bin/env python3
"""
Update Translation Master HTML Files for GitHub Submission

This script modifies all tmaster*.html files to:
1. Include the new submit-handler.js script
2. Update the submit button handler to use the new GitHub submission function
3. Keep backward compatibility with download functionality
"""

import re
import os
from pathlib import Path

# Path to Windows output directory
DOCS_DIR = Path("/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs")

# URL to the submit-handler script (relative to the HTML files)
SUBMIT_HANDLER_URL = "https://YOUR-SITE-NAME.netlify.app/submit-handler.js"

def update_tmaster_file(filepath):
    """Update a single tmaster HTML file"""

    print(f"\nProcessing: {filepath.name}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract language from filename
    # e.g., tmasterThai.html -> thai
    match = re.search(r'tmaster([A-Za-z]+)\.html', filepath.name)
    if not match:
        print(f"  ⚠️  Could not extract language from filename")
        return False

    language = match.group(1).lower()
    # Handle special cases
    if language == 'simplifiedchinese':
        language = 'simplified_chinese'
    elif language == 'traditionalchinese':
        language = 'traditional_chinese'

    print(f"  Language: {language}")

    # Check if already updated
    if 'submit-handler.js' in content:
        print(f"  ℹ️  Already updated - skipping")
        return False

    # 1. Add script include before closing </body> tag
    script_include = f'\n    <script src="{SUBMIT_HANDLER_URL}"></script>\n</body>'
    content = content.replace('</body>', script_include)

    # 2. Find and modify the download button click handler
    # Look for: document.getElementById('download-btn').addEventListener('click', function() {

    pattern = r"document\.getElementById\('download-btn'\)\.addEventListener\('click', function\(\) \{(.*?)\}\);(?=\s*//|\s*</script>)"

    def replace_handler(match):
        # Extract the old handler content to preserve validation logic
        old_handler = match.group(1)

        # Build new handler
        new_handler = f"""document.getElementById('download-btn').addEventListener('click', async function() {{
        // Validate required fields
        const editorName = document.getElementById('editor-name').value.trim();
        const editorEmail = document.getElementById('editor-email').value.trim();

        if (!editorName || !editorEmail) {{
            alert('⚠️ Please fill in your name and email address before submitting.');
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
                language: '{language}',
                editor: editorName,
                editor_email: editorEmail,
                timestamp: new Date().toISOString(),
                source_file: 'RDGBook_{language.replace('_', '').title()}.md',
                total_items: document.querySelectorAll('.paragraph-block').length,
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

        // Use new submission handler (submits to GitHub + downloads backup)
        await handleFormSubmission(output);
    }});"""

        return new_handler

    # Replace the handler
    content_new = re.sub(pattern, replace_handler, content, flags=re.DOTALL)

    if content_new == content:
        print(f"  ⚠️  Could not find download button handler to replace")
        return False

    # Write updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content_new)

    print(f"  ✓ Updated successfully")
    return True

def main():
    """Update all tmaster HTML files"""

    print("=" * 60)
    print("Updating Translation Master Files for GitHub Submission")
    print("=" * 60)

    if not DOCS_DIR.exists():
        print(f"\n❌ Error: Directory not found: {DOCS_DIR}")
        return

    # Find all tmaster*.html files
    tmaster_files = sorted(DOCS_DIR.glob("tmaster*.html"))

    if not tmaster_files:
        print(f"\n❌ No tmaster*.html files found in {DOCS_DIR}")
        return

    print(f"\nFound {len(tmaster_files)} tmaster files")

    updated_count = 0
    for filepath in tmaster_files:
        if update_tmaster_file(filepath):
            updated_count += 1

    print("\n" + "=" * 60)
    print(f"✓ Complete: {updated_count} files updated")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Deploy to Netlify to get your function URL")
    print("2. Update NETLIFY_FUNCTION_URL in the files")
    print("3. Test with one language before rolling out to all")

if __name__ == '__main__':
    main()
