# AI Session Backup and Stats - Contributor Quick-Start

Quick reference to back up AI co-developer sessions and update project statistics.

## Prerequisites

- local Python 3.x
- local SQLite with access to the AI co-developer SQLite database
- `.dev-scripts/ai-sessions/` in the project

## Workflow

### 1. Back Up Current Session

```bash
python .dev-scripts/ai-sessions/ai-sessions-backup.py \
  --db-path <path-to-source.db> \
  --developer <developer-id> \
  --current-session \
  --append
```

This appends the current session to the existing backup database without overwriting existing data.

### 2. Regenerate Statistics

```bash
python .dev-scripts/ai-sessions/ai-sessions-stats.py \
  --db-path .ai-activity/ai-sessions/<developer>/sessions.db \
  --incremental \
  --developer <developer-id>
```

Incremental mode only processes new sessions, preserving existing stats for unchanged sessions.

### 3. Verify Output

- Database: `.ai-activity/ai-sessions/<developer>/sessions.db`
- Stats: `.ai-activity/ai-sessions/<developer>/sessions.stats.json`
- Reports: `.ai-activity/ai-reports/project-stats-totals.json` and `.md`

### 4. Run Pre-Commit Audit

```bash
python .dev-scripts/scripts/pre-commit/pre_commit_audit.py
```

This verifies:
- Todo integrity
- AI transparency logs
- Changelog format
- Guide references
- Session stats are up-to-date after database changes

## Adding a New Co-Developer

1. Add entry to `.dev-scripts/ai-assistant/scripts/ai-developers.jsonc`
2. Create `.dev-scripts/ai-assistant/<developer-id>/` with:
   - `database-schema.jsonc`
   - `paths-to-replace.jsonc`
   - `session-ids.jsonc`
3. Run backup and stats scripts with `--developer <developer-id>`
