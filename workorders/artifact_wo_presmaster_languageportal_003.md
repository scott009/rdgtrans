# WO-PRESMASTER-LanguagePortal-003

## SSQS v2 — Haiku-Safe Work Order

---

## 0. WORK ORDER HEADER

**Work Order ID:** WO-PRESMASTER-LanguagePortal-003
**Title:** Specify LanguagePortal Container in presentation.json
**Date Issued:** 2025-12-29
**Supervisor:** User
**Priority:** High

**Summary:** Design and specify LanguagePortal container type in presentation.json - a single-language filtered portal derived from rdg_translations_portal structure, enabling focused presentation for language-specific collaborators and partners.

---

## 1. PURPOSE

Add a complete specification for the LanguagePortal container to presentation.json, defining a new container type for single-language focused portals. This will:
- Enable language-specific collaboration with focused, respectful presentation
- Support real-world use cases (Thai consulate contact, Japanese partners, etc.)
- Provide filtered view showing only one language's resources
- Derive from rdg_translations_portal structure for consistency
- Complete presmaster specification for all currently approved and implementable container types

---

## 2. SCOPE & BOUNDARIES

### 2.1 Allowed Directories

- `/home/scott/gitrepos/rdgtrans/`
  *(Read and write: presentation.json)*

### 2.2 Forbidden Directories

- `/home/scott/gitrepos/rdgtrans/lmasters/` — content layer
- `/home/scott/gitrepos/rdgtrans/corrections/` — out of scope
- Any non-project directories

### 2.3 File Types in Scope

- **Read → Write:** `presentation.json`

---

## 3. EXECUTION MODEL (Sonnet / Haiku)

### 3.1 Sonnet Responsibilities

- Analyze rdg_translations_portal specification as foundation
- Design LanguagePortal as filtered, single-language derivative
- Determine structure: sections, elements, language filtering approach
- Define language configuration for 6 portal instances (one per language)
- Specify assets and validation rules
- Generate complete JSON specification following established patterns
- Supervise Haiku execution and validate results

### 3.2 Haiku Responsibilities

- Execute Sonnet's finalized plan
- Add language_portal entry to presentation.json container_types
- Preserve exact JSON structure provided by Sonnet
- Maintain correct formatting and syntax
- Report completion or errors

### 3.3 Execution Rule

Sonnet analyzes, designs, and specifies.
Haiku executes file modification exactly as specified.

---

## 4. TASK DESCRIPTION

### Deterministic Steps

1. **Read current presmaster:**
   `/home/scott/gitrepos/rdgtrans/presentation.json`

2. **Review rdg_translations_portal specification** (lines 631-719) to understand base structure

3. **Design LanguagePortal specification** including:
   - `version`
   - `description`
   - `reference_implementation` (future reference file)
   - `specification` (future doc reference)
   - `structure` (filtered sections: about, english_source, language_audio, language_tmaster, language_print, participation, contact)
   - `language_config` (6 language instances: Thai, Japanese, Korean, Simplified Chinese, Traditional Chinese, Vietnamese)
   - `assets` (CSS, structure)
   - `validation` rules

4. **Add new container type:**
   Insert `language_portal` entry into container_types object (locate by key, not line number)

5. **Write updated presentation.json**

6. **Validate:**
   - JSON syntax correctness
   - Structural consistency with other containers
   - Language configuration completeness

---

## 5. METADATA FOR EXECUTION

### Target File

- **File:** `presentation.json`
- **Path:** `/home/scott/gitrepos/rdgtrans/presentation.json`
- **Current Version:** 3.0.0 (no version bump for this Work Order)

### Base Container for Derivation

- **rdg_translations_portal** (WO-1 deliverable)
- Structure includes: header, about_project, english_source, audio_introductions, translation_masters, print_masters, participation, contact

### LanguagePortal Concept

**Filters rdg_translations_portal to single language:**
- Retains: header, about_project, english_source (reference), participation, contact
- Filters: audio_introductions → single language audio
- Filters: translation_masters → single language tmaster link
- Filters: print_masters → single language print link
- Removes: multi-language navigation elements

**File Naming Pattern (proposed):**
- Thai: rdgThaiPortal.html
- Japanese: rdgJapanesePortal.html
- Korean: rdgKoreanPortal.html
- Simplified Chinese: rdgSimplifiedChinesePortal.html
- Traditional Chinese: rdgTraditionalChinesePortal.html
- Vietnamese: rdgVietnamesePortal.html

### Real-World Use Case

**Example:** Thai Language Portal for Thai consulate contact
- Shows: Thai-specific resources only
- Message: "We are honored to bring Recovery Dharma to Thailand"
- Demonstrates: Serious, focused commitment to Thai language community
- Cultural impact: Respectful presentation, not "find your language in this list"

### Assets

- External CSS: ada3.css (same as rdg_translations_portal)
- Structure: Filtered/simplified navigation

### Language Configuration

6 language portal instances, each configured for one target language

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

1. **Updated presentation.json** with new `language_portal` container_types entry
2. **Validation confirmation** that JSON is syntactically correct
3. **Structure summary** showing filtered sections and language configuration

---

## 10. ACCEPTANCE CRITERIA

✅ `presentation.json` contains new `language_portal` entry in `container_types`
✅ Entry includes: `version`, `description`, `reference_implementation`, `structure`, `language_config`, `assets`, `validation`
✅ Structure captures filtered single-language portal sections
✅ Language configs define all 6 language portal instances with correct file names
✅ Structure clearly derives from rdg_translations_portal with appropriate filtering
✅ JSON syntax is valid (file can be parsed without errors)
✅ Specification follows established container pattern for consistency
✅ No modifications to existing container_types entries
✅ File version metadata remains at 3.0.0 (no version bump)

---

## 11. NOTES & SPECIAL INSTRUCTIONS

### Derivation from rdg_translations_portal

LanguagePortal is conceptually a "filter" applied to rdg_translations_portal:
- Takes multi-language portal structure
- Removes multi-language navigation
- Retains only one language's resources
- Maintains same sectional organization

### Single-Language Focus

Each language portal instance presents:
- About section (may be translated or remain in English)
- English source link (for bilingual reference)
- ONE audio introduction (target language only)
- ONE translation master link (target language only)
- ONE print master link (target language only)
- Participation section
- Contact section

### Cultural/Diplomatic Value

LanguagePortal demonstrates respect and commitment to specific language communities:
- Thai portal for Thai partners shows Thai-specific focus
- Japanese portal for Japanese collaborators shows Japanese-specific commitment
- Not "here's everything, find your language" but "this is FOR Thailand"

### Reference Pattern

Use rdg_translations_portal (WO-1) and other container specifications as structural models.

### Future Implementation

This specification defines the container type. Actual HTML files (rdgThaiPortal.html, etc.) will be generated later based on this specification.

### Key Lookup

Haiku must locate container entry by key name (`language_portal`) within the `container_types` object, not by fixed line numbers.

---

## 12. END OF WORK ORDER
