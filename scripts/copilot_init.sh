#!/bin/bash

# Copilot Initialization Script
# Loads essential context for GitHub Copilot to operate as implementation partner
#
# Location: /home/scott/gitrepos/rdgtrans/scripts/copilot_init.sh
#
# This script loads ONLY what Copilot needs to execute tasks.
# Copilot is the implementer/executor, not the architect.
#
# For full architectural context, see scripts/read_docs.sh (Claude Code uses that)

DOCHOME="/mnt/c/Users/scott/Documents/AIProjects/Markdown/RDGTranslations"

echo "=========================================="
echo "GitHub Copilot - Implementation Context"
echo "=========================================="
echo ""
echo "*** IMPORTANT: READ FIRST ***"
echo ""
echo "  sharedContext.md - AUTHORITATIVE source for all paths, repos, and project structure"
echo "                     READ THIS FIRST to understand where everything is located"
echo ""
echo "  CopilotGuide.md  - YOUR operational guide defining your role and boundaries"
echo ""
echo "=========================================="

# Check if dochome exists
if [ ! -d "$DOCHOME" ]; then
    echo "ERROR: Documentation directory not found at $DOCHOME"
    exit 1
fi

echo ""
echo "Essential documentation files for Copilot:"
echo ""

# List essential files with sizes
ls -lh "$DOCHOME/sharedContext.md" 2>/dev/null | awk '{print "  " $9, "(" $5 ")"}'
ls -lh "$DOCHOME/CopilotGuide.md" 2>/dev/null | awk '{print "  " $9, "(" $5 ")"}'
ls -lh "$DOCHOME/Tasks.md" 2>/dev/null | awk '{print "  " $9, "(" $5 ")"}'

echo ""
echo "Reference documentation (read but do not modify):"
echo ""

ls -lh "$DOCHOME/presentationLayer.md" 2>/dev/null | awk '{print "  " $9, "(" $5 ")"}'
ls -lh "$DOCHOME/ClaudeGuide.md" 2>/dev/null | awk '{print "  " $9, "(" $5 ")"}'

echo ""
echo "To load Copilot context, please read in this order:"
echo ""
echo "  1. sharedContext.md (READ FIRST - authoritative paths and structure)"
echo "  2. CopilotGuide.md  (YOUR operational guide and boundaries)"
echo "  3. Tasks.md         (Current tasks and priorities)"
echo ""
echo "Path: $DOCHOME"
echo ""
echo "=========================================="
echo ""
echo "Your Role: Implementation Partner"
echo "  ✓ Execute tasks within established architecture"
echo "  ✓ Follow patterns defined by Claude Code"
echo "  ✓ Run generator scripts (do not modify them)"
echo "  ✓ Test and validate outputs"
echo ""
echo "  ✗ Do NOT modify: presentation.json, workmaster.json"
echo "  ✗ Do NOT modify: Generator scripts or core documentation"
echo "  ✗ Do NOT make architectural decisions"
echo ""
echo "  When in doubt: Ask the user or defer to Claude Code"
echo ""
echo "=========================================="
echo ""

# Create timestamp file so Claude Code can verify Copilot initialization
TIMESTAMP_FILE="/home/scott/gitrepos/rdgtrans/.copilot_last_init"
date "+%Y-%m-%d %H:%M:%S" > "$TIMESTAMP_FILE"
echo "✓ Copilot initialization timestamp recorded"
echo "  ($TIMESTAMP_FILE)"
echo ""
