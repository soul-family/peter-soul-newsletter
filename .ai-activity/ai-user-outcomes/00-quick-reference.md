# 00 — Quick Reference

The tl;dr. Print this, read it before every session. Each card is one rule;
full reasoning lives in `01`–`05`.

## Pre-flight (2 minutes, before the first message)

- [ ] I know what I want the end state to look like (I can describe the *result*, not just a keyword).
- [ ] I know which files are involved — paths noted, or at least which directory.
- [ ] I have the error message / stack / log text ready if this is a bug.
- [ ] I've decided the constraints (stack, deps allowed, platform, perf, style).
- [ ] I've decided what "done" is, and which command proves it (test, lint, build).
- [ ] I've picked ONE task for this session. The rest go in a notepad for later sessions.

If any box is unchecked, spend the extra 30 seconds now. It buys you 5–10 turns later.

## Cards

### C1. One task per message
Send one complete task per message. Three asks in one message → each descoped
and checked separately. Fewer than 10 words is usually too vague; more than
three sentences usually means it's two tasks.
→ See `01`.

### C2. Name the files
Put paths in the first message: `src/services/auth.ts`. No "the file that does
auth". If you don't know the path, say so once — the AI will find it, and that
search is a *planned* step, not drift.
→ See `02`.

### C3. Constraints upfront
Before the work starts: language/framework, forbidden additions, environments,
bounds. A constraint given mid-build is a correction; a constraint given early
is free.
→ See `02`.

### C4. Define "done"
End the task with the verifiable proof: `"…and run the tests"`, `"…and run
`npm run typecheck`"`, `"…and show me the diff"`. Unspecified "done" → the AI
picks one, and it's usually "no tests".
→ See `04`.

### C5. Correct within 1–2 turns
If the direction is wrong, redirect immediately with what's wrong *and* what
the right direction is. Correcting after the whole build → a re-request, the
costliest stat you have.
→ See `03`.

### C6. Yes/no, no hedges
Drop "maybe", "if possible", "I think", "roughly". Commitment in, commitment
out. If you genuinely don't care, literally write "either is fine".
→ See `01`.

### C7. Review before accept
Every accepted AI change goes through: diff review → tests/lint (unless C4
deferred) → then "it's done". "Looks fine" without running anything is how
regressions slip.
→ See `04`.

## Anti-pattern cheat sheet

| Anti-pattern | Symptom in stats | Replace with |
| --- | --- | --- |
| "fix it" (no target) | vague ask, high re-requests | exact failure + expected behaviour |
| "make it better" | scope drift, repeated rewrites | measurable improvement or concrete metric |
| message of 5 sentences | cramming, partial deliveries | 3 separate messages |
| "maybe X would be nice" | hedged half-baked output | yes or "either is fine" |
| waiting 10 turns to course-correct | re-request storm, backtracking | correct at turn 1–2 |
| "run it and see" with no error text | AI re-runs identical commands | paste the actual error |
| accepting without tests | outcome "partial", later bug sessions | define the proving command |
| same task across 3 sessions | task replaced stat high | finish or explicitly abandon, don't drift |

## Rules that fix each red stat

- High user re-requests → C5 (correct early) + C1 (one task).
- High AI re-runs → C2 + C3 (give error text and constraints so it stops guessing).
- No search-before-edit → C2 (give paths so it doesn't hunt mid-flight).
- High corrections / scope extensions → C3 + C4 (constraints + done upfront).
- Hedged group in 3.Clarity → C6.
- "done" without tests → C4.