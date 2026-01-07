#!/bin/bash

################################################################################
# T-Spec Bandy/Lock Workflow Script
################################################################################
#
# Purpose:
#   Operationalizes the bandy → revise → lock workflow for T-spec documents.
#   Generates draft filenames, emits Claude review instructions, manages
#   version bumping, and supports final LOCK renaming.
#
# What It Does:
#   1. Creates standardized T-spec filenames
#   2. Prints copy-paste-ready Claude bandy instructions
#   3. Pauses for human feedback and decision input
#   4. Tracks version iterations (v_1_0, v_1_1, v_1_2, etc.)
#   5. RENAMES files to LOCKED status on human confirmation
#
# What It Does NOT Do:
#   - Parse Claude output or perform semantic analysis
#   - Automate decision-making
#   - Call external APIs
#   - Delete files
#   - Create directories
#   - CREATE spec content files (must be created manually before running)
#
# IMPORTANT: Draft .md files must exist before running this script.
# The script manages workflow, not file creation.
#
# Usage:
#   ./bandy_lock.sh <TRANSFORMATION_ID> <SHORT_NAME> [VERSION] [WORKDIR]
#
# Examples:
#   ./bandy_lock.sh T5 container_split
#   ./bandy_lock.sh T5 container_split v_1_0
#   ./bandy_lock.sh T5 container_split v_1_0 /path/to/workingfiles
#
################################################################################

set -euo pipefail

# Color codes for readability
BOLD='\033[1m'
RESET='\033[0m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'

################################################################################
# Input validation and configuration
################################################################################

if [[ $# -lt 2 ]]; then
    cat << USAGE
Usage: $0 <TRANSFORMATION_ID> <SHORT_NAME> [VERSION] [WORKDIR]

Arguments:
  TRANSFORMATION_ID   T-spec identifier (e.g., T5)
  SHORT_NAME         Transformation short name (e.g., container_split)
  VERSION            Version tag, default v_1_0 (e.g., v_1_1)
  WORKDIR            Path to workingfiles directory (optional)

Examples:
  $0 T5 container_split
  $0 T5 container_split v_1_0
  $0 T5 container_split v_1_0 /mnt/c/Users/scott/Documents/AIProjects/Markdown/RDGTranslations/workingfiles

IMPORTANT: Draft .md files must be created manually in WORKDIR before running this script.

USAGE
    exit 1
fi

TRANSFORMATION_ID="$1"
SHORT_NAME="$2"
VERSION="${3:-v_1_0}"
WORKDIR="${4:-/mnt/c/Users/scott/Documents/AIProjects/Markdown/RDGTranslations/workingfiles}"

# Validate working directory exists
if [[ ! -d "$WORKDIR" ]]; then
    echo "Error: Working directory does not exist: $WORKDIR"
    exit 1
fi

# Derive Windows path for Claude instructions
WORKDIR_WIN=$(wslpath -w "$WORKDIR" 2>/dev/null || echo "$WORKDIR")

################################################################################
# Generate filename and paths
################################################################################

# Convert T-ID to lowercase with underscore (T5 → t_5)
T_ID_NUM=$(echo "$TRANSFORMATION_ID" | sed 's/^T//')
T_ID_LOWER="t_${T_ID_NUM}"
FILENAME_BASE="${T_ID_LOWER}_${SHORT_NAME}_spec_${VERSION}"
FILEPATH="$WORKDIR/${FILENAME_BASE}.md"

echo ""
echo -e "${BOLD}═══════════════════════════════════════════════════════════${RESET}"
echo -e "${BOLD}T-Spec Bandy/Lock Workflow${RESET}"
echo -e "${BOLD}═══════════════════════════════════════════════════════════${RESET}"
echo ""
echo "Transformation ID: $TRANSFORMATION_ID"
echo "Short Name:       $SHORT_NAME"
echo "Version:          $VERSION"
echo "Filename:         ${FILENAME_BASE}.md"
echo "Location:         $WORKDIR/"
echo ""

# Verify file exists
if [[ ! -f "$FILEPATH" ]]; then
    echo "Error: Spec file not found: $FILEPATH"
    echo ""
    echo "Note: This script does not create spec content files."
    echo "Create the .md file manually before running this workflow."
    exit 1
fi

################################################################################
# Print Round 1 Bandy Instructions
################################################################################

echo -e "${BOLD}Round 1: Initial Bandy Review${RESET}"
echo ""
echo "Copy and paste the following instructions into Claude:"
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo ""

cat << EOF
Claude Bandy Instructions — $TRANSFORMATION_ID (Round 1)

Task: Bandy review of $TRANSFORMATION_ID specification
Document: ${FILENAME_BASE}.md
Status: DRAFT (pre-lock)

Authoritative local path (WSL):

\\\\wsl\$\\Ubuntu\\$(printf '%s' "$WORKDIR" | sed 's|/mnt/c|C|;s|/|\\|g')

Shortcut name: workingfiles

Your Role

You are acting as spec reviewer, not implementer.

Your task is to critically review $TRANSFORMATION_ID for:

- Logical completeness
- Consistency with prior locked specs (T1, T2, T3 if applicable)
- Correct scoping (no leakage)
- Clarity of invariants and abort conditions
- Absence of ambiguity

Explicit Constraints

Do NOT edit the file
Do NOT propose implementation details
Do NOT expand scope
Do NOT soften invariants

You MAY:

- Flag ambiguities
- Flag missing invariants
- Flag contradictions with prior specs
- Recommend tightening language
- Recommend removals if scope is too broad

Output Format (Required)

Return comments only, in this structure:

SECTION <number>:
- Observation:
- Risk (if any):
- Recommendation:

If a section is acceptable, respond with:

SECTION <number>:
- No issues.

No prose outside this structure.

Success Condition

Bandy completes when all issues are enumerated and the spec is ready for revision.

Begin review on ${FILENAME_BASE}.md only.
EOF

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo ""

################################################################################
# Human feedback loop
################################################################################

read -p "Press Enter when Claude Round 1 review is complete: "
echo ""

################################################################################
# Revision/Lock decision loop
################################################################################

ROUND=1

while true; do
    echo -e "${BOLD}Next Step:${RESET}"
    echo ""
    echo "1. Revise spec (bump version and re-review)"
    echo "2. LOCK this spec (confirmation required)"
    echo ""
    read -p "Enter choice (1 or 2): " CHOICE

    case "$CHOICE" in
        1)
            # Bump version
            MAJOR=$(echo "$VERSION" | cut -d_ -f2)
            MINOR=$(echo "$VERSION" | cut -d_ -f3)
            NEW_MINOR=$((MINOR + 1))
            NEW_VERSION="v_${MAJOR}_${NEW_MINOR}"

            echo ""
            echo "Version bump: $VERSION → $NEW_VERSION"

            VERSION=$NEW_VERSION
            FILENAME_BASE="${T_ID_LOWER}_${SHORT_NAME}_spec_${VERSION}"
            FILEPATH="$WORKDIR/${FILENAME_BASE}.md"
            ROUND=$((ROUND + 1))

            echo "New filename: ${FILENAME_BASE}.md"
            echo ""

            # Verify new file exists
            if [[ ! -f "$FILEPATH" ]]; then
                echo "Error: Spec file not found: $FILEPATH"
                echo ""
                echo "Create the revised .md file manually before continuing."
                exit 1
            fi

            read -p "Press Enter to continue with Round $ROUND review: "
            echo ""

            ################################################################################
            # Print Round 2+ Bandy Instructions
            ################################################################################

            echo -e "${BOLD}Round $ROUND: Bandy Review (Lock-Readiness)${RESET}"
            echo ""
            echo "Copy and paste the following instructions into Claude:"
            echo ""
            echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
            echo ""

            cat << EOF
Claude Bandy Instructions — $TRANSFORMATION_ID (Round $ROUND)

Task: Second-round bandy review (lock-readiness)
Document: ${FILENAME_BASE}.md
Status: DRAFT (post-revision, pre-LOCK)

Authoritative local path (WSL):

\\\\wsl\$\\Ubuntu\\$(printf '%s' "$WORKDIR" | sed 's|/mnt/c|C|;s|/|\\|g')

Your Role

You are acting as lock-gate reviewer.

Assume prior bandy feedback has been incorporated.

Your task is to determine whether $TRANSFORMATION_ID is fit to LOCK.

Review Focus (Only)

Evaluate for:

- Residual ambiguity
- Completeness of hard invariants
- Verification gates (necessary, sufficient, non-overlapping, explicit)
- Clean boundaries with adjacent transformations

Explicit Constraints

Do NOT edit the file
Do NOT suggest feature expansion
Do NOT re-litigate resolved issues

You MAY:

- Identify remaining blockers to LOCK
- Recommend narrowing language
- Declare the spec LOCK-ready

Output Format (Required)

Respond in one of two ways only:

Option A — LOCK READY

LOCK READY
No blocking issues.

Option B — BLOCKERS PRESENT

BLOCKER <n>:
- Location:
- Issue:
- Required change:

No other prose.

Success Condition

LOCK READY → spec may be locked without further revision

BLOCKERS PRESENT → one final revision will be applied

Begin review on ${FILENAME_BASE}.md only.
EOF

            echo ""
            echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
            echo ""

            read -p "Press Enter when Claude Round $ROUND review is complete: "
            echo ""
            ;;

        2)
            # Lock confirmation
            echo ""
            echo -e "${BOLD}${GREEN}LOCK CONFIRMATION${RESET}"
            echo ""
            echo "Current filename: ${FILENAME_BASE}.md"
            echo "Locked filename:  ${FILENAME_BASE}_LOCKED.md"
            echo ""
            echo "Confirm: Type 'LOCK' to proceed with lock, or press Enter to cancel:"
            read -p "> " CONFIRM

            if [[ "$CONFIRM" == "LOCK" ]]; then
                # Perform file rename
                LOCKED_FILEPATH="$WORKDIR/${FILENAME_BASE}_LOCKED.md"

                if [[ -f "$LOCKED_FILEPATH" ]]; then
                    echo ""
                    echo "Warning: Locked file already exists: ${FILENAME_BASE}_LOCKED.md"
                    echo "Type 'OVERWRITE' to replace, or press Enter to cancel:"
                    read -p "> " OVERWRITE_CONFIRM
                    if [[ "$OVERWRITE_CONFIRM" != "OVERWRITE" ]]; then
                        echo "Lock cancelled."
                        echo ""
                        continue
                    fi
                fi

                # Perform rename
                mv "$FILEPATH" "$LOCKED_FILEPATH"

                echo ""
                echo -e "${GREEN}✓ File locked and renamed.${RESET}"
                echo ""
                echo "Previous filename: ${FILENAME_BASE}.md"
                echo "New filename:      ${FILENAME_BASE}_LOCKED.md"
                echo ""
                echo "Next steps:"
                echo "- Locked file ready: $LOCKED_FILEPATH"
                echo "- Begin next T-spec if applicable"
                echo ""
                break
            else
                echo ""
                echo "Lock cancelled. Returning to menu."
                echo ""
            fi
            ;;

        *)
            echo "Invalid choice. Enter 1 or 2."
            echo ""
            ;;
    esac
done

echo -e "${BOLD}═══════════════════════════════════════════════════════════${RESET}"
echo -e "${BOLD}Bandy/Lock Workflow Complete${RESET}"
echo -e "${BOLD}═══════════════════════════════════════════════════════════${RESET}"
echo ""
