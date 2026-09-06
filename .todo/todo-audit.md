# Todo — Audit

Repeatable verification tasks for the Archive project. Audit tasks are not tied to a specific release or task number; they are gap-numbered checks that can be run at any time during project reviews, pre-commit audits, or maintenance windows.

## Purpose

Audit tasks verify project health and prevent regressions across:
- Todo integrity and numbering
- AI transparency and logging
- Changelog format and versioning
- Documentation consistency
- Privacy and path anonymization
- Database and stats accuracy

## When to Run

- Before committing changes
- After importing or migrating data
- During project reviews
- When adding new AI co-developers or session databases
- Periodically as part of maintenance

## How to Run

Audit tasks are manual checks. Run each applicable task and confirm the result before proceeding. If an audit fails, fix the issue or document the exception before continuing.

## Audit Tasks

- A-2: Verify todo-next.md and todo-done.md have no duplicate T-numbers
- A-3: Verify AI transparency logs exist and contain no sensitive data
- A-4: Verify CHANGELOG.md follows format and version ordering rules
- A-5: Verify all guide files exist and reference current project structure
- A-10: Verify content file dates are older than or equal to log and guide dates
- A-11: Verify no plaintext email addresses exist in project HTML files
- A-12: Verify family tree index links use trailing-slash URLs
- A-15: Verify contact pages use obfuscated email format
- A-16: Verify all skills and instructions reference correct paths
- A-17: Verify no T-numbers appear in guides, docs, or skills
- A-18: Verify encoding descriptions in docs match actual implementation
- A-19: Verify changelog entries use present tense
- A-20: Verify all todo files use present tense for task descriptions
- A-21: Verify session stats are regenerated after database changes
- A-22: Verify no local filesystem paths are exposed in backup databases
