# Work Order: SSQS v2 --- Revision 004

**Filename:** wo-SSQS-v2-revision-004.md\
**Version:** 2.0\
**Revision:** 004\
**Date Issued:** 2025-12-10\
**Issued By:** Supervisor (ChatGPT)\
**Target Agent:** Claude (Architect / Executor)\
**Status:** Approved for execution

------------------------------------------------------------------------

## 1. PURPOSE

Safely update `sharedContext.md` to formally introduce the `wohome`
shortcut, following OPSEC rules.\
All modifications must be **minimal**, **surgical**, and **limited
strictly** to inserting the approved definition block.

This Work Order must NOT restructure or alter any other part of the
file.

Additionally, Claude must produce a **Supervisor Review Copy** in the
`supervisor_updates` directory for human approval before replacing the
authoritative version.

------------------------------------------------------------------------

## 2. REQUIRED ACTIONS

### 2.1 Load Current sharedContext.md

-   Read the authoritative file from:

        {dochome}/sharedContext.md

-   Validate that it matches the last loaded version (v1.2 unless
    updated).

### 2.2 Insert New Shortcut Definition

Insert the following block immediately after the existing path
definitions (e.g., after projhome, dochome, or equivalent section):

    - **wohome**: ${projhome}/workorders  
      The canonical location for all Work Orders.  
      AI agents MUST NOT write or read Work Orders outside this directory.  
      All Work Orders MUST use the naming pattern:  
      `wo-<system>-v<version>-revision-<n>.md`

Rules: - Insert exactly as written. - Do not modify surrounding lines. -
Do not reflow or reformat unrelated content.

### 2.3 Write Supervisor Review Copy

Save the updated file to:

    {dochome}/supervisor_updates/sharedContext_v1.3_candidate.md

Requirements: - Include ONLY the added insertion block as the
difference. - Must not overwrite the authoritative sharedContext.md. -
File naming must reflect the next sequential document version.

### 2.4 Produce Supervisor Diff Report

Save a structured diff report to:

    {dochome}/Reports/sharedContext_update_report_004.md

Report must include: - Before → After diff (minimal and
human-readable) - Description of the modification - Statement of OPSEC
compliance - Confirmation that no other content was changed - A one‑line
Approval Request notice

### 2.5 Logging

Append an execution log entry to:

    {projhome}/logs/wo-SSQS-v2-revision-004.log

Log must include: - Timestamps - Summary of actions taken - Confirmation
of compliance with OPSEC - Any warnings or anomalies

------------------------------------------------------------------------

## 3. OUTPUTS REQUIRED

Claude must generate:

1.  `sharedContext_v1.3_candidate.md` in supervisor_updates\
2.  `sharedContext_update_report_004.md` in Reports\
3.  Updated log file in projhome/logs\
4.  A confirmation message summarizing execution

------------------------------------------------------------------------

## 4. COMPLETION CRITERIA

This Work Order is complete when: - The candidate updated sharedContext
copy exists - A diff report is present in Reports - Supervisor receives
a completion confirmation - No OPSEC violations occurred

------------------------------------------------------------------------

## 5. NOTES

Supervisor approval is required before the updated sharedContext becomes
authoritative.\
After approval, a future Work Order (005) will promote the candidate to
the live version.

**END OF WORK ORDER**
