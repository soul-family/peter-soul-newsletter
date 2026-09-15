# AI Transparency Guide

Quick reference for AI transparency in this project. For the full guide, see `_docs/dev-guides/ai-dev-guides/ai-transparency.md`.

## Log Files

| File | Purpose |
|------|---------|
| `.ai-activity/ai-logs/interactions.md` | Detailed per-task interaction log |
| `.ai-activity/ai-logs/sessions.md` | Session index with outcomes |
| `.ai-activity/ai-logs/sources.md` | Research sources consulted |
| `.ai-activity/ai-logs/tools.md` | Tools and techniques used |
| `.ai-activity/ai-logs/research-log.md` | Research findings and outcomes |

## Entry Format

```markdown
## Interaction: [short task label]

**Time:** [date/time if available]

**Task:** [one sentence describing the work performed]

**Actions:**
1. [action item]
2. [action item]

**Result:** [outcome in one sentence]
```

## Key Rules

- **Self-contained:** Each entry must be understandable without external context.
- **No sensitive data:** Never log plaintext emails, passwords, API keys, tokens, or personal identifiers.
- **No implementation details:** Use descriptive role labels instead of function names, file paths, or script names.
- **No task numbers:** Describe work conceptually; do not reference T-numbers or gap numbers.
- **Concise:** One entry per discrete task. Merge micro-decisions into a single entry when they occur in one continuous interaction.
