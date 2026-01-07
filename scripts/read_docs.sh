#!/bin/bash

# read_docs.sh — SSQS v2 Compliant Initialization
# Script Version: 2.0
# SSQS Version: 2.0
# Last Updated by: WO-SSQS-v2-read_docs-Update-001
#
# Claude Code Initialization Script
# Location: /home/scott/gitrepos/rdgtrans/scripts/read_docs.sh
#
# This script loads governance and project documentation in SSQS v2 order

# SSQS v2 Initialization Order:
# 1. SessionStart.md — governs Sonnet/Haiku behavior and Work Order protocol
# 2. SSQS_v2_WorkOrder_Template.md — defines Work Order structure
# 3. sharedContext.md — authoritative project context
# 4. Additional project documents

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
echo "  SSQS v2 Governance Layer:"
echo "  1. SessionStart.md - Session initialization protocol and Work Order governance"
echo "  2. SSQS_v2_WorkOrder_Template.md - Work Order structure definition"
echo "  3. sharedContext.md - AUTHORITATIVE source for paths, repos, and project structure"
echo ""
echo "  All AI agents MUST load these three documents FIRST in this exact order."
echo ""
echo "Documentation files in dochome:"
echo ""

# List markdown files in dochome
if [ -d "$DOCHOME" ]; then
    ls -lh "$DOCHOME"/*.md 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'

    # Check for subdirectories
    if [ -d "$DOCHOME/session_start" ]; then
        echo ""
        echo "Session Start documents:"
        ls -lh "$DOCHOME/session_start"/*.md 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
    fi

    if [ -d "$DOCHOME/SSQS" ]; then
        echo ""
        echo "SSQS documents:"
        ls -lh "$DOCHOME/SSQS"/*.md 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
    fi

    echo ""
    echo "=========================================="
    echo "REQUIRED READING ORDER (SSQS v2):"
    echo "=========================================="
    echo ""
    echo "  GOVERNANCE LAYER (read in this order):"
    echo "  1. session_start/SessionStart.md"
    echo "  2. SSQS/SSQS_v2_WorkOrder_Template.md"
    echo "  3. sharedContext.md"
    echo ""
    echo "  OPERATIONAL LAYER (read as needed):"
    echo "  - ClaudeGuide.md"
    echo "  - CopilotGuide.md"
    echo "  - NETLIFY_SETUP.md"
    echo "  - SupervisorSessionQuickStart_v2.md"
    echo "  - Tasks.md"
    echo "  - presentationJson.md"
    echo "  - presentationLayer.md"
    echo "  - projspec.md"
    echo "  - tmaster_container_spec.md"
    echo ""
    echo "Path: $DOCHOME"
    echo ""
    echo "=========================================="
    echo "SSQS v2 Initialization Complete — Governance Layer Loaded"
    echo "=========================================="
else
    echo "  Warning: dochome directory not found at $DOCHOME"
fi

echo ""

# WO Applied: WO-SSQS-v2-read_docs-Update-001
