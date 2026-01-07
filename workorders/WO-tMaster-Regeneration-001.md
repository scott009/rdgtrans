# Work Order: Regenerate Incomplete tMaster Files to v2.0 Spec
Work Order ID: WO-tMaster-Regeneration-001
Title: Regenerate Korean, Chinese, and Vietnamese tMaster Files Using v2.0 Container Spec
Date Issued: 2025-12-11
Supervisor: Scott Tobias
Priority: High

## Summary
This Work Order regenerates the four incomplete v1.0 tMaster HTML files (Korean, Simplified Chinese, Traditional Chinese, Vietnamese) so they conform fully to the **tMaster v2.0 container specification**, using the **Thai** and **Japanese** tMaster files as structural reference models.

All five non-Thai languages will ultimately match the v2.0 structure used by `tmasterThai.html` and the corrected `tmasterJapanese.html`.

All target files are located in the same directory as the Japanese file:

```
/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/
```

`tmasterThai.html` and `tmasterJapanese.html` must be treated as **read-only** and used only as references.

---

## 1. PURPOSE

- Replace the remaining four v1.0-style tMaster HTML files with fully v2.0-compliant versions.  
- Ensure each regenerated file:
  - uses the v2.0 container structure defined in `tmaster_container_spec.md`
  - matches the high-level structure of `tmasterThai.html` and `tmasterJapanese.html`
  - preserves the existing localized content (i.e., text in Korean/Chinese/Vietnamese) as much as possible
  - includes all required metadata, sections, and attributes (pr-id, data-original, etc.)
- Leave Thai and Japanese files unchanged.

This Work Order is **structural and generative**, not just a small patch.

---

## 2. SCOPE & BOUNDARIES

### 2.1 Allowed Directories (read/write)

Sonnet/Haiku may read from and write to:

```
/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/
/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/specs/   (if needed for tmaster_container_spec.md)
/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/tmasters/ (if this subdirectory exists)
/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/*.html
supervisor_updates/WO-tMaster-Regeneration-001/
```

### 2.2 Forbidden Directories (no read/write)

No operations may occur in:

```
showoff/archive/
workorders/
translations/
src/
dist/
assets/
any .git/ directory
```

### 2.3 Files Allowed to Be Modified

Exactly **four** files may be modified by this Work Order:

- The four non-Thai, non-Japanese tMaster files located in:

  ```
  /mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/
  ```

These must be discovered by pattern and filtered as:

- Filenames matching `tmaster*.html`
- EXCLUDING:
  - `tmasterThai.html`
  - `tmasterJapanese.html`
- The set of remaining files MUST contain exactly four entries (Korean, Chinese (2), Vietnamese).
- If the resulting set is not exactly four files, Haiku must halt and report an error.

### 2.4 Files Explicitly Protected (read-only)

These files must not be modified:

- `tmasterThai.html`
- `tmasterJapanese.html`
- Any file outside the four discovered targets

---

## 3. EXECUTION MODEL (Sonnet / Haiku)

### 3.1 Sonnet Responsibilities

Sonnet must:

1. Interpret this Work Order under SSQS v2 governance.  
2. Discover the four target files via:
   - listing all `tmaster*.html` in the docs directory
   - excluding `tmasterThai.html` and `tmasterJapanese.html`
   - ensuring exactly four remain
3. Load:
   - `tmasterThai.html` (reference model 1)
   - `tmasterJapanese.html` (reference model 2)
   - `tmaster_container_spec.md` (v2.0 spec, if available)
4. For each of the four target files:
   - Parse the existing HTML
   - Extract and preserve language-specific content (paragraphs, headings, etc.) as far as possible
   - Design a regenerated v2.0 container structure that:
     - matches Thai/Japanese structure
     - includes all required sections (reviewers, metadata, version info, language toggle, etc.)
     - assigns or preserves pr-id and data-original attributes
5. Generate a deterministic plan for:
   - backing up the original file
   - writing the regenerated file
   - producing a per-file diff or summary for the Supervisor
6. Ensure no proposed modifications target Thai/Japanese files or any files outside the four discovered targets.

### 3.2 Haiku Responsibilities

Haiku must:

- Execute file operations exactly as planned by Sonnet.  
- For each of the four target files:
  1. Create a backup in:
     ```
     supervisor_updates/WO-tMaster-Regeneration-001/backups/<filename>
     ```
  2. Write the regenerated v2.0-compliant HTML to the original filepath.
  3. Optionally generate a diff or summary file in:
     ```
     supervisor_updates/WO-tMaster-Regeneration-001/diffs/<filename>.diff
     ```
- Ensure that:
  - No writes occur to Thai or Japanese files.
  - No writes occur outside the four target files and the supervisor_updates area.

### 3.3 Execution Rule

**Sonnet plans; Haiku executes.**  
If Haiku detects any attempt to modify more than four files, or to touch Thai/Japanese, it must halt and report the error.

---

## 4. TASK DESCRIPTION

For each of the four target languages (Korean, Simplified Chinese, Traditional Chinese, Vietnamese):

1. **Analyze current file**  
   - Note that it is currently in v1.0 container format.
   - Identify existing content blocks (sections of translated text).

2. **Define the v2.0 structure**  
   - Use `tmasterThai.html` and `tmasterJapanese.html` as structural templates.
   - Ensure the following are present (non-exhaustive list, Sonnet to refine using spec):
     - top-level metadata/header block
     - title and subtitle container
     - language toggle controls
     - translation content sections with pr-id attributes
     - data-original attributes (if applicable in spec)
     - reviewer/translation notes section
     - version history or modification tracking region

3. **Regenerate HTML**  
   - Construct a new HTML document using the v2.0 structure.
   - Map the existing language content into the correct pr-id slots.
   - Where content is missing, leave clearly marked placeholders (e.g., HTML comments), but do not invent new translated text.

4. **Backup & Replace**  
   - Save the original v1.0 file to:
     ```
     supervisor_updates/WO-tMaster-Regeneration-001/backups/<filename>
     ```
   - Overwrite the original path in `.../output_V1/docs/` with the regenerated v2.0 HTML.

5. **Reporting**  
   - For each file, produce a short report section summarizing:
     - file path
     - whether regeneration succeeded
     - any sections where content could not be mapped and placeholders were inserted

---

## 5. METADATA FOR EXECUTION

### 5.1 Discovery Logic

- Use deterministic logic to gather:
  - `tmaster*.html` in `/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/`
  - Filter out:
    - `tmasterThai.html`
    - `tmasterJapanese.html`
  - Confirm that there are exactly four remaining files.

If this condition fails → Haiku must halt and return an error to Sonnet.

### 5.2 Reference Materials

- `tmasterThai.html` — primary v2.0 reference
- `tmasterJapanese.html` — secondary v2.0 reference
- `tmaster_container_spec.md` — specification document (if available under docs/specs or equivalent directory already known from the project)

### 5.3 Output Location

All Work Order artifacts must be written under:

```
supervisor_updates/WO-tMaster-Regeneration-001/
```

Expected subdirectories:

- `backups/` — original pre-regeneration versions  
- `diffs/` — optional per-file diffs  
- `reports/` — regeneration summary, e.g., `RegenerationSummary.md`

---

## 6. PLAN OF EXECUTION (Generated by Sonnet)

Sonnet must produce and document a plan that includes:

1. The exact list of four target filenames.  
2. A per-file transformation strategy.  
3. A description of how content will be mapped into v2.0 containers.  
4. A fallback strategy if unexpected HTML patterns are present.  
5. Confirmation that Thai/Japanese are excluded from modification.

This plan may be written into `RegenerationSummary.md` or logged in the session transcript.

---

## 7. EXECUTION (Performed by Haiku)

Haiku must:

- Perform backups.  
- Overwrite the four target files with regenerated versions.  
- Generate the summary report and any diffs.  

Haiku must not:

- Modify Thai/Japanese tMasters.  
- Modify any additional files.  
- Write outside supervisor_updates and the four target file paths.

---

## 8. ERROR HANDLING & ESCALATION

### 8.1 Haiku

Haiku must halt and report an error if:

- The number of target files (excluding Thai/Japanese) is not exactly four.  
- Any attempt is made to modify a protected file.  
- File operations fail (permissions, missing files, etc.).  

### 8.2 Sonnet

Sonnet must:

- Analyze the error.  
- If necessary, request clarification from the Supervisor (e.g., new filenames or paths).  
- Regenerate a safe plan that adheres to all constraints.

---

## 9. DELIVERABLES

Under `supervisor_updates/WO-tMaster-Regeneration-001/`:

- `backups/<filename>` for each of the four original v1.0 files.  
- Regenerated v2.0 tMaster HTML files in their original locations.  
- `RegenerationSummary.md` summarizing:
  - list of target files
  - per-file status (success/failure)
  - mapping/placeholder notes  
- Optional: `diffs/<filename>.diff` for human inspection.

---

## 10. ACCEPTANCE CRITERIA

- Exactly four non-Thai, non-Japanese tMaster files are regenerated.  
- Each regenerated file follows the v2.0 tMaster container structure.  
- Thai and Japanese files remain unchanged.  
- Original v1.0 files are safely backed up in `supervisor_updates/`.  
- RegenerationSummary.md clearly documents what was done.  
- No unauthorized files were modified.  
- All operations are SSQS v2-compliant.

---

## 11. NOTES & SPECIAL INSTRUCTIONS

- This Work Order is the main “heavy lift” for normalizing tMaster containers.  
- After completion, a subsequent Work Order (e.g., `WO-tMaster-LangFix-001`) may perform global lang-attribute and toggle-label sanity checks.  
- No changes are to be made to `.gitignore` or archive directories in this Work Order.

---

## 12. END OF WORK ORDER
