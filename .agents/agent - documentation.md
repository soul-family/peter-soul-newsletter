# Agent Instructions

## Documentation Guidelines

Key principles:
- Every doc must be self-contained (no cross-references that break)
- Scripts/tools get their own dedicated doc
- Contribution docs serve both humans and agents
- Language instructions in docs must be followed
- Changelog entries must be future-proof (no specific filenames or paths)

Read `/_docs/contribution-guides/` folder.

### Self-Contained Documents
Every documentation file must be self-sufficient. Do not create cross-references to other docs that could break if files move or change. Each doc should contain all necessary information within itself.

### Dedicated Documentation
When creating scripts or tools, create a dedicated documentation file for each one. Do not overload general guides with specific tool documentation.

### Contribution Documents
Contribution documents are for both humans and agents. When creating or updating docs, ensure they serve both audiences:
- Use clear language instructions that agents can follow
- Include contribution doc file references where humans can find more details
- Contribution docs live in `_docs/contribution-guides/`

### Documentation Structure
- `_docs/contribution-guides/` — Contribution guidelines for humans and agents
- `_docs/dev-guides/ai-dev-guides/` — AI development guides (one per topic)
- `_docs/dev-guides/` — Development guides
- `_docs/reports/` — Reports and analysis

### File Naming
Use descriptive, hyphenated names: `ai-session-backup-guide.md`, `skills-guide.md`, etc.

### Language Instructions
All agents must follow language instructions in documentation. When a doc references a contribution file, agents should read it before proceeding.

### Changelog Entries
When writing changelog entries:
- Describe capabilities and features, not implementation details
- Do not mention specific filenames, function names, script names, or file paths
- Write entries that remain accurate even when code changes
- See `_docs/contribution-guides/changelog-management.md` for full guidelines

### AI Logging
When writing AI activity log entries:
- Do not mention specific filenames, function names, script names, or file paths
- Do not reference task numbers (T-numbers) — these can change or be reassigned
- Describe capabilities and outcomes, not implementation details
- See `_docs/contribution-guides/ai-logging-guidelines.md` for full guidelines
