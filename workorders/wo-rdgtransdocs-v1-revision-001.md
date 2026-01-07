# Work Order: wo-rdgtransdocs-v1-revision-001

## System
rdgtransdocs

## Purpose
Create the initial directory structure required to support the Gemini initialization workflow.

This work order authorizes **directory creation only**. No manifest content is to be added at this stage.

## Scope
Repository: rdgtransdocs  
Branch: main  

## Authorized Actions
1. Create a new directory named `InitGemini` at the repository root.
2. Add a placeholder file (`.gitkeep`) inside `InitGemini` so the directory is tracked by git.
3. Commit the change to the `main` branch.

## Explicit Constraints
- Do NOT add `manifest.md` yet.
- Do NOT modify any existing files.
- Do NOT refactor, rename, or relocate any directories.
- Do NOT interpret this work order beyond the listed steps.

## Commit Requirements
- Single commit only.
- Commit message must be exactly:
  ```
  Add InitGemini directory for Gemini init conventions
  ```

## Validation Criteria
This work order is complete when:
- The `InitGemini/` directory exists at the root of `rdgtransdocs`.
- The directory is tracked in git via `.gitkeep`.
- No other repository changes are present.

## Notes
This work order establishes filesystem structure only.  
A subsequent work order will introduce `InitGemini/manifest.md`.
