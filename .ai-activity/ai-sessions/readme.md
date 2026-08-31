# AI Sessions Backup

Exported Kilo session transcripts stored here for archival and offline analysis. Session exports are generated from the local SQLite database and saved as markdown files. These files are gitignored from the main repository but may be referenced during analysis tasks.

## Co-Developers

This project supports multiple AI co-developers. Each developer's sessions are stored in a separate subdirectory:

| Developer | Databases | Purpose |
|-----------|----------|---------|
| `kilo-code` | website-sessions.db, famtree-sessions.db | Primary Kilo session exports — most complete |
| `opencode` | (none) | OpenCode co-developer (future use) |
| `github-copilot` | (none) | GitHub Copilot (future use) |

## Usage

Scripts are in `_www_/.dev-scripts/ai-assistant/`:
- `ai-sessions-backup.py` — Export sessions with path anonymization
- `session-ids-*.json` — Session IDs per developer
- `paths-to-replace-*.json` — Path patterns for anonymization

## Path Anonymization

All local filesystem paths are replaced with `_www_` during export to avoid exposing local directory structures. The Kilo database path is never hardcoded in scripts — it should be provided via command-line argument when running the backup script.

## Workflow

Use the `ai-session-backup` skill:

```
skill(name="ai-session-backup")
```

See `_docs/dev-guides/kilo-dev-guide.md` for session export instructions and `.skills/ai-session-backup/skill.md` for the backup workflow. Also see `.skills/ai-analysis/skill.md` for analysis workflow.
