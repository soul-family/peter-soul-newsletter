# Task Management

## Overview

Tasks are tracked using numbered files in the `.todo/` directory. This guide defines the file structure, numbering rules, and workflow for managing tasks across the archive project. Descriptions here are conceptual and remain true regardless of which specific tasks are assigned, moved, or renumbered.

## File Reference

| File | Purpose |
|------|---------|
| `todo-next.md` | Active tasks with T-numbers |
| `todo-done.md` | Completed tasks with T-numbers |
| `todo-future.md` | Concepts and v2+ tasks without actionable T-numbers |
| `todo-ignore.md` | Deprecated or excluded items (no T-numbers) |
| `todo-audit.md` | Reusable verification tasks (gap numbers reused across sessions) |
| `todo-familytrees.md` | Family tree tasks (migrating to separate repository) |

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

## Task Design Rules

- Each task must describe a single **task-goal**: what is delivered, not how to do it.
- Only combine tasks if they are **tightly related** and **non-overlapping**.
- Tasks must not **intercross**: each task should be independently executable.
- Keep tasks grouped by conceptual phase, independent of which file they currently occupy.

## Migration Phases

Tasks are grouped by conceptual phase. The set of active phases may grow or shrink as the project evolves; tasks move between phases and files as needed.

| Phase | Focus |
|-------|-------|
| Consulting | Archive purpose, boundaries, stakeholder alignment |
| Planning | Content capture, structure extraction, inventory, AI artifacts |
| Skills & Tools | AI activity, skills folder, verification, scripts, guidance |
| File & Folder Planning | Research, sitemap, schema, routing, prep folders, commits |
| v1 Migration | Capture, extraction, inventory, AI artifacts, HTML5 update |
| v1 Family Trees | Separate family trees into folders, credits page, commit0-familytree prep |
| Execution | Documentation, guidance, deployment, legal, retention |
| Future | v2+ research, deployment, family tree Mermaid conversion |

## Task Lifecycle

Tasks flow through the following lifecycle, independent of specific task numbers or content:

1. **Concept** — captured in `todo-future.md` as a deferred idea or future work.
2. **Action** — promoted to `todo-next.md` with a T-number when scoped and actionable.
3. **Completion** — moved to `todo-done.md` when finished.
4. **Retirement** — moved to `todo-ignore.md` if deprecated or excluded.

## Workflow

1. Define or promote a task into `todo-next.md` and assign a T-number.
2. Execute the task following skill workflows.
3. On completion, move the entry to `todo-done.md`.
4. Log decisions and changes to `.ai-activity/` per AI transparency rules.

## Automation

- `task_management.py` validates no duplicate T-numbers exist between `todo-next.md` and `todo-done.md`.
- This check runs automatically as part of the Git pre-commit hook (`pre_commit_audit.py`).
- Pre-commit fails if duplicate T-numbers are detected.
