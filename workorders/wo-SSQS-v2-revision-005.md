# Work Order: SSQS v2 --- Revision 005

**Filename:** wo-SSQS-v2-revision-005.md\
**Version:** 2.0\
**Revision:** 005\
**Date Issued:** 2025-12-10\
**Issued By:** Supervisor (ChatGPT)\
**Target Agent:** Claude (Architect / Executor)\
**Status:** Approved for execution

------------------------------------------------------------------------

## 1. PURPOSE

Promote the updated shared context specification from candidate status
to the authoritative version.\
This Work Order promotes:

    {dochome}/supervisor_updates/sharedContext_v1.3_candidate.md

to:

    {dochome}/sharedContext.md

This action finalizes the addition of the `wohome` shortcut and brings
the system contract to version **v1.3**.

------------------------------------------------------------------------

## 2. REQUIRED ACTIONS

### 2.1 Load Candidate File

Load the file:

    {dochome}/supervisor_updates/sharedContext_v1.3_candidate.md

Validate that: - The file exists\
- The only modification is the insertion of the `wohome` block\
- The OPSEC header remains untouched\
- No other structural or semantic changes are present

If anything is inconsistent, STOP and issue a warning.

------------------------------------------------------------------------

### 2.2 Promote Candidate to Authoritative

Copy the validated candidate file to:

    {dochome}/sharedContext.md

Rules: - Overwrite the existing authoritative file - Preserve encoding
and formatting exactly - No additional modifications may be made

------------------------------------------------------------------------

### 2.3 Update Version Label

If the document contains an internal version tag (e.g., v1.2), update it
to:

    v1.3, 2025-12-10

Do not modify anything except the version/date line.

------------------------------------------------------------------------

### 2.4 Post-Promotion Validation

Reload the newly authoritative sharedContext and verify:

-   All required paths exist (projhome, dochome, wohome, etc.)
-   No corruption or truncation occurred during promotion
-   OPSEC header remains intact
-   JSON/YAML/Markdown syntax (if present) is still valid
-   MCP agents can resolve paths without warnings

If validation fails, revert promotion and notify Supervisor.

------------------------------------------------------------------------

### 2.5 Produce Promotion Report

Save a structured promotion report to:

    {dochome}/Reports/sharedContext_promotion_005.md

Report must include: - Confirmation of successful promotion\
- Version label before → after\
- A line-by-line diff of changes\
- Validation results\
- Statement of OPSEC compliance

------------------------------------------------------------------------

### 2.6 Logging

Append an execution log entry to:

    {projhome}/logs/wo-SSQS-v2-revision-005.log

Log must include: - Timestamp - Steps executed - File checksums
before/after promotion - Any warnings or anomalies - Confirmation of
success

------------------------------------------------------------------------

## 3. OUTPUTS REQUIRED

Claude must generate:

1.  Updated authoritative sharedContext.md\
2.  Promotion report in `Reports/`\
3.  Log file update in `logs/`\
4.  Supervisor-facing confirmation message

------------------------------------------------------------------------

## 4. COMPLETION CRITERIA

This Work Order is complete when:

-   sharedContext.md is promoted to v1.3\
-   Validation report and log file exist\
-   Supervisor receives a completion confirmation

------------------------------------------------------------------------

## 5. NOTES

After this promotion, all MCP agents MUST treat sharedContext.md v1.3 as
the single authoritative contract.\
Future changes require new Work Orders.

**END OF WORK ORDER**
