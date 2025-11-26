#!/bin/bash
# Script to prompt reading documentation from dochome

# Define paths
DOCHOME="/mnt/c/Users/scott/Documents/AIProjects/Markdown/RDGTranslations"

echo "=========================================="
echo "RDG Translation Project - Load Context"
echo "=========================================="
echo ""
echo "Documentation files in dochome:"
echo ""

# List markdown files in dochome
if [ -d "$DOCHOME" ]; then
    ls -lh "$DOCHOME"/*.md 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
    echo ""
    echo "To load project context, please read:"
    echo ""
    for file in "$DOCHOME"/*.md; do
        if [ -f "$file" ]; then
            echo "  - $(basename "$file")"
        fi
    done
    echo ""
    echo "Path: $DOCHOME"
else
    echo "  Warning: dochome directory not found at $DOCHOME"
fi

echo ""
echo "=========================================="
