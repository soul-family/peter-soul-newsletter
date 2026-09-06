# AI Session Backup Skill

## Goal

Export AI co-developer session data from the local SQLite database into project-specific backup databases, anonymizing all local filesystem paths to avoid exposing the local directory structure.

## When to Use

- When archiving AI co-developer sessions for long-term storage
- Before pushing session data to a shared repository
- When offline analysis of sessions is needed
- When local paths must be hidden from collaborators

## Prerequisites

- Access to the AI co-developer SQLite database
- `.dev-scripts/ai-assistant/scripts/ai-sessions-backup.py` script
- Session IDs to back up (from `session-ids-*.json` or auto-discovered via `--current-session`)
- Output directory (`.ai-activity/ai-sessions/<developer>/` by default)

## Workflow

### Step 1: Identify Session IDs

1. Query the local AI co-developer database for session IDs belonging to the target project
2. Group sessions by project (e.g., website, famtree)
3. Session IDs are listed in `session-ids-*.json` files next to the script

### Step 2: Run the Backup Script

Provide the database path and session IDs via command-line arguments:

```bash
python .dev-scripts/ai-assistant/scripts/ai-sessions-backup.py \
  --db-path <path-to-source.db> \
  --developer <developer-id> \
  --current-session
```

**`--developer`** selects which AI co-developer's session IDs to load from JSON config. Available developers are defined in `ai-developers.jsonc`.

**`--current-session`** auto-discovers the most recent session from the developer's session knowledge folder (`.ai-activity/ai-sessions/<developer>/`) or by querying the SQLite database directly. The discovered session ID is added to the backups if not already present.

If session-specific options are omitted, the script loads defaults from JSON config files.

If no session IDs are found in config or arguments, the script falls back to interactive mode.

### Step 3: Verify Output

1. Confirm databases are created in `.ai-activity/ai-sessions/<developer>/`
2. Verify path anonymization by checking that `_www_` replaces all local paths
3. Review generated stats JSON files for per-session counts and totals
4. Confirm session, message, and part counts match expected data

### Path Anonymization

The script's path replacement function generates all slash-form variations automatically — forward slash, backslash, JSON-escaped, and with/without drive letter. The JSON config files only need to list each base path once:

```json
{"paths": ".*" "replacement": "_www_"}
```

## Output Format

SQLite databases and stats JSON files created in `.ai-activity/ai-sessions/<developer>/`:
- `<project>-sessions.db` and `<project>-sessions.stats.json` — project-specific sessions

Each database contains three tables:

| Table | Purpose |
|-------|---------|
| `session` | Session metadata (ID, title, directory, tokens, cost) |
| `message` | Conversation turns (role, model, finish reason) |
| `part` | Content pieces (text, reasoning, tool calls/results) |

Each stats JSON file contains:
- `database` — database filename
- `generated_at` — ISO timestamp of stats generation
- `totals` — total counts across all sessions
- `sessions` — per-session stats (id, title, directory, timestamps, message/part counts)

## Verification

- [ ] Database files exist in `.ai-activity/ai-sessions/<developer>/`
- [ ] Stats JSON files exist alongside databases
- [ ] Session directories show `_www_` (not local paths)
- [ ] No local project path strings found in any database column
- [ ] Session, message, and part counts match source database

## Notes

- The source database path is never hardcoded — always provide via `--db-path`
- Local paths are replaced with `_www_` before writing to the output database
- New AI co-developers can be added by extending the developer config and adding per-developer session ID and path replacement files
