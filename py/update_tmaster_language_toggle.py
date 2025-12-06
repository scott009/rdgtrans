#!/usr/bin/env python3
"""
Update tmaster HTML files with language toggle functionality.
Adds data-pr-id attributes, CSS, and JavaScript for multilingual UI.
"""

import re
import sys
from pathlib import Path

def update_japanese_tmaster(input_file, output_file):
    """Update Japanese tmaster with language toggle feature."""

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add language toggle CSS before the closing </style> tag
    language_toggle_css = """
        #language-toggle {
            background: #2b6cb0;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }

        #language-toggle:hover {
            background: #2c5282;
        }

        #language-toggle:active {
            background: #1e4e8c;
        }
"""

    # Find the last </style> tag and insert CSS before it
    content = content.replace('    </style>', language_toggle_css + '    </style>', 1)

    # 2. Add data-pr-id attributes to header elements
    content = re.sub(
        r'<h1>Recovery Dharma - Japanese Translation Correction Tool</h1>',
        r'<h1 data-pr-id="pr_6">Recovery Dharma - Japanese Translation Correction Tool</h1>',
        content
    )

    # 3. Add data-pr-id to reviewer section elements
    # Update "About You" section if it exists (might not be styled exactly like Thai version)
    content = re.sub(
        r'<h2>About You</h2>',
        r'<h2 data-pr-id="pr_7">👤 About You</h2>',
        content
    )

    # Add section description if missing
    if 'Please provide your information before starting' not in content:
        # Add it after the h2
        content = re.sub(
            r'(<h2 data-pr-id="pr_7">.*?</h2>)',
            r'\1\n        <p data-pr-id="pr_27">Please provide your information before starting the review. This helps us track contributions and contact you if needed.</p>',
            content
        )

    # 4. Update input placeholders with data-pr-id and data-pr-type
    content = re.sub(
        r'<input type="text" id="editor-name"([^>]*?)placeholder="Your Full Name \*"',
        r'<input type="text" id="editor-name" data-pr-id="pr_8" data-pr-type="placeholder" placeholder="Your Full Name *"',
        content
    )

    content = re.sub(
        r'<input type="email" id="editor-email"([^>]*?)placeholder="Your Email Address \*"',
        r'<input type="email" id="editor-email" data-pr-id="pr_9" data-pr-type="placeholder" placeholder="Your Email Address *"',
        content
    )

    # 5. Add data-pr-id to all label elements
    # English Chapter Title label
    content = re.sub(
        r'<label>English Chapter Title:</label>',
        r'<label data-pr-id="pr_2">English Chapter Title:</label>',
        content
    )

    # Japanese Chapter Title label (editable)
    content = re.sub(
        r'<label>Japanese Chapter Title \(editable\):</label>',
        r'<label data-pr-id="pr_17">Japanese Chapter Title (editable):</label>',
        content
    )

    # English (reference) label
    content = re.sub(
        r'<label>English \(reference\):</label>',
        r'<label data-pr-id="pr_14">English (reference):</label>',
        content
    )

    # Japanese (editable) label
    content = re.sub(
        r'<label>Japanese \(editable\):</label>',
        r'<label data-pr-id="pr_22">Japanese (editable):</label>',
        content
    )

    # Comment labels
    content = re.sub(
        r'<label>Comment \(optional\):</label>',
        r'<label data-pr-id="pr_16">Comment (optional):</label>',
        content
    )

    # 6. Add data-pr-id to comment input placeholders
    content = re.sub(
        r'<input type="text" name="([^"]+)-comment" placeholder="Notes about this chapter title">',
        r'<input type="text" name="\1-comment" data-pr-id="pr_34" data-pr-type="placeholder" placeholder="Notes about this chapter title">',
        content
    )

    content = re.sub(
        r'<input type="text" name="([^"]+)-comment" placeholder="Notes or explanation for this correction">',
        r'<input type="text" name="\1-comment" data-pr-id="pr_35" data-pr-type="placeholder" placeholder="Notes or explanation for this correction">',
        content
    )

    # 7. Add data-pr-id to MODIFIED badges
    content = re.sub(
        r'<span class="modified-badge">MODIFIED</span>',
        r'<span class="modified-badge" data-pr-id="pr_36">MODIFIED</span>',
        content
    )

    # 8. Update footer to include language toggle button
    footer_pattern = r'(<footer>.*?<button[^>]*id="download-btn"[^>]*>Submit</button>)'
    footer_replacement = r'''<footer>
        <div class="footer-buttons">
            <button type="button" id="language-toggle">日本語で表示</button>
            <button type="button" id="download-btn" data-pr-id="pr_37">Submit</button>
        </div>'''

    if '<footer>' in content and 'language-toggle' not in content:
        # Replace the footer section
        content = re.sub(
            r'<footer>\s*<button[^>]*id="download-btn"',
            r'<footer>\n        <div class="footer-buttons">\n            <button type="button" id="language-toggle">日本語で表示</button>\n            <button type="button" id="download-btn" data-pr-id="pr_37"',
            content
        )

        # Close the footer-buttons div after the download button
        content = re.sub(
            r'(<button[^>]*id="download-btn"[^>]*>Submit</button>)',
            r'\1\n        </div>',
            content
        )

    # 9. Add language toggle JavaScript before existing script
    language_toggle_js = '''    <script>
        // Language Toggle Functionality
        let currentLanguage = 'english';
        let translations = null;

        // Load translations from external JSON file
        async function loadTranslations() {
            try {
                const response = await fetch('presentation.json');
                const data = await response.json();
                translations = data.translation_sets;
                console.log('Translations loaded successfully');
            } catch (error) {
                console.error('Error loading translations:', error);
                // Fallback for development - disable toggle if can't load
                const toggleBtn = document.getElementById('language-toggle');
                if (toggleBtn) {
                    toggleBtn.disabled = true;
                    toggleBtn.title = 'Translation data not available';
                    toggleBtn.style.opacity = '0.5';
                }
            }
        }

        // Toggle language function
        function toggleLanguage() {
            if (!translations) {
                console.warn('Translations not loaded yet');
                return;
            }

            // Switch language
            currentLanguage = (currentLanguage === 'english') ? 'japanese' : 'english';
            const langSet = translations[currentLanguage];

            // Update all elements with data-pr-id
            document.querySelectorAll('[data-pr-id]').forEach(element => {
                const prId = element.getAttribute('data-pr-id');
                const prType = element.getAttribute('data-pr-type');

                if (langSet[prId]) {
                    const newText = langSet[prId].text;

                    // Handle different element types
                    if (prType === 'placeholder') {
                        element.placeholder = newText;
                    } else if (element.tagName === 'INPUT' && element.type === 'submit') {
                        element.value = newText;
                    } else if (element.tagName === 'BUTTON') {
                        element.textContent = newText;
                    } else {
                        // For labels, spans, h1, h2, p, etc.
                        element.textContent = newText;
                    }
                }
            });

            // Update button text to show current state
            const toggleBtn = document.getElementById('language-toggle');
            toggleBtn.textContent = currentLanguage === 'english' ?
                '日本語で表示' : 'Show in English';
        }

        // Initialize language toggle
        document.addEventListener('DOMContentLoaded', async function() {
            // Load translations first
            await loadTranslations();

            // Set up toggle button
            const toggleBtn = document.getElementById('language-toggle');
            if (toggleBtn) {
                toggleBtn.addEventListener('click', toggleLanguage);
            }

            console.log('Language toggle initialized successfully');
        });
    </script>

'''

    # Insert before the first <script> tag
    if '<script>' in content and 'Language Toggle Functionality' not in content:
        content = content.replace('<script>', language_toggle_js + '    <script>', 1)

    # Write the updated content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Updated {output_file}")
    print("  - Added language toggle CSS")
    print("  - Added data-pr-id attributes to UI elements")
    print("  - Added language toggle button to footer")
    print("  - Added language toggle JavaScript")

if __name__ == '__main__':
    input_file = '/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/tmasterJapanese.html'
    output_file = input_file  # Update in place

    print(f"Updating Japanese tmaster with language toggle feature...")
    update_japanese_tmaster(input_file, output_file)
    print("\nDone!")
