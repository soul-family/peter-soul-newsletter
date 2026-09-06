# AI Development Tools Documentation

This directory contains documentation for AI development tools used in the project.

## Available Co-Developers

| Co-Developer | Description |
|--------------|-------------|
| Kilo | AI coding assistant  |
| Opencode |  AI coding assistant |

Additional co-developers can be added by extending the developer config.

## Scripts and Configuration

The actual scripts and JSON configuration files are located in `.dev-scripts/ai-assistant/`:

| Item | Location |
|------|----------|
| Backup script | `.dev-scripts/ai-assistant/scripts/ai-sessions-backup.py` |
| Stats script | `.dev-scripts/ai-assistant/scripts/ai-sessions-stats.py` |
| Shared utilities | `.dev-scripts/ai-assistant/scripts/shared/` |
| Developer configs | `.dev-scripts/ai-assistant/scripts/ai-developers.jsonc` |
| Per-developer configs | `.dev-scripts/ai-assistant/<developer-id>/` |

## General Guidelines

- Each AI co-developer has their own session storage under `.ai-activity/ai-sessions/`
- Session statistics are calculated using the same methodology across all tools
- See session stats units documentation for stats calculation details

## See Also

- AI development guides — methodology, templates, and usage
- Statistics reports and analysis — `.ai-activity/ai-reports/`
- Session backups and exports — `.ai-activity/ai-sessions/`
