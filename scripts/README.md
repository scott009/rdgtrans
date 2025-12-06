# Scripts Directory

This directory contains operational scripts for the RDG Translation Project.

---

## Initialization Scripts

### `read_docs.sh`
**Purpose:** Load project context for Claude Code
**User:** Claude Code (Architect)
**Copilot Allowed:** ❌ No (Claude-specific initialization)

**What it does:**
- Displays documentation files in dochome
- Emphasizes sharedContext.md as authoritative source
- Lists all documentation for Claude to read
- Loads full architectural context

**How to run:**
```bash
/home/scott/gitrepos/rdgtrans/scripts/read_docs.sh
```

---

### `copilot_init.sh`
**Purpose:** Load project context for GitHub Copilot
**User:** GitHub Copilot (Implementation Partner)
**Copilot Allowed:** ✅ Yes (Copilot's initialization)

**What it does:**
- Displays essential documentation for Copilot
- Emphasizes role boundaries and responsibilities
- Lists implementation-focused documentation
- Loads lighter context (execution, not architecture)

**How to run:**
```bash
/home/scott/gitrepos/rdgtrans/scripts/copilot_init.sh
```

---

## Operational Scripts

### `backup.sh`
**Purpose:** Create compressed backup of entire project
**User:** GitHub Copilot (on user request)
**Copilot Allowed:** ✅ Yes (simple operational task)

**What it does:**
- Backs up projhome, dochome, and showoff
- Creates compressed tar.gz file in archive/
- Names file: `rdgtransbackup_YYYYMMDD_HHMMSS.tar.gz`
- Excludes .git directories and build artifacts
- Reports backup size and location

**How to run:**
```bash
/home/scott/gitrepos/rdgtrans/scripts/backup.sh
```

**Output location:**
```
/home/scott/gitrepos/rdgtrans/archive/rdgtransbackup_*.tar.gz
```

---

## Script Guidelines

### For Claude Code:
- ✅ Can create and modify all scripts
- ✅ Makes architectural decisions about script design
- ✅ Runs `read_docs.sh` for initialization

### For GitHub Copilot:
- ✅ Can run operational scripts (backup.sh)
- ✅ Can run copilot_init.sh for initialization
- ❌ Cannot modify scripts (defer to Claude Code)
- ❌ Cannot run read_docs.sh (Claude-specific)
- ✅ Reports results after execution

---

## Adding New Scripts

When adding new scripts:
1. Place in this directory (`scripts/`)
2. Make executable (`chmod +x scriptname.sh`)
3. Update this README with description
4. Specify whether Copilot is allowed to run it
5. Update sharedContext.md if introducing new concepts
6. Commit to git

---

**Last Updated:** 2025-12-06
**Maintained by:** Claude Code
