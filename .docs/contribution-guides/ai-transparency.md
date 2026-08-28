# AI Transparency Guide

## Overview

This guide defines how AI interactions are logged for this archive project. The log must be readable without external research, free of sensitive data, and precise in scope and outcome.

## File

- `.ai-activity/INTERACTIONS.md`

## Entry Format

Each interaction entry follows this structure:

```markdown
## Interaction: [short task label]

**Time:** [date/time if available]

**Task:** [one sentence describing the work performed]

**Actions:**
1. [action item]
2. [action item]
...

**Result:** [outcome in one sentence]
```

## Rules

- **Self-contained:** Do not reference other documents for context. Each entry must be understandable on its own.
- **No sensitive data:** Never log plaintext emails, passwords, API keys, tokens, or personal identifiers.
- **No implementation details:** Do not log specific function names, class names, file paths, or script names. Use descriptive role labels instead (e.g., "date-mapping script" instead of `update_commit_dates.py`).
- **No task numbers:** Do not reference T-numbers or gap numbers. Describe the work conceptually.
- **Goal-oriented:** State what was done and what changed. Do not narrate the reasoning process or intermediate exploration.
- **Concise:** One entry per discrete task or decision. Merge micro-decisions into a single entry when they occur in one continuous interaction.

## Allowed Content

- Task descriptions
- Actions taken (numbered list)
- Outcomes and decisions
- Concepts and architectural choices
- Files created, modified, or removed (by role or path, no OS-specific details)
- Data structures or formats changed
- Verification steps performed

## Prohibited Content

- Email addresses
- URLs that expose personal or sensitive information
- Function names, class names, or method signatures
- Variable names or configuration keys
- T-numbers, gap numbers, or other internal task identifiers
- Verbose reasoning, exploration, or back-and-forth narration

## Review Cycle

- Review before each commit.
- Remove entries that reveal sensitive data or implementation details.
- Merge or compress redundant entries.
