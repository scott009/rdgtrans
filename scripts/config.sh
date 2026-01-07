#!/bin/bash

# RDG Translation Project - Script Configuration
# Shared configuration for all operational scripts
#
# This file is sourced by all scripts in the scripts/ directory

# Project Paths (from sharedContext.md)
PROJHOME="/home/scott/gitrepos/rdgtrans"
DOCHOME="/mnt/c/Users/scott/Documents/AIProjects/Markdown/RDGTranslations"
SHOWOFF="/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1"
PYHOME="$PROJHOME/py"
LMASTERS="$PROJHOME/lmasters"
CORRECTIONS="$PROJHOME/corrections"
ARCHIVE="$PROJHOME/archive"
SCRIPTS="$PROJHOME/scripts"
LOGS="$PROJHOME/logs"

# Session Tracking
SESSION_INFO="$PROJHOME/.session_info"

# Retention Policies (session-based)
LOG_RETENTION_SESSIONS=10      # Keep last 10 sessions of logs
BACKUP_RETENTION_SESSIONS=5    # Keep last 5 sessions of backups
MILESTONE_INTERVAL=10          # Create milestone backup every 10 sessions

# Core Files
JMASTER="$PROJHOME/workmaster.json"
PRESMASTER="$PROJHOME/presentation.json"

# Logging Configuration
LOG_TO_CONSOLE=true            # Print to console
LOG_TO_FILE=true               # Also save to log file
LOG_TIMESTAMP_FORMAT="%Y-%m-%d %H:%M:%S"

# Colors for console output (optional, for readability)
COLOR_RESET="\033[0m"
COLOR_GREEN="\033[0;32m"
COLOR_YELLOW="\033[0;33m"
COLOR_RED="\033[0;31m"
COLOR_BLUE="\033[0;34m"
COLOR_GRAY="\033[0;90m"

# Helper Functions

# Get current session number
get_session_number() {
    if [ -f "$SESSION_INFO" ]; then
        grep "SESSION_NUMBER=" "$SESSION_INFO" | cut -d'=' -f2
    else
        echo "0"
    fi
}

# Get current timestamp
get_timestamp() {
    date "+%Y%m%d_%H%M%S"
}

# Get formatted date for display
get_display_date() {
    date "+$LOG_TIMESTAMP_FORMAT"
}

# Create log filename for a script
get_log_filename() {
    local script_name=$1
    local session=$(get_session_number)
    local timestamp=$(get_timestamp)
    echo "${LOGS}/${script_name}_s${session}_${timestamp}.log"
}

# Initialize logging for a script
init_logging() {
    local script_name=$1

    # Create logs directory if it doesn't exist
    mkdir -p "$LOGS"

    # Get log filename
    LOG_FILE=$(get_log_filename "$script_name")

    # Export for use in script
    export LOG_FILE
}

# Log message (both console and file)
log_msg() {
    local message="$1"

    if [ "$LOG_TO_CONSOLE" = true ]; then
        echo -e "$message"
    fi

    if [ "$LOG_TO_FILE" = true ] && [ -n "$LOG_FILE" ]; then
        # Strip ANSI color codes for log file
        echo -e "$message" | sed 's/\x1b\[[0-9;]*m//g' >> "$LOG_FILE"
    fi
}

# Log with timestamp
log_with_time() {
    local message="$1"
    local timestamp=$(get_display_date)
    log_msg "[$timestamp] $message"
}

# Log header
log_header() {
    local title="$1"
    log_msg ""
    log_msg "=========================================="
    log_msg "$title"
    log_msg "=========================================="
    log_msg ""
}

# Log success message
log_success() {
    log_msg "${COLOR_GREEN}✓${COLOR_RESET} $1"
}

# Log warning message
log_warning() {
    log_msg "${COLOR_YELLOW}⚠${COLOR_RESET} $1"
}

# Log error message
log_error() {
    log_msg "${COLOR_RED}✗${COLOR_RESET} $1"
}

# Log info message
log_info() {
    log_msg "${COLOR_BLUE}ℹ${COLOR_RESET} $1"
}

# Finish logging (print log file location)
finish_logging() {
    if [ "$LOG_TO_FILE" = true ] && [ -n "$LOG_FILE" ]; then
        log_msg ""
        log_success "Full log saved to: $LOG_FILE"
    fi
}
