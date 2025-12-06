#!/bin/bash

# RDG Translation Project - Local Backup Script
# Creates compressed tar backup of dochome, projhome, and showoff
#
# This script is designed for GitHub Copilot to execute on user request
# Architect: Claude Code
# Executor: GitHub Copilot

# Exit on error
set -e

# Define paths (from sharedContext.md)
PROJHOME="/home/scott/gitrepos/rdgtrans"
DOCHOME="/mnt/c/Users/scott/Documents/AIProjects/Markdown/RDGTranslations"
SHOWOFF="/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1"
ARCHIVE="$PROJHOME/archive"

# Create timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="rdgtransbackup_${TIMESTAMP}.tar.gz"
BACKUP_PATH="$ARCHIVE/$BACKUP_NAME"

# Ensure archive directory exists
mkdir -p "$ARCHIVE"

echo "=========================================="
echo "RDG Translation Project - Backup"
echo "=========================================="
echo ""
echo "Creating backup: $BACKUP_NAME"
echo ""
echo "Backing up:"
echo "  - projhome: $PROJHOME"
echo "  - dochome:  $DOCHOME"
echo "  - showoff:  $SHOWOFF"
echo ""
echo "Destination: $BACKUP_PATH"
echo ""
echo "This may take a few moments..."
echo ""

# Create temporary directory for staging
TEMP_DIR=$(mktemp -d)
BACKUP_STAGE="$TEMP_DIR/rdgtrans_backup_$TIMESTAMP"
mkdir -p "$BACKUP_STAGE"

# Copy directories to staging area (excluding .git, node_modules, etc.)
echo "Stage 1/4: Copying projhome..."
rsync -a --exclude='.git' --exclude='archive' --exclude='node_modules' --exclude='__pycache__' \
    "$PROJHOME/" "$BACKUP_STAGE/projhome/"

echo "Stage 2/4: Copying dochome..."
rsync -a --exclude='.git' --exclude='node_modules' --exclude='vx_notebook' \
    "$DOCHOME/" "$BACKUP_STAGE/dochome/"

echo "Stage 3/4: Copying showoff..."
rsync -a --exclude='.git' --exclude='node_modules' \
    "$SHOWOFF/" "$BACKUP_STAGE/showoff/"

# Create compressed tar archive
echo "Stage 4/4: Creating compressed archive..."
tar -czf "$BACKUP_PATH" -C "$TEMP_DIR" "rdgtrans_backup_$TIMESTAMP"

# Cleanup
rm -rf "$TEMP_DIR"

# Get backup size
BACKUP_SIZE=$(du -h "$BACKUP_PATH" | cut -f1)

echo ""
echo "=========================================="
echo "Backup Complete!"
echo "=========================================="
echo ""
echo "File:     $BACKUP_NAME"
echo "Size:     $BACKUP_SIZE"
echo "Location: $ARCHIVE/"
echo ""
echo "To restore:"
echo "  tar -xzf $BACKUP_PATH -C /destination/path/"
echo ""
echo "=========================================="
