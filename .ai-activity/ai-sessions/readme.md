# AI Sessions Backup

Exported AI co-developer session transcripts stored here for archival and offline analysis. Session exports are generated from the local SQLite database and saved as markdown files. These files are gitignored from the main repository but may be referenced during analysis tasks.

## Co-Developers

This project supports multiple AI co-developers. Each developer's sessions are stored in a separate subdirectory:

| Developer | Databases | Purpose |
|-----------|----------|---------|
| `kilo-code` | website-sessions.db, famtree-sessions.db | Primary AI assistant session exports — most complete |
| `opencode` | (none) | AI co-developer (future use) |
| `github-copilot` | (none) | AI pair programmer (future use) |

Additional co-developers can be added by:
1. Adding a new entry to `.dev-scripts/ai-assistant/scripts/ai-developers.jsonc`
2. Creating a matching subdirectory under `.dev-scripts/ai-assistant/<developer-id>/`
3. Adding `database-schema.jsonc`, `paths-to-replace.jsonc`, and `session-ids.jsonc` in that subdirectory

## Usage

Scripts are in `.dev-scripts/ai-assistant/`:
- `ai-sessions-backup.py` — Export sessions with path anonymization
- `ai-sessions-stats.py` — Generate session statistics
- `session-ids-*.json` — Session IDs per developer
- `paths-to-replace-*.json` — Path patterns for anonymization

## Path Anonymization

All local filesystem paths are replaced with `_www_` during export to avoid exposing local directory structures. The source database path is never hardcoded in scripts — it should be provided via command-line argument when running the backup script.

## Workflow

Use the `ai-session-backup` skill:

```
skill(name="ai-session-backup")
```

See AI development tools documentation for tools guides and `.skills/ai-session-backup/skill.md` for the backup workflow. Also see `.skills/ai-analysis/skill.md` for analysis workflow.
