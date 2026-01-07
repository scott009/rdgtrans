# WORK ORDER

**ID:** wo-SSQS-v2-revision-001
**TYPE:** DOC_UPDATE
**TARGET:** dochome/SupervisorSessionQuickStart_v2.md
**GOAL:** Apply all revisions needed to align the document with Supervisor, Claude, and User consensus following initial review.

## CONDITIONS

- Do not change the document's intent or authority model.
- Modify only the .md file.
- No structural or filesystem side effects beyond this file.
- Produce clean, well-formatted Markdown.

## REQUIRED CHANGES

### 1. Fix all Markdown formatting issues
- Ensure bullet lists, numbered lists, and nested lists render correctly
- Add proper blank lines where needed
- Repair sections where items collapsed into single lines

### 2. Standardize placeholder syntax
Replace all angle-bracket placeholders `<like this>` with: `{placeholder_name}`

This includes:
- paths
- commit hashes
- timestamps
- all template variables

### 3. Clarify Git operations boundary
Revise Section 8 to state:
- Claude may perform read-only Git operations (git status, git log, git diff) at any time
- Claude must not perform write operations (git add, git commit, git push, git branch, git merge, etc.) without an explicit Work Order

### 4. Add a Conflict Resolution subsection (Section 5)
Add the following decision rules:

**CONFLICT RESOLUTION RULES**
1. If the conflict concerns paths, filesystem structure, or file timestamps → the filesystem is authoritative.
2. If the conflict concerns roles, responsibilities, or conceptual definitions → Supervisor memory is authoritative.
3. If the conflict concerns sharedContext.md → the version in dochome is authoritative over both Supervisor memory and filesystem copies.

### 5. Clarify "init script has run" semantics
Modify the text to specify:
- Claude must verify init script status using a session indicator (e.g., .last_init) or other environment-specific state markers
- "This session" refers to the active VS Code/WSL environment from which Claude is operating

### 6. Add Claude's Ready Acknowledgement Requirement
After Supervisor declares readiness, add:

Claude must respond: "Ready and awaiting Work Orders."

### 7. Clarify Advisory vs Work Order distinction
Add a subsection explaining:
- **Advisory:** Safe, non-binding informational output; may be issued at any time; no Work Order required.
- **Work Order:** Explicit authorization for Claude to perform actions that modify files or execute scripts.

### 8. Move Section 9 to a new Appendix
Rename it: **Appendix A — Document Verification Protocol**

Move the entire section there with minimal editing.

### 9. Add optional Copilot status to the State Report
Add the line under "Key Files":

`Copilot Init: Yes/No`

And note that this field is optional unless Supervisor requests it.

### 10. Add a short note at the end of the document
State:

**Note:** Future versions (v3) will include Session End protocol and Initialization Error Recovery procedures.

## OUTPUTS REQUIRED FROM CLAUDE

- Updated SupervisorSessionQuickStart_v2.md in full
- A brief summary listing which changes were made
- No other modifications or actions

## STATUS

**Issued:** 2025-12-10
**Executed by:** Claude Code
**Status:** ✅ Completed
**Approved by:** Supervisor, User

---

*END OF WORK ORDER wo-SSQS-v2-revision-001*
