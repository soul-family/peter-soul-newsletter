# AI Session Backup Guide

Complete guide for the session backup script - exports AI co-developer session data into project-specific SQLite databases with local paths anonymized.

## What It Does

Reads session data (session, message, part tables) from the local AI co-developer SQLite database and writes a new database filtered to the specified session IDs, with all local filesystem paths replaced by `_www_` to avoid exposing the local directory structure.

## When to Use

- Before pushing session data to a shared repository
- When archiving sessions for long-term storage
- When local paths must be hidden from collaborators
- When offline analysis of session transcripts is needed
- When adding new sessions to an existing database (use `--append`)

## Script Location

`.dev-scripts/ai-sessions/ai-sessions-backup.py`

## Usage

```bash
# Create new database (default mode)
python .dev-scripts/ai-sessions/ai-sessions-backup.py --db-path <path-to-source.db>

# Append new sessions to existing database
python .dev-scripts/ai-sessions/ai-sessions-backup.py --db-path <path-to-source.db> --append

# Specify developer and auto-include current session
python .dev-scripts/ai-sessions/ai-sessions-backup.py --db-path <path-to-source.db> --developer <developer-id> --current-session

# Override session IDs via command line
python .dev-scripts/ai-sessions/ai-sessions-backup.py --db-path <path-to-source.db> --sessions ses_xxx,ses_yyy
```

## Command-line Arguments

| Argument | Description |
|----------|-------------|
| `--db-path PATH` | Path to the AI co-developer SQLite database - required |
| `--output-dir DIR` | Output directory (default: `.ai-activity/ai-sessions/<developer>`) |
| `--output-name NAME` | Output database filename (default: from developer config) |
| `--developer NAME` | AI co-developer ID from config (default: first configured developer) |
| `--current-session` | Auto-discover and include the most recent session |
| `--sessions IDS` | Comma-separated session IDs (overrides JSON config) |
| `--paths-to-replace PATHS` | Comma-separated paths to replace with `_www_` (overrides JSON config) |
| `--append` | Append new sessions to existing database instead of recreating it |

## Config Files

Located in `.dev-scripts/ai-sessions/` and per-developer subdirectories:

| File | Purpose |
|------|---------|
| `.dev-scripts/ai-sessions/ai-developers.jsonc` | AI developer definitions and configuration |
| `.dev-scripts/ai-sessions/shared/config_loader.py` | Configuration loading functions |
| `.dev-scripts/ai-sessions/<developer-id>/session-ids.jsonc` | Session IDs to back up - `{"session_ids": [...]}` |
| `.dev-scripts/readonly-paths-to-replace.jsonc` | Local paths to anonymize - `{"rules": [{"paths": [...], "replacement": "_www_"}]}` |
| `.dev-scripts/ai-sessions/shared/database-schema.jsonc` | Database schema definition |

## How It Works

### Default Mode
1. Loads session IDs from JSON config files (or command line)
2. Reads session data from the source database
3. Applies path replacement to anonymize local paths
4. Creates a new output database with the filtered data
5. Generates a `.stats.json` file with per-session statistics

### Append Mode (`--append`)
1. Checks existing sessions in the output database
2. Only processes sessions not already present
3. Applies path replacement per-entry for efficiency
4. Preserves all existing data

### Path Replacement
- All slash form variations are generated automatically from base paths
- Replacement is applied to all text fields in session, message, and part tables
- JSON-escaped paths are handled correctly

## Safeguards

- **Overwrite confirmation**: When output database exists and `--append` is not used, shows existing sessions and requires typing 'yes' to confirm or 'append' to switch modes
- **Append mode protection**: Existing sessions in the output database are preserved; only new sessions are added
- **Data retention**: Explicit confirmation required before any existing data is retired from the output

## Output

- `sessions.db` and matching `.stats.json` files in `.ai-activity/ai-sessions/<developer>/`
- Each database contains `session`, `message`, and `part` tables
- All local paths replaced with `_www_`

## Verification

- [ ] Database files exist in `.ai-activity/ai-sessions/<developer>/`
- [ ] Stats JSON files exist alongside databases
- [ ] Session directories show `_www_` (not local paths)
- [ ] No local path strings found in any database column
- [ ] Session, message, and part counts match source database
