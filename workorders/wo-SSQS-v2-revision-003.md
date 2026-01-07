# Work Order: SSQS v2 --- Revision 003

**Filename:** wo-SSQS-v2-revision-003.md\
**Version:** 2.0\
**Revision:** 003\
**Date Issued:** 2025-12-10\
**Issued By:** Supervisor (ChatGPT)\
**Target Agent:** Claude (Architect / Executor)\
**Status:** Approved for execution

------------------------------------------------------------------------

## 1. PURPOSE

Transition the system from **Observation Mode** into **Active Test Phase
1** by:

-   Validating that previous Work Orders (001 and 002) have been
    completed\
-   Ensuring the environment is consistent with sharedContext.md\
-   Verifying directory structure, master files, and Git status\
-   Generating the missing init timestamp file\
-   Producing a Session Readiness Report suitable for supervisor-level
    review

This Work Order represents the **formal start of testing** for SSQS v2.

------------------------------------------------------------------------

## 2. REQUIRED ACTIONS

### 2.1 Confirm Prior Work Orders

-   Confirm revision 001 and revision 002 have been executed.\
-   Summarize what was done and whether any follow-up tasks remain.

### 2.2 Validate Environment State

Using the rules in `sharedContext.md`:

-   Confirm that:
    -   `projhome` is correctly set\
    -   `dochome` is correctly set\
    -   `presentation.json` and `workmaster.json` are readable\
    -   All required context files were loaded\
-   Identify any mismatches or inconsistencies.

### 2.3 Generate Init Timestamp File

Because no `.last_init` file exists:

-   Create a new timestamp file at:

        {projhome}/.last_init

-   Timestamp format: ISO 8601, local timezone (EST).\

-   If the timestamp directory or file is missing, create it
    automatically.

### 2.4 Session Readiness Verification

Produce a *Supervisor-facing Readiness Report* that includes:

1.  Confirmation of the above tasks\
2.  Any remaining blockers for Phase 1 testing\
3.  Warnings or optional improvements\
4.  Recommended next Work Order (Revision 004)\
5.  A one-line "GO / NO-GO" status

Place this report at:

    {dochome}/Reports/ReadinessReport_003.md

If the Reports directory does not exist, create it.

### 2.5 Logging

Write an execution log to:

    {projhome}/logs/wo-SSQS-v2-revision-003.log

-   If `logs/` does not exist, create it.\
-   Include timestamps for each step.

------------------------------------------------------------------------

## 3. OUTPUTS REQUIRED

Claude must produce:

-   A confirmation message to the Supervisor summarizing execution\
-   A written ReadinessReport_003.md\
-   A `.last_init` timestamp file\
-   A `.log` file describing steps taken

------------------------------------------------------------------------

## 4. COMPLETION CRITERIA

This Work Order is complete when:

-   All required actions above are completed\
-   The Readiness Report is present in `{dochome}/Reports`\
-   Supervisor is presented with a "GO / NO-GO" result

------------------------------------------------------------------------

## 5. NOTES

This Work Order begins **System Test Phase 1**.\
Future Work Orders (004+) will cover:

-   Dry-run processing of masters\
-   Controlled updates to presentation.json\
-   Testing the Copilot execution layer\
-   Full pipeline test across Claude + Copilot + GitHub integration

------------------------------------------------------------------------

**END OF WORK ORDER**
