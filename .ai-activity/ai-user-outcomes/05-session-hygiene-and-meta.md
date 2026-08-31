# 05 — Session Hygiene & Meta

Behaviour *around* the task: which sessions you open, what you carry into
them, and what you do with the noise. This is where the meta-stats live —
`task replaced`, request volume, abandoned tasks.

## 5.1 One session, one job

A session's context is finite and degrades as it fills. A session that has
done "login, footer, dark mode, that bug from yesterday" is a session where
the AI forgets the details of each. The stat `task replaced / repeated`
climbs exactly when jobs share a session.

Rules:

- Open a new session per deliverable. Login work → session A. Footer work →
  session B.
- If a session drifts onto a second task, finish the current task *first*,
  then open a new session for the second. Drifting is how "done" never
  happens and the `scope-extension` stat spikes.
- Reuse for the *same* job that's genuinely mid-flight; never as "I'll just
  ask in here".

## 5.2 Carry a stable preamble

Grease the start of every session with a tiny standard header. 15 seconds of
typing, removes a whole class of missing-context questions:

```text
Project: <name>
Stack: <lang/framework>
Conventions: <plain DOM, pattern from modules/user, eslint, etc.>
Constraints: <no new deps, must run on Node 18, etc.>
Task: <one line — the deliverable from 01>
```

Over time, this preamble becomes muscle memory and parts of it earn their own
`AGENTS.md` / CLAUDE.md so you only state the diff.

## 5.3 Make your project teach the AI (write an AGENTS.md)

If this is a real project, put the rules the AI keeps violating into an
`AGENTS.md` in the repo root: build/test command, code layout, naming,
what-not-to-touch, the commit style. Then every session inherits it and you
stop re-stating it (`2.5`).

## 5.4 Context diet

- Paste **only** what the task touches (see `02`). An AI with 10 stale files
  in context drifts to them.
- Delete/don't-paste finished diagnostics. Error messages that have been
  resolved are dead weight once the fix is confirmed.
- If the session feels sluggish or the AI starts repeating itself, that's the
  `compaction`/`context` warning — close the loop (accept or abandon) and
  start fresh rather than pushing forward.
- Name the noise: if you pasted a long log and only one line mattered, say so:
  `"only the first line of this log is relevant, ignore the rest"`.

## 5.5 Abandon honestly

A task you stop working on belongs in one of two buckets:

- **Done** — verified, accepted.
- **Abandoned** — say so out loud in the session: `"abandon this task for
  now, record what it needs in a notes file."` Leave a breadcrumb (a TODO, a
  note, a short file) so the next session can resume without rediscovery.

Neither bucket is "left hanging". An abandoned-but-unspoken task is what makes
`task replaced` stats climb, because a future session consumes it and
*calls it new*.

## 5.6 Start from the terminal state, not the story

For a bug/feature that has a history: don't narrate what happened last week.
Start from the current code + the current failure. The AI needs the *delta*,
not the saga (`2.6`). Write it as:

`"Current state: X. Failure: Y. Expected: Z. I've tried: A, B."`

`"I've tried"` is gold — it stops the AI from re-running A and B, which is
directly your `identical re-runs` stat.

## 5.7 Habits checklist (weekly)

- [ ] Did each session have one clear deliverable?
- [ ] Do any sessions show high `re-requests` or `corrections`? → re-read `03`.
- [ ] Is the preamble still accurate? Update it and the AGENTS.md.
- [ ] Any defensible ABANDONED breadcrumbs left for future you?
- [ ] Re-scan `ai-stats.md` Section 6 items from last batch — tick the ones you applied.