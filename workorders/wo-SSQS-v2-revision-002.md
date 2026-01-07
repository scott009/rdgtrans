# WORK ORDER

**ID:** wo-SSQS-v2-revision-002
**TYPE:** DOC_UPDATE
**TARGET:** dochome/SupervisorSessionQuickStart_v2.md
**GOAL:** Apply revisions based on post-review advisories regarding Executive role, model selection, Appendix generalization, sync staging workflow, and Work Order storage semantics.

## CONDITIONS

- Modify only this .md file.
- Maintain all existing content unless directly revised.
- Produce clean, readable Markdown.
- No other filesystem changes.

## REQUIRED CHANGES

### 1. Add Executive Role (User) as Section 1.0

Insert the following text before Section 1.1:

```markdown
### 1.0 Executive (User)
- Holds ultimate authority over all decisions and operations.
- Delegates orchestration to Supervisor.
- Bridges structured memory (Supervisor) and real filesystem state (Claude) by reviewing and dragging required files into the Supervisor interface.
- May override Supervisor or agent decisions when required.
- Ensures alignment across agents and resolves conflicts.
- Initiates sessions and approves major workflow transitions.
```

### 2. Add Model Selection Subsection to Section 7

Append this as Section 7.3:

```markdown
### 7.3 Model Selection (Advisory)

Claude may recommend a preferred model (e.g., sonnet, haiku, opus) for a Work Order based on computational complexity, cost, or operational efficiency.

Supervisor Responsibilities:
- Determine whether a task should be executed by spawning a separate Task using the recommended model.
- Model selection occurs at the Task level; Supervisor cannot switch the active Claude model mid-session.

Notes:
- Architecture and design Work Orders should typically use Sonnet or Opus.
- Routine or low-complexity edits may be delegated to Haiku via Task spawning.
- Model recommendations do not authorize actions; they are advisory only.
```

### 3. Add Work Order Storage & Versioning as Section 7.4

Append this immediately after Section 7.3:

```markdown
### 7.4 Work Order Storage & Versioning

All Work Orders must be stored in the repository at:

{projhome}/workorders/

Each Work Order is saved as a standalone Markdown file named:

wo-{short_description}-{sequence}.md

Examples:
- wo-SSQS-v2-revision-002.md
- wo-context-update-042.md

Versioning Rules:
- All Work Orders must be committed to Git to preserve an authoritative audit trail.
- Work Orders document why changes were made, not just how.
- Only Work Orders that define or modify system protocols need to be synchronized to Supervisor memory.
- Routine operational Work Orders do not require Supervisor sync unless they modify Supervisor-facing behavior or contracts.
```

### 4. Generalize Appendix A

Replace the first line of Appendix A with:

"This appendix defines the general protocol for iterative review, verification, and refinement of any operational or architectural document within the RDG Translations system."

### 5. Add Synchronization Staging Workflow to Appendix A

Append this to the end of Appendix A:

```markdown
### Synchronization Workflow for Supervisor Memory

To ensure structured memory remains aligned with the real filesystem, all files modified via Work Order are copied by Claude into a staging directory.

Location:
{dochome}/supervisor_updates/

Contents:
- Copies of changed files requiring Supervisor sync
- SYNC_MANIFEST.md describing:
  - filename
  - change type
  - timestamp
  - reason for change
  - priority (CRITICAL, IMPORTANT, ROUTINE)

Claude Responsibilities:
- Automatically populate the staging directory after any file modification.
- Update SYNC_MANIFEST.md with detailed change records.
- Maintain a .last_sync timestamp file recording the last confirmed synchronization.
- Clear the staging directory once Supervisor confirms sync completion.

Supervisor Workflow:
1. Review SYNC_MANIFEST.md.
2. Drag listed files into Supervisor interface for memory refresh.
3. Notify Claude: "Sync complete."
```

## REQUIRED OUTPUTS FROM CLAUDE

- Updated SupervisorSessionQuickStart_v2.md containing all changes.
- A brief summary of modifications.
- No additional side effects.

## STATUS

**Issued:** 2025-12-10
**Executed by:** Claude Code
**Status:** ✅ Completed
**Approved by:** Supervisor, User

---

*END OF WORK ORDER wo-SSQS-v2-revision-002*
