# Session History Template

> One file per session. The chronological companion to `ai-stats.md`: stats records **how much** of everything happened; this records **what happened, when, and why it mattered**. Fill the timeline from the same source export - event order must match the real transcript, never reconstructed.

## 0. References

| Field | Value |
| --- | --- |
| Session file | `_e.g. session_2026-08-29_1530.json_` |
| Title / topic | `_one-line summary, matching ai-stats.md_` |
| Paired stats | `_path to the ai-stats.md for this session_` |
| Duration span | `_first message → last message_` |

## 1. Arc (2–4 sentence narrative)

`_What the user wanted, what the AI reached for first, where it went off, how it got back on track, and what actually landed. Written after the timeline is complete, not before._`

## 2. Timeline

One entry per event, in order. Columns: `#` (turn/event number), `T` (type), `When` (timestamp or `+mm` relative), `Detail` (one line), `Note` (why it matters / link to a stats field).

Event types (use these tags): `ASK` user request · `CTX` user context (path, log, constraint) · `HEDGE` user hedge · `CRAM` multiple asks in one message · `CLAR` AI clarifying question · `SEARCH` read/glob/grep · `EDIT` write/edit · `RUN` bash · `FAIL` tool/command error · `RETRY` identical re-run · `CORR` user correction · `REDO` user re-request · `SCOPE` user scope-extension · `VERIFY` test/lint/ diff check · `ACCEPT` · `ABANDON` · `META` (plan change, backtrack).

| # | T | When | Detail | Note |
| --- | --- | --- | --- | --- |
| 1 | ASK | **t0** | `"fix the login redirect"` | vague - no file, no expected behaviour (`ai-stats.md` 3.Clarity) |
| 2 | SEARCH |  | glob for `*login*`, reads `src/pages/login.tsx` | hunt begins because no path given |
| 3 | CTX |  | user pastes error + path after 2 turns | arrived late - cost turns 2–3 |
| … |  |  |  |  |

## 3. Turning points

Marked by turn number, in order.

- **First direction taken:** `_# - the AI's opening approach; was it right?_`
- **First deviation / wrong turn:** `_# - what drifted; did the user correct within 2 turns?_`
- **First failure:** `_# - what failed (test, edit miss, rerun)_`
- **Repeated failure (loop):** `_# → # - how many identical attempts before a change_`
- **First success:** `_# - what worked_`
- **Course-corrections:** `_# (early) / # (late) - whether they landed before or after build_`
- **"Done" declared:** `_# - was a proving command run before this (see ai-training 04)_`

## 4. User decisions at each crossroad

Every point where the user had a real choice, what they chose, and the cost:

| At turn | Choice | Chose | Cost / benefit |
| --- | --- | --- | --- |
| **3** | let the AI keep hunting vs. give the path | kept waiting | +2 wasted turns |
| **7** | repeat "no, not that" vs. give the correct direction | repeated | `REDO` count +1, no new info (`ai-training` 03.3) |

## 5. AI process trail

- Order it searched: `_e.g. login.tsx → authStore.ts → hooks/useAuth.ts; skipped tests/_`
- Verified with: `_commands run (tests/lint/typecheck) and results, in turn order_`
- Verified nothing: `_turns where output shipped without any checking_`
- Loop points: `_what it re-ran / re-read without learning (matches ai-stats 4.Process)_`

## 6. Cost / value ledger

| Activity | Turns spent | Value |
| --- | --- | --- |
| Hunting / searching | `_n_` | `_found file, low value_` |
| Building / editing | `_n_` | `_core value_` |
| Fixing own mistakes | `_n_` | `_rework_` |
| Answering clarifications | `_n_` | `_would have been 0 with a path_` |
| User course-correcting | `_n_` | `_$if repeated: buy back ~n turns by giving path/constraint up front$_` |

## 7. Lesson (the moral of the session)

`_One paragraph: what happened in story form and the single most concrete thing that would have changed the outcome. Cross-check against ai-stats.md Section 6 and the ai-user-training/ rule that matches._`
