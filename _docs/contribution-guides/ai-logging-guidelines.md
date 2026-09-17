# AI Logging Guidelines

## Overview

AI activity logs track decisions, sources, tool usage, and session outcomes. These logs serve both humans and agents working on the project.

## Logging Principles

### Future-Proof Entries

- Do not mention specific filenames, function names, script names, or file paths
- Do not reference task numbers (T-numbers) - these can change or be reassigned
- Describe capabilities and outcomes, not implementation details
- Write entries that remain accurate even when code or structure changes
- Do not log meta-actions about updating the log itself, the changelog, or any project management artifacts (todo files, documentation, instructions, contribution rules, or guides)

### Self-Contained Entries

- Each log entry should stand alone
- Do not create cross-references to other docs that could break
- Include all necessary context within the entry

## Session Log Format

```markdown
### Session: [Brief descriptive title]

**Task:** [One sentence describing the goal]

**Decisions/Notes:**

- [Decision or action taken]
- [Another decision or action]

**Outcome:** [Result of the session]
```

## What to Log

### Sessions (`sessions.md`)

- Session title (descriptive, not task number)
- Task description (goal-focused)
- Key decisions made
- Outcome achieved

### Interactions (`interactions.md`)

- Date of interaction
- Task description
- Actions taken (describe what was done, not which functions were called)
- Result achieved

### Sources (`sources.md`)

- Sources consulted (type and reliability, not specific file paths)
- Research findings

### Tools (`tools.md`)

- Tools and techniques used (describe capability, not specific tool names)

## Examples

**Good (future-proof):**

- "Add multi-AI co-developer support to session backup"
- "Consolidate session databases in shared directory"
- "Anonymize project name mentions in conversation text"

**Bad (will become outdated):**

- "Add `--developer` flag to `ai-sessions-backup.py`"
- "Update `append_sessions_to_db()` function"
- "Move databases to developer-specific subdirectories under `.ai-activity/ai-sessions/`"
- "Complete task T-101"

## Log File Location

All log files reside in `.ai-activity/ai-logs/`:

- `interactions.md` - Per-task interaction entries
- `sources.md` - Sources consulted
- `tools.md` - Tools and techniques used
- `sessions.md` - Session-level summaries
- `research-log.md` - Research findings
