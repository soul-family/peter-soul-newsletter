# Adding Text

Rules for writing text in permanent project records: todo entries, changelog entries, logs, documentation, and code comments. These rules keep records accurate and maintainable as the project evolves.

## Core Principle

**Write for the project's future, not its current implementation.**

Records outlive the code they describe. When refactoring renames a function or moves a file, records that mention the old names become misleading. The rule is simple: describe what something does, not what it is called or where it lives.

## Prohibited Details

These become outdated during normal project evolution:

- File names: scripts, configs, databases, assets
- Function and method names
- Class and module names
- Variable names
- CLI flags and arguments
- Directory paths and folder structures
- Line numbers and offsets
- URLs that encode implementation details
- **See Also sections in documentation** - Cross-references that break if files move or change

## Required Instead

Describe behavior, capability, and intent:

| Instead of | Write |
| --- | --- |
| "Add `--developer` flag to script" | "Add multi-AI co-developer support" |
| "Update `generate_path_variations()`" | "Improve path replacement logic" |
| "Move databases to `.ai-activity/`" | "Consolidate session storage location" |
| "Fix line 142 in audit script" | "Fix version synchronization check" |
| "Create `VERSION` file" | "Add version tracking" |
| **Documentation with `## See Also`** | **Self-contained documentation** - each file must work standalone without cross-references to other docs that could break if files move or change |

## Required Instead

Describe behavior, capability, and intent:

| Instead of | Write |
| --- | --- |
| "Add `--developer` flag to script" | "Add multi-AI co-developer support" |
| "Update `generate_path_variations()`" | "Improve path replacement logic" |
| "Move databases to `.ai-activity/`" | "Consolidate session storage location" |
| "Fix line 142 in audit script" | "Fix version synchronization check" |
| "Create `VERSION` file" | "Add version tracking" |
| "Prevent left sidebar from being sticky on small screens" | "Restrict sticky sidebar to large-screen layouts" |

## Tone

Describe changes in positive terms: state what something does, not what it does not do.

- Prefer "Restrict sticky sidebar to large-screen layouts" over "Prevent sidebar from sticking on small screens"
- Prefer "Deduplicate navigation links" over "Remove duplicate links"

## By Context

### Todo Entries

Describe the outcome, not the implementation:

```markdown
- T-123: Add incremental stats generation with caching
```

Not:

```markdown
- T-123: Add --incremental flag to ai-sessions-stats.py
```

### Changelog Entries

Describe what changed for users:

```markdown
### Added

- Incremental stats generation with caching
```

Not:

```markdown
### Added

- Added --incremental flag
- Created _normalize_session() function
```

### Logs

Record decisions and outcomes:

```markdown
The user wants to refactor the backup workflow. This means separating backup from stats generation.
```

Not:

```markdown
I moved ai-sessions-backup.py from folder A to folder B
```

### Documentation

Describe concepts and workflows:

```markdown
The backup script exports session data to anonymized databases.
```

Not:

```markdown
The script is at `.dev-scripts/ai-assistant/ai-sessions-backup.py`
```

### Code Comments

Explain why, not what:

```python
# Bulk loading avoids N+1 queries across large datasets
```

Not:

```python
# Load all messages in one query
```

## Edge Cases

- **Existing records**: When updating old records, apply these rules to the new text
- **Technical terms**: Domain-specific terms like "SQLite", "JSON", "session" are fine
- **Proper nouns**: Project names, tool names, and people names are fine
- **Examples in docs**: When giving examples, use generic placeholders like `<script>` or `<config-file>`

## Enforcement

The pre-commit audit checks todo and changelog entries for:

- File extensions
- Path-like strings
- Implementation-specific terminology

Violations fail the commit with actionable messages.
