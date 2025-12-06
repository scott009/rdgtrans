#!/usr/bin/env python3
"""
Generate Translation Master HTML files from presentation.json specification.

This script generates tmaster HTML files using presentation.json as the
authoritative source for container structure, UI translations, and language
configuration.

Usage:
    python3 generate_tmaster_from_presmaster.py <language>

Languages:
    thai, japanese, korean, simplified_chinese, traditional_chinese, vietnamese

Example:
    python3 generate_tmaster_from_presmaster.py japanese

Requirements:
    - presentation.json v3.0+ with container_types.tmaster definition
    - workmaster.json for chapter/paragraph structure
    - Language master files in lmasters/
    - CSS template file (extracted from reference implementation)
    - JavaScript template files (extracted from reference implementation)
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class TmasterGenerator:
    """Generate tmaster HTML files from presentation.json specification."""

    def __init__(self, language: str, projhome: str = None):
        """
        Initialize generator.

        Args:
            language: Target language (thai, japanese, korean, etc.)
            projhome: Project home directory (defaults to current location)
        """
        self.language = language
        self.projhome = Path(projhome) if projhome else Path('/home/scott/gitrepos/rdgtrans')

        # Load configuration files
        self.presmaster = self._load_json(self.projhome / 'presentation.json')
        self.workmaster = self._load_json(self.projhome / 'workmaster.json')

        # Get tmaster container specification
        self.tmaster_spec = self.presmaster['container_types']['tmaster']
        self.lang_config = self.tmaster_spec['language_config'][language]

        # Paths from presmaster
        self.paths = self.presmaster['paths']
        self.lmasters = Path(self.paths['lmasters'])
        self.showoff_docs = Path(self.paths['showoff_docs'])

        # Load language master files
        self.english_content = self._load_master_file('RDGBook_English.md')
        self.target_content = self._load_master_file(self.lang_config['master_file'])

        # Extract chapter structure from workmaster
        self.chapters = self._extract_chapters()

        # UI translations
        self.ui_english = self.presmaster['translation_sets']['english']
        self.ui_target = self.presmaster['translation_sets'][language]

    def _load_json(self, filepath: Path) -> dict:
        """Load and parse JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_master_file(self, filename: str) -> Dict[str, str]:
        """
        Load language master file and extract content by paragraph ID.

        Returns:
            Dict mapping paragraph IDs to content strings
        """
        filepath = self.lmasters / filename
        content = {}

        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

        # Extract paragraphs using regex
        # Format: <!--[p3-1]-->
        # Content between markers
        pattern = r'<!--\[([^\]]+)\]-->\s*\n(.*?)(?=<!--\[|$)'
        matches = re.findall(pattern, text, re.DOTALL)

        for para_id, para_text in matches:
            content[para_id] = para_text.strip()

        return content

    def _extract_chapters(self) -> List[dict]:
        """Extract chapter structure from workmaster.json."""
        chapters = []

        for chapter in self.workmaster['chapters']:
            if chapter['type'] == 'chapter':
                chapter_data = {
                    'id': chapter['id'],
                    'number': chapter['chapter_number'],
                    'slug': chapter['slug'],
                    'title': chapter['chapter_title'],
                    'paragraphs': []
                }

                # Extract paragraphs
                for item in chapter.get('content', []):
                    if item['type'] == 'paragraph':
                        chapter_data['paragraphs'].append(item['id'])

                chapters.append(chapter_data)

        return chapters

    def _get_ui_text(self, pr_id: str, use_english: bool = True) -> str:
        """Get UI text for a given pr_id."""
        ui_set = self.ui_english if use_english else self.ui_target
        return ui_set.get(pr_id, {}).get('text', '')

    def generate_css(self) -> str:
        """Generate embedded CSS from template."""
        # For now, read from reference implementation
        # In future, could generate from spec or template file
        ref_file = self.showoff_docs / 'tmasterThai.html'

        with open(ref_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract CSS between <style> and </style>
        match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
        if match:
            return match.group(1)

        return ""

    def generate_javascript(self) -> str:
        """Generate embedded JavaScript from template."""
        # Read from reference implementation
        ref_file = self.showoff_docs / 'tmasterThai.html'

        with open(ref_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract first <script> block
        match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
        if match:
            js_template = match.group(1)

            # Replace language-specific values
            js_template = js_template.replace("'thai'", f"'{self.language}'")
            js_template = js_template.replace('แสดงเป็นภาษาไทย', self.lang_config['toggle_text_native'])

            return js_template

        return ""

    def generate_header(self) -> str:
        """Generate header section."""
        return f'''    <header>
        <h1 data-pr-id="pr_6">{self._get_ui_text('pr_6')}</h1>
    </header>'''

    def generate_reviewer_section(self) -> str:
        """Generate reviewer information section."""
        return f'''    <div class="reviewer-section">
        <h2 data-pr-id="pr_7">{self._get_ui_text('pr_7')}</h2>
        <p data-pr-id="pr_27">{self._get_ui_text('pr_27')}</p>

        <div class="editor-info">
            <input type="text" id="editor-name" data-pr-id="pr_8" data-pr-type="placeholder" placeholder="{self._get_ui_text('pr_8')}" required>
            <input type="email" id="editor-email" data-pr-id="pr_9" data-pr-type="placeholder" placeholder="{self._get_ui_text('pr_9')}" required>
        </div>

        <label for="about-yourself" data-pr-id="pr_28">{self._get_ui_text('pr_28')}</label>
        <p class="field-note" data-pr-id="pr_29">{self._get_ui_text('pr_29')}</p>
        <textarea id="about-yourself" rows="3" data-pr-id="pr_30" data-pr-type="placeholder" placeholder="{self._get_ui_text('pr_30')}"></textarea>

        <label for="overall-notes" data-pr-id="pr_31">{self._get_ui_text('pr_31')}</label>
        <p class="field-note" data-pr-id="pr_32">{self._get_ui_text('pr_32')}</p>
        <textarea id="overall-notes" rows="4" data-pr-id="pr_33" data-pr-type="placeholder" placeholder="{self._get_ui_text('pr_33')}"></textarea>
    </div>'''

    def generate_chapter_block(self, chapter: dict) -> str:
        """Generate HTML for a chapter title block."""
        chapter_num = chapter['number']
        chapter_id = chapter['id']

        # Get English and target language titles
        english_title = self.english_content.get(chapter_id, '[Missing English title]')
        target_title = self.target_content.get(chapter_id, '[Missing translation]')

        pr_title = self.lang_config['pr_title']

        return f'''            <div class="paragraph-block heading-block" data-id="chapter-{chapter_num}" data-chapter="{chapter_num}">
                <div class="para-header">
                    <span class="chapter-num">📖 CHAPTER {chapter_num}</span>
                    <span class="modified-badge" data-pr-id="pr_36">{self._get_ui_text('pr_36')}</span>
                </div>

                <div class="english-ref">
                    <label data-pr-id="pr_2">{self._get_ui_text('pr_2')}</label>
                    <p>{english_title}</p>
                </div>

                <div class="thai-edit">
                    <label data-pr-id="{pr_title}">{self._get_ui_text(pr_title)}</label>
                    <textarea
                        name="chapter-{chapter_num}"
                        data-original="{target_title}"
                        data-chapter="{chapter_num}"
                    >{target_title}</textarea>
                </div>

                <div class="comment">
                    <label data-pr-id="pr_16">{self._get_ui_text('pr_16')}</label>
                    <input type="text" name="chapter-{chapter_num}-comment" data-pr-id="pr_34" data-pr-type="placeholder" placeholder="{self._get_ui_text('pr_34')}">
                </div>
            </div>'''

    def generate_paragraph_block(self, para_id: str, chapter_num: int) -> str:
        """Generate HTML for a paragraph block."""
        # Get English and target language content
        english_text = self.english_content.get(para_id, '[Missing English text]')
        target_text = self.target_content.get(para_id, '[Missing translation]')

        pr_edit = self.lang_config['pr_edit']

        # Display format for para_id
        display_id = f"Ch {chapter_num}: {para_id}"

        return f'''            <div class="paragraph-block" data-id="{para_id}" data-chapter="{chapter_num}">
                <div class="para-header">
                    <span class="para-id">{display_id}</span>
                    <span class="modified-badge" data-pr-id="pr_36">{self._get_ui_text('pr_36')}</span>
                </div>

                <div class="english-ref">
                    <label data-pr-id="pr_14">{self._get_ui_text('pr_14')}</label>
                    <p>{english_text}</p>
                </div>

                <div class="thai-edit">
                    <label data-pr-id="{pr_edit}">{self._get_ui_text(pr_edit)}</label>
                    <textarea
                        name="{para_id}"
                        data-original="{target_text}"
                        data-chapter="{chapter_num}"
                    >{target_text}</textarea>
                </div>

                <div class="comment">
                    <label data-pr-id="pr_16">{self._get_ui_text('pr_16')}</label>
                    <input type="text" name="{para_id}-comment" data-pr-id="pr_35" data-pr-type="placeholder" placeholder="{self._get_ui_text('pr_35')}">
                </div>
            </div>'''

    def generate_content_form(self) -> str:
        """Generate main content form with all chapters and paragraphs."""
        blocks = []

        for chapter in self.chapters:
            # Add chapter title block
            blocks.append(self.generate_chapter_block(chapter))

            # Add paragraph blocks
            for para_id in chapter['paragraphs']:
                blocks.append(self.generate_paragraph_block(para_id, chapter['number']))

        form_html = '''    <main>
        <form id="correction-form">
''' + '\n\n'.join(blocks) + '''

        </form>
    </main>'''

        return form_html

    def generate_footer(self) -> str:
        """Generate footer with buttons and stats."""
        toggle_text = self.lang_config['toggle_text_native']

        # Count total items
        total_chapters = len(self.chapters)
        total_paragraphs = sum(len(ch['paragraphs']) for ch in self.chapters)
        total_items = total_chapters + total_paragraphs

        return f'''    <footer>
        <div class="footer-buttons">
            <button type="button" id="language-toggle">{toggle_text}</button>
            <button type="button" id="download-btn" data-pr-id="pr_37">{self._get_ui_text('pr_37')}</button>
        </div>
        <div id="stats">
            <span id="total-count">{total_items} items ({total_chapters} chapters + {total_paragraphs} paragraphs)</span>
            <span id="edited-count">0 edited</span>
        </div>
    </footer>'''

    def generate_html(self) -> str:
        """Generate complete HTML document."""
        lang_code = self.lang_config['code']
        lang_name = self.language.replace('_', ' ').title()

        html = f'''<!DOCTYPE html>
<html lang="{lang_code}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{lang_name} Translation Master - Correction Tool</title>
    <link rel="stylesheet" href="ada3.css">
    <style>
{self.generate_css()}
    </style>
</head>
<body>
{self.generate_header()}

{self.generate_reviewer_section()}

{self.generate_content_form()}

{self.generate_footer()}

    <script>
{self.generate_javascript()}
    </script>

    <script src="submit-handler.js"></script>
</body>
</html>
'''
        return html

    def generate_file(self, output_path: Path = None) -> str:
        """
        Generate tmaster HTML file and write to disk.

        Args:
            output_path: Optional output path. Defaults to showoff_docs.

        Returns:
            Path to generated file
        """
        if output_path is None:
            output_path = self.showoff_docs / self.lang_config['output_file']

        html = self.generate_html()

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        return str(output_path)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 generate_tmaster_from_presmaster.py <language>")
        print("\nAvailable languages:")
        print("  thai, japanese, korean")
        print("  simplified_chinese, traditional_chinese, vietnamese")
        sys.exit(1)

    language = sys.argv[1].lower()

    # Validate language
    valid_languages = ['thai', 'japanese', 'korean', 'simplified_chinese',
                      'traditional_chinese', 'vietnamese']

    if language not in valid_languages:
        print(f"Error: Invalid language '{language}'")
        print(f"Valid languages: {', '.join(valid_languages)}")
        sys.exit(1)

    try:
        print(f"Generating tmaster for {language}...")
        print(f"Reading presentation.json v3.0 container specification...")

        generator = TmasterGenerator(language)

        print(f"Loading workmaster.json structure...")
        print(f"Loading English source: RDGBook_English.md")
        print(f"Loading target language: {generator.lang_config['master_file']}")

        print(f"Generating HTML...")
        output_file = generator.generate_file()

        print(f"\n✓ Successfully generated: {output_file}")

        # Print statistics
        total_chapters = len(generator.chapters)
        total_paragraphs = sum(len(ch['paragraphs']) for ch in generator.chapters)
        print(f"  - Chapters: {total_chapters}")
        print(f"  - Paragraphs: {total_paragraphs}")
        print(f"  - Total items: {total_chapters + total_paragraphs}")
        print(f"  - Language code: {generator.lang_config['code']}")
        print(f"  - Toggle text: {generator.lang_config['toggle_text_native']}")

    except FileNotFoundError as e:
        print(f"Error: Required file not found: {e}")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing configuration key: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
