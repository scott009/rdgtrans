# WO-PRESMASTER-ReadContainers-002

## SSQS v2 — Haiku-Safe Work Order

---

## 0. WORK ORDER HEADER

**Work Order ID:** WO-PRESMASTER-ReadContainers-002
**Title:** Complete screen_reader and print_master Container Specifications
**Date Issued:** 2025-12-29
**Supervisor:** User
**Priority:** High

**Summary:** Analyze existing screen reader and print master reference implementations, then complete their container specifications in presentation.json by adding structure, language configuration, assets, and validation rules for both read-only container types.

---

## 1. PURPOSE

Complete the specifications for screen_reader and print_master containers in presentation.json, upgrading them from status "planned" to fully specified container types. This will:
- Document the structure and assets for all read-only translation containers
- Enable systematic generation and maintenance of screen and print versions
- Complete presmaster specification coverage of existing containers
- Close the final gap for manifest creation prerequisites (per roadmap)

---

## 2. SCOPE & BOUNDARIES

### 2.1 Allowed Directories

- `/home/scott/gitrepos/rdgtrans/`
  *(Read and write: presentation.json)*

- `/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/`
  *(Read-only: screen_reader and print_master reference implementations)*

### 2.2 Forbidden Directories

- `/home/scott/gitrepos/rdgtrans/lmasters/` — content layer
- `/home/scott/gitrepos/rdgtrans/corrections/` — out of scope
- Any non-project directories

### 2.3 File Types in Scope

- **Read:** `rdgThai.html`, `rdgThaiPrint.html` (representative examples for analysis)
- **Read → Write:** `presentation.json`

---

## 3. EXECUTION MODEL (Sonnet / Haiku)

### 3.1 Sonnet Responsibilities

- Read and analyze screen_reader and print_master reference implementations
- Identify structural patterns, content organization, assets, and styling
- Determine differences between screen_reader and print_master containers
- Design complete specifications for both container types following tmaster/rdg_translations_portal models
- Generate JSON specifications with structure, language_config, assets, validation
- Validate specifications against existing implementations
- Supervise Haiku execution and validate results

### 3.2 Haiku Responsibilities

- Execute Sonnet's finalized plan
- Update screen_reader entry in presentation.json (locate by key name, not line number)
- Update print_master entry in presentation.json (locate by key name, not line number)
- Preserve exact JSON structure provided by Sonnet
- Maintain correct formatting and syntax
- Report completion or errors

### 3.3 Execution Rule

Sonnet analyzes, designs, and specifies.
Haiku executes file modifications exactly as specified.

---

## 4. TASK DESCRIPTION

### Deterministic Steps

1. **Read reference implementations:**
   - Screen reader: `/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/rdgThai.html`
   - Print master: `/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/rdgThaiPrint.html`

2. **Analyze and identify:**
   - HTML structure (chapters, paragraphs, ID tags)
   - CSS assets (external and embedded)
   - Print-specific styles (@media print)
   - Language-specific file patterns

3. **Design complete specifications** for both container types including:
   - `version`
   - `description`
   - `reference_implementation`
   - `specification` (future doc reference)
   - `structure` (sections, elements, content organization)
   - `language_config` (6 languages: Thai, Japanese, Korean, Simplified Chinese, Traditional Chinese, Vietnamese)
   - `assets` (CSS external and embedded, print styles for print_master)
   - `validation` rules

4. **Read current presmaster:**
   `/home/scott/gitrepos/rdgtrans/presentation.json`

5. **Update both container types:**
   - Replace screen_reader entry with complete specification (locate by key name)
   - Replace print_master entry with complete specification (locate by key name)

6. **Write updated presentation.json**

7. **Validate:**
   - JSON syntax correctness
   - Structural consistency with tmaster and rdg_translations_portal patterns
   - Full coverage of container features

---

## 5. METADATA FOR EXECUTION

### Reference Implementations

**Screen Reader:**
- **Files:** rdgThai.html, rdgJapanese.html, rdgKorean.html, rdgSimplifiedChinese.html, rdgTraditionalChinese.html, rdgVietnamese.html
- **Path:** `/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/`
- **Representative:** rdgThai.html (analyzed)

**Print Master:**
- **Files:** rdgThaiPrint.html, rdgJapanesePrint.html, rdgKoreanPrint.html, rdgSimplifiedChinesePrint.html, rdgTraditionalChinesePrint.html, rdgVietnamesePrint.html
- **Path:** `/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/`
- **Representative:** rdgThaiPrint.html (analyzed)

### Target File

- **File:** `presentation.json`
- **Path:** `/home/scott/gitrepos/rdgtrans/presentation.json`
- **Current Version:** 3.0.0 (no version bump for this Work Order)

### Structural Analysis

**Both Containers Share:**
- Chapter/paragraph structure with ID tags (h2.chaptermain, h3.id-tag, p elements)
- External CSS: ada3.css
- 6 language versions each
- Read-only content presentation

**Print Master Additions:**
- Embedded @media print styles (~90 lines)
- Page size control (letter)
- Facing pages (different margins for left/right)
- Page break control (chapters start on right pages, avoid orphans/widows)
- Print-optimized spacing and typography
- Version notice styling

### Assets

**screen_reader:**
- External CSS: ada3.css

**print_master:**
- External CSS: ada3.css
- Embedded CSS: @media print styles block

### Language Configuration (Both)

6 languages with file naming pattern:
- Thai: code "th", files: rdgThai.html / rdgThaiPrint.html
- Japanese: code "ja", files: rdgJapanese.html / rdgJapanesePrint.html
- Korean: code "ko", files: rdgKorean.html / rdgKoreanPrint.html
- Simplified Chinese: code "zh-CN", files: rdgSimplifiedChinese.html / rdgSimplifiedChinesePrint.html
- Traditional Chinese: code "zh-TW", files: rdgTraditionalChinese.html / rdgTraditionalChinesePrint.html
- Vietnamese: code "vi", files: rdgVietnamese.html / rdgVietnamesePrint.html

---

## 6. PLAN OF EXECUTION

*To be generated by Sonnet during validation and handed to Haiku for execution.*

---

## 7. EXECUTION

*Haiku will execute exactly as planned by Sonnet.*

---

## 8. ERROR HANDLING & ESCALATION

### Haiku Must Halt If:

- `presentation.json` has unexpected structure changes since last read
- JSON syntax errors occur during edit
- File write fails

### Haiku Must Report:

- Exact error message
- File state at time of error
- Last successful operation completed

### Sonnet Resolution:

- Validate Work Order assumptions
- Adjust plan if needed
- Re-execute or escalate to user

---

## 9. DELIVERABLES

1. **Updated presentation.json** with complete screen_reader specification
2. **Updated presentation.json** with complete print_master specification
3. **Validation confirmation** that JSON is syntactically correct
4. **Structure summaries** for both container types

---

## 10. ACCEPTANCE CRITERIA

✅ screen_reader entry includes: `version`, `description`, `reference_implementation`, `structure`, `language_config`, `assets`, `validation`
✅ print_master entry includes: `version`, `description`, `reference_implementation`, `structure`, `language_config`, `assets`, `validation`
✅ Both entries have status upgraded from "planned" to fully specified (remove status field)
✅ Structure sections capture content organization (chapters, paragraphs, ID tags)
✅ Language configs define all 6 languages with correct file names
✅ Assets define external CSS (both) and embedded print styles (print_master only)
✅ JSON syntax is valid (file can be parsed without errors)
✅ Specifications follow tmaster/rdg_translations_portal pattern for consistency
✅ No modifications to existing container_types entries (tmaster, rdg_translations_portal)
✅ File version metadata remains at 3.0.0 (no version bump)

---

## 11. NOTES & SPECIAL INSTRUCTIONS

### Structural Similarity

screen_reader and print_master share identical HTML content structure. The primary difference is print_master includes embedded @media print styles for PDF optimization.

### Print Styles Detail

The print_master embedded styles include:
- @page rules for size (letter) and margins (facing pages)
- Orphan/widow control
- Page-break rules (chapters start on right pages)
- Print-optimized spacing
- Link styling removal for print
- ID tag visibility in print

### Language Configuration Pattern

Both containers follow the same language configuration pattern used in tmaster, with 6 languages. File naming convention:
- Screen: `rdg{Language}.html`
- Print: `rdg{Language}Print.html`

### Reference Pattern

Use tmaster and rdg_translations_portal specifications as structural models for consistency.

### Key Lookup (Not Line Numbers)

Haiku must locate container entries by key name (`screen_reader`, `print_master`) within the `container_types` object, not by fixed line numbers. Line number references in this Work Order are informational only.

---

## 12. END OF WORK ORDER
