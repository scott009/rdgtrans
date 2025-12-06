#!/bin/bash

# Claude Code Initialization Script
# Location: /home/scott/gitrepos/rdgtrans/scripts/read_docs.sh
#
# This script shows available documentation files for the RDG Translation Project

# Change to project directory
cd /home/scott/gitrepos/rdgtrans/

# Define paths
DOCHOME="/mnt/c/Users/scott/Documents/AIProjects/Markdown/RDGTranslations"

echo "=========================================="
echo "RDG Translation Project - Load Context"
echo "=========================================="
echo ""
echo "*** IMPORTANT: READ FIRST ***"
echo ""
echo "  sharedContext.md - AUTHORITATIVE source for all paths, repos, and project structure"
echo "                     All AI agents MUST use this as canonical reference"
echo ""
echo "Documentation files in dochome:"
echo ""

# List markdown files in dochome
if [ -d "$DOCHOME" ]; then
    ls -lh "$DOCHOME"/*.md 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
    echo ""
    echo "To load project context, please read:"
    echo ""
    echo "  1. sharedContext.md (READ FIRST - canonical paths and structure)"
    echo ""
    echo "  Then read agent-specific guides:"
    for file in "$DOCHOME"/*.md; do
        if [ -f "$file" ]; then
            basename_file=$(basename "$file")
            if [ "$basename_file" != "sharedContext.md" ]; then
                echo "  - $basename_file"
            fi
        fi
    done
    echo ""
    echo "Path: $DOCHOME"
else
    echo "  Warning: dochome directory not found at $DOCHOME"
fi

echo ""
echo "=========================================="
