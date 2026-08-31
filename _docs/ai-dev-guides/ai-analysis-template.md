# Session Stats Template

> One file per session. Fill in values for a single exported session only —
> nothing here is aggregated across sessions. When a field has no data in the
> export, leave it as `N/A` (or `_unknown_`) rather than guessing.

## 1. Session Overview

| Field | Value |
| --- | --- |
| Session ID / file | `_e.g. session_2026-08-29_1530.json_` |
| Title / topic | `_one-line summary of what the task was_` |
| Started | `_timestamp_` |
| Ended | `_timestamp_` |
| Duration | `_hh:mm:ss (or N/A if not recorded)_` |
| Model(s) | `_primary model, small model, subagents_` |
| Total messages (user) | `_n_` |
| Total messages (assistant) | `_n_` |
| Total turns | `_n (user + assistant messages)_` |
| Token usage (if logged) | `_in / out / total_` |
| Task replaced / repeated | `_n (times this task was re-attempted across sessions)_` |

## 2. Message Times

> One row per message, in transcript order. Only fill if the export carries
> timestamps; otherwise mark the whole section `N/A` and pull what you can from
> `ai-history.md`. All `Δ` values are relative to the **previous** row.

### 2.1 Per-message table

| # | Role | Time | Δ | Dur | Tag | Words | Note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | user | `_ts_` | `_–_` | `_–_` | ASK | `_n_` | `_first task_` |
| 2 | assistant | `_ts_` | `_+m:ss_` | `_m:ss response_` | — | `_n_` | |
| 3 | user | `_ts_` | `_+m:ss_` | `_–_` | CTX | `_n_` | `_gave path late_` |
| … | | | | | | | |

Tags reuse `ai-history.md` types: `ASK, CTX, HEDGE, CRAM, CLAR, SEARCH, EDIT,
RUN, FAIL, RETRY, CORR, REDO, SCOPE, VERIFY, ACCEPT, ABANDON, META`.

### 2.2 Time aggregates

- Wall-clock session length: `_hh:mm:ss (first → last message)_`
- Work window (session resumed across hours/days): `_first TS → last TS_`
- AI response time (per assistant turn): avg `_m:ss_` / median `_m:ss_` / min `_m:ss_` / max `_m:ss_`
- User idle gaps (before each user message): avg `_m:ss_` / max `_m:ss_`
- Longest idle gap and what it preceded: `_m:ss — collected context / walked away / resumed later_`
- Response-time drift: first-half avg `_m:ss_` vs second-half avg `_m:ss_` — `_rising → context bloat or degraded focus; falling → habits are sticking_`
- Batching signal (user messages <60 s apart): `_n_` — `_cramming surrogate (see 3.Volume)_`
- Tool burst density: `_n_` tool calls in busiest `_m:ss_` window — `_machine grinding vs. stalling_`
- Time-of-day: `_start hour (e.g. 09:41 → morning session)_`

## 3. User Behaviour

### Volume
- User messages: `_n_`
- Avg words per user message: `_n_`
- Short (`<20 words`), medium, long (`>120 words`) split: `_n / n / n_`
- Request cramming (multiple distinct asks in one message): `_n_`

### Clarity
- Messages with a clear, explicit goal: `_n_`
- Vague / underspecified asks (no target, no acceptance criteria): `_n_`
- Messages giving relevant context (file paths, error logs, screenshots, constraints): `_n_`
- Messages referencing files by path: `_n_`
- Clarifying questions asked by the AI that the user *could* have answered upfront: `_n_`

### Steering
- Mid-task corrections / redirects ("no, do X instead"): `_n_`
- Re-requests, rejection of output ("redo", "that's wrong", "try again"): `_n_`
- Follow-up scope extensions ("also add …" after completion): `_n_`
- Changes from a stated plan/approach mid-session: `_n_`
- Times the user repeated the same instruction (unanswered first time): `_n_`
- Politeness/hesitation hedges ("maybe", "if possible", "I think"): `_n_`

## 4. AI Behaviour

### Volume & tools
- Assistant messages: `_n_`
- Tool calls total: `_n_`
- Tool call breakdown:
  - `write`: `_n_`
  - `edit`: `_n_`
  - `read` / `glob` / `grep`: `_n_`
  - `bash`: `_n_`
  - `webfetch` / `websearch`: `_n_`
  - other: `_n_`
- Tool calls that succeeded: `_n_`
- Tool calls that errored / failed: `_n_`
- Tool re-runs of the identical command: `_n_`

### Editing
- Files created: `_n_`
- Files edited: `_n_`
- Files deleted: `_n_`
- `edit`/`write` attempts rejected (`oldString not found`) and retried: `_n_`
- Lint / typecheck / test runs: `_n_; passed _n_`

### Process
- Search-before-edit (read/glob/grep before a write/edit): `_yes / no / partial_`
- First-attempt tool success rate: `_%_`
- Backtracking (reverted approach, rewrote own code): `_n_`
- Clarifying questions asked by the AI: `_n_`
- Abandoned / half-done tasks: `_n_`
- Unnecessary or wasted actions (redundant reads, speculative code): `_n_`

## 5. Outcome

| Metric | Value |
| --- | --- |
| Goal achieved | `_yes / no / partial_` |
| Final state verified (tests / lint / build pass) | `_yes / no_` |
| Blockers hit | `_n_` |
| AI hit a ceiling (model limit, wrong file, repeated failure) | `_yes / no — where_` |
| Turns until first useful result | `_n_` |
| Turns until completion | `_n_` |
| user satisfied signal (acceptance, thanks, no complaint) | `_yes / no_` |

## 6. What the User Could Do Better (if repeated)

> Honest, actionable, one line each. Only include items backed by evidence in
> this session; skip items that stayed fine.

1. `_e.g. Give the target file path up front — the AI spent 4 turns finding it._`
2. `_e.g. Split the 3-part request into separate messages — part 2 was redone._`
3. `_e.g. State "no dependencies" / stack constraints at the start._`
4. `_e.g. Ask for tests/lint to run before declaring done._`
5. `_e.g. Don't say "maybe" — commit to yes/no so the AI doesn't hedge._`