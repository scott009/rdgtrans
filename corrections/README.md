# Translation Corrections

This folder contains submitted translation corrections from bilingual reviewers using the Translation Master forms.

## File Format

Each correction submission is saved as a JSON file with the following naming convention:

```
{language}_{date}_{time}.json
```

Examples:
- `thai_2024-12-02_14-30-15.json`
- `japanese_2024-12-03_09-15-42.json`
- `vietnamese_2024-12-05_16-45-00.json`

## JSON Structure

```json
{
  "metadata": {
    "language": "thai",
    "editor": "Reviewer Name",
    "editor_email": "reviewer@example.com",
    "timestamp": "2024-12-02T14:30:15.123Z",
    "source_file": "RDGBook_Thai.md",
    "total_items": 396,
    "edited_items": 15,
    "chapters_covered": [1, 3, 5, 8],
    "about_reviewer": "Optional: Background information about the reviewer",
    "overall_notes": "Optional: General notes about the corrections"
  },
  "corrections": [
    {
      "id": "p1-1",
      "chapter": 1,
      "original": "Original Thai text here",
      "edited": "Corrected Thai text here",
      "status_update": "corrected",
      "comment": "Optional: Explanation of the correction"
    },
    ...
  ]
}
```

## Metadata Fields

- **language**: Target language (thai, japanese, korean, vietnamese, simplified_chinese, traditional_chinese)
- **editor**: Name of the person submitting corrections
- **editor_email**: Email address for follow-up questions
- **timestamp**: ISO 8601 timestamp of submission
- **source_file**: Original markdown file being corrected
- **total_items**: Total number of translatable items in the document
- **edited_items**: Number of items corrected in this submission
- **chapters_covered**: Array of chapter numbers that were edited
- **about_reviewer**: (Optional) Reviewer's background/qualifications
- **overall_notes**: (Optional) General observations or comments

## Correction Fields

- **id**: Unique identifier for the paragraph (e.g., "p1-1", "h2-3")
- **chapter**: Chapter number
- **original**: The AI-generated translation before correction
- **edited**: The corrected/improved translation
- **status_update**: Always "corrected" for submitted items
- **comment**: (Optional) Explanation of why the change was made

## Processing Workflow

1. **Review submissions**: Check new files in this folder
2. **Quality check**: Verify corrections make sense
3. **Apply to master**: Update the appropriate language markdown file in `/lmasters/`
4. **Update workmaster.json**: Mark items as reviewed/corrected
5. **Regenerate HTML**: Run generation scripts to update tmaster files
6. **Archive**: Move processed corrections to `/archive/corrections/`

## Automated Submissions

Files in this folder are automatically created by the Netlify serverless function when reviewers submit corrections through the Translation Master forms.

**Function endpoint:** `https://rdgtrans.netlify.app/.netlify/functions/submit-corrections`

**GitHub Action:** (Optional) Set up automated processing workflow

## Security

- Submission requires editor name and valid email
- All submissions are logged with timestamp
- Email addresses are stored for contact purposes only
- No authentication required (open community review model)

## Contact

For questions about submitted corrections, contact the editor via the email address in the metadata.

## Languages Supported

- Thai (ไทย)
- Japanese (日本語)
- Korean (한국어)
- Vietnamese (Tiếng Việt)
- Simplified Chinese (简体中文)
- Traditional Chinese (繁體中文)
