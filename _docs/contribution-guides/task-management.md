# Task Management

## Overview

Tasks are tracked using numbered files in the `.todo/` directory. This guide defines the file structure, numbering rules, and workflow for managing tasks across the archive project. Descriptions here are conceptual and remain true regardless of which specific tasks are assigned, moved, or renumbered.

## File Reference

| File | Purpose |
| --- | --- |
| `todo-next.md` | Active tasks |
| `todo-done.md` | Completed tasks |
| `todo-future.md` | Concepts and v2+ tasks |
| `todo-ignore.md` | Deprecated or excluded items |
| `todo-audit.md` | Reusable verification tasks |

## Numbering Rules

- **T-numbers** are assigned to actionable tasks.
- **Future concepts** in `todo-future.md` have no T-numbers. Promote to `next` when scoped into actionable work.
- **Ignored items** in `todo-ignore.md` have no T-numbers. Do not action.
- **Gap numbers** in `todo-audit.md` are reusable verification tasks. Run these tasks during project reviews and pre-commit audits. Gap numbers may be reassigned as the project evolves.
- T-numbers may be reassigned or reordered as the project evolves; the guide remains valid because it describes the numbering concept, not a fixed sequence.

## Audit Tasks

- `todo-audit.md` contains reusable verification tasks with gap numbers.
- These tasks verify project health across all areas: file dates, todo integrity, AI transparency, changelog, guides, encoding, hrefs, privacy, and documentation consistency.
- Run all applicable audit tasks before committing changes.
- Audit tasks do not expire; they remain in `todo-audit.md` and are executed repeatedly.
- See `_docs/dev-guides/audit/readme.md` for the audit guide.

## Task Design Rules

- Each task must describe a single **task-goal**: what is delivered, not how to do it.
- Only combine tasks if they are **tightly related** and **non-overlapping**.
- Tasks must not **intercross**: each task should be independently executable.
- Keep tasks grouped by conceptual phase, independent of which file they currently occupy.
- **Do not mark todo entries as "planned"** - tasks in `todo-next.md` are by definition upcoming work. Section headers should name the area of work, not restate that it is planned.

## Family Tree Work Phases

Tasks are grouped by conceptual phase. The set of active phases may grow or shrink as the project evolves; tasks move between phases and files as needed.

| Phase | Focus |
| --- | --- |
| Inventory | Public branches, assets, sources, and privacy boundaries |
| Structure | Branch folders, index page, about |
| Skills & Tools | AI activity, verification, scripts, and guidance |
| Privacy | Contact protection and living-person data safeguards |
| Verification | Links, images, HTML, accessibility, and offline browsing |
| Future | Mermaid conversion, source references, and family tree improvements |

## Task Lifecycle

Tasks flow through the following lifecycle, independent of specific task numbers or content:

1. **Concept** - captured in `todo-future.md` as a deferred idea or future work.
2. **Action** - promoted to `todo-next.md` with a T-number when scoped and actionable.
3. **Completion** - moved to `todo-done.md` when finished.
4. **Retirement** - moved to `todo-ignore.md` if deprecated or excluded.

## Workflow

1. Define or promote a task into `todo-next.md` and assign a T-number.
2. Execute the task following skill workflows.
3. On completion, move the entry to `todo-done.md`.
4. Log decisions and changes to `.ai-activity/` per AI transparency rules.

## Automation

- `task_management.py` validates no duplicate T-numbers exist between `todo-next.md` and `todo-done.md`.
- This check runs automatically as part of the Git pre-commit hook (`pre_commit_audit.py`).
- Pre-commit fails if duplicate T-numbers are detected.
