# AI Activity Log - Tools

## External Apps and Tools Used

| Category | Tools | Purpose |
| --- | --- | --- |
| Development environment | Visual Studio Code, PowerShell terminal | File editing, command execution, project navigation |
| Version control | Git | Repository inspection, commit strategy, history management |
| Scripting | Python | Task management, changelog generation, pre-commit audit |
| File operations | Shell utilities (Copy-Item, New-Item, Get-ChildItem) | Directory management, file copying, pattern matching |
| AI assistants | Kilo, OpenCode, GitHub Copilot | Planning, code generation, workflow automation, multi-agent orchestration |
| Skills | .skills/ folder and v1 migration archive | Specialized AI instructions for current and historical workflows |
| Web browsers | Chrome, Firefox, Edge | Compatibility testing, link verification |

## Techniques Used

| Technique | Purpose |
| --- | --- |
| glob | Lists files matching patterns to confirm source files exist |
| read | Reads source files to understand structure, link patterns, and content |
| grep | Searches for link patterns and specific text across source files |
| write | Creates new files and documentation |
| edit | Plans and executes fixes for inconsistencies across project files |
| skill | Loads specialized skill definitions for specific task categories |
| sqlite3 | Query and back up AI co-developer session database tables |
| agent_manager | Orchestrate multiple AI sessions in parallel worktrees |
| task | Launch subagents for parallel exploration or code generation |

**Notes:**

- Exact filenames and paths are omitted from command details because they change as the project evolves.
- Commands describe by technique and purpose rather than specific file references.

## Current Review Techniques

| Technique | Purpose |
| --- | --- |
| Targeted repository reading | Compare task, documentation, changelog, and log records with contribution rules |
| Pattern search | Locate duplicate task states, implementation-specific log details, and stale references |
| Automated repository audit | Verify todos, documentation links, transparency, changelog, and session statistics |
| Changelog promotion | Move completed release entries into the current version and clear pending entries |
