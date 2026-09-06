# Documentation Management

Rules for maintaining project documentation, logs, and contribution records. This guide combines documentation-specific guidance with shared contribution rules for future-proof text.

## Core Principle

**Write for the project's future, not its current implementation.**

Documentation outlives the code it describes. When refactoring renames a function or moves a file, docs that mention the old names become misleading. The rule is simple: describe what something does, not what it is called or where it lives.

## Shared Contribution Rules

These rules apply to all permanent project records: documentation, logs, todo entries, changelog entries, and code comments.

### Prohibited Details

These become outdated during normal project evolution:

- File names: scripts, configs, databases, assets
- Function and method names
- Class and module names
- Variable names
- CLI flags and arguments
- Directory paths and folder structures
- Line numbers and offsets
- URLs that encode implementation details

### Required Instead

Describe behavior, capability, and intent:

| Instead of | Write |
|------------|-------|
| "Add `--developer` flag to script" | "Add multi-AI co-developer support" |
| "Update `generate_path_variations()`" | "Improve path replacement logic" |
| "Move databases to `.ai-activity/`" | "Consolidate session storage location" |
| "Fix line 142 in audit script" | "Fix version synchronization check" |
| "Create `VERSION` file" | "Add version tracking" |

## Documentation-Specific Rules

### Structure

- Documentation belongs in `_docs/` with topic-based subdirectories
- Each doc should be self-contained — avoid cross-references that could break
- Use relative links only when the target is stable and unlikely to move
- Prefer describing concepts over linking to specific files

### Content

- Describe **what** and **why**, not **how** or **where**
- Focus on user-facing behavior and project concepts
- Avoid implementation details that change during refactoring
- Use generic examples with placeholders like `<script>` or `<config-file>`

### Maintenance

- When updating docs, apply future-proof rules to new text
- Remove outdated sections rather than patching them
- If a doc describes a moving target (like file locations), make it generic or remove it
- Keep docs synchronized with actual behavior — outdated docs are worse than no docs

## Logging Rules

AI activity logs track decisions, sources, tool usage, and session outcomes. These logs serve both humans and agents working on the project.

### Logging Principles

#### Future-Proof Entries
- Do not mention specific filenames, function names, script names, or file paths
- Do not reference task numbers (T-numbers) — these can change or be reassigned
- Describe capabilities and outcomes, not implementation details
- Write entries that remain accurate even when code or structure changes

#### Self-Contained Entries
- Each log entry should stand alone
- Do not create cross-references to other docs that could break
- Include all necessary context within the entry

### Session Log Format

```markdown
### Session: [Brief descriptive title]

**Task:** [One sentence describing the goal]

**Decisions/Notes:**
- [Decision or action taken]
- [Another decision or action]

**Outcome:** [Result of the session]
```

### What to Log

#### Sessions (`sessions.md`)
- Session title (descriptive, not task number)
- Task description (goal-focused)
- Key decisions made
- Outcome achieved

#### Interactions (`interactions.md`)
- Date of interaction
- Task description
- Actions taken (describe what was done, not which functions were called)
- Result achieved

#### Sources (`sources.md`)
- Sources consulted (type and reliability, not specific file paths)
- Research findings

#### Tools (`tools.md`)
- Tools and techniques used (describe capability, not specific tool names)

## Enforcement

The pre-commit audit checks:

### Todo and Changelog
- File extensions in entries
- Path-like strings in entries
- Duplicate tasks across todo files

### Logs
- T-numbers in log entries
- File extensions in log entries
- Path-like strings in log entries

### Documentation
- Referenced files exist
- Cross-references are valid

Violations fail the commit with actionable messages.

## Examples

### Todo Entries

**Good:**
```markdown
- T-123: Add incremental stats generation with caching
```

**Bad:**
```markdown
- T-123: Add --incremental flag to ai-sessions-stats.py
```

### Changelog Entries

**Good:**
```markdown
### Added
- Incremental stats generation with caching
```

**Bad:**
```markdown
### Added
- Added --incremental flag to ai-sessions-stats.py
- Created _normalize_session() function
```

### Log Entries

**Good:**
```markdown
The user wants to refactor the backup workflow. This means separating backup from stats generation.
```

**Bad:**
```markdown
I moved ai-sessions-backup.py from folder A to folder B
```

## See Also

- `_docs/contribution-guides/adding-text.md` — Future-proof text rules
- `_docs/contribution-guides/ai-logging-guidelines.md` — AI logging standards
- `_docs/contribution-guides/changelog-management.md` — Changelog workflow
- `_docs/dev-guides/version-management.md` — Version file management
- `.todo/todo-next.md` — Active tasks following these rules
- `.todo/todo-done.md` — Completed tasks following these rules
- `.ai-activity/ai-logs/` — Project activity logs
