# Audit Guide

Repeatable verification tasks for the Archive project. Audit tasks are not tied to specific releases or task numbers. They are gap-numbered checks that can be run at any time during project reviews, pre-commit audits, or maintenance windows.

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

## Task File

The canonical list of audit tasks is `.todo/todo-audit.md`. That file is the single source of truth for audit task IDs and descriptions. This guide explains how to use it; it does not duplicate the task list.

## Task Numbering

Audit tasks use gap numbers (e.g., A-2, A-3, A-10). Gap numbers may be reassigned as the project evolves. Do not reuse an active audit number for a different check unless the original check is retired.

## Adding New Audit Tasks

1. Identify a repeatable verification that is not already covered.
2. Assign the next available gap number in `.todo/todo-audit.md`.
3. Write the task as a check, not an implementation: "Verify ...", not "Add ..." or "Fix ...".
4. Update this guide if the new task introduces a new audit category.

## Integration with Pre-Commit

The pre-commit audit (`pre_commit_audit.py`) runs a subset of these checks automatically. Manual audits cover checks that require human judgment or access to external systems.

## See Also

- `_docs/contribution-guides/task-management.md` — Task lifecycle, numbering rules, and file conventions
- `.todo/todo-audit.md` — Active audit tasks
- `.todo/todo-next.md` — Active implementation tasks
- `.todo/todo-done.md` — Completed implementation tasks
