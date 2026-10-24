# Verification & Acceptance

Every accepted AI change passes a gate. Without a gate, "done" is whatever the AI says, and your outcome stat reports `partial` without you knowing.

## Define "done" in the task - the proving command

The cheapest verification is the one baked into the task message:

- `"…and run `npm test`/`pytest`/`cargo test` when finished"`
- `"…and run `npm run typecheck`"`
- `"…and run lint"`
- `"…and show me the diff / the new file when done"`
- `"…then trigger the failing command yourself and confirm it passes"`

Pattern: `"do X, then prove it with Y"`. A task with no proving command has an implicit, unspoken one, and it's usually "write the code and stop".

## The three checks before you accept

1. **Diff review.** Read what actually changed, not the summary. Look for:
   - edits to files you didn't ask about,
   - deleted code that was doing something,
   - secrets / stray logging / debug prints,
   - hard-coded values that should be config.
2. **The proving command.** Run it, or have it run. Passing = the task is green under the test that says so. That's the point of C4.
3. **The behaviour check.** For non-test-able output (UI, scripts, decisions): run it once and eyeball it, or read the diff line by line.

## Escalating acceptance

On doubts, ask for evidence, not reassurance:

| Doubt | Ask for |
| --- | --- |
| "did it actually change?" | `"show me the diff"` |
| "will this compile?" | `"run typecheck"` |
| "did this break anything?" | `"run the full test suite, not just the new tests"` |
| "is this the whole change?" | `"list every file you touched"` |

Buffer words from the AI - "should work", "probably fine", "looks good" - are not evidence. Demand the command output.

## Never accept "tests passed" without the suite scope

`"all tests pass"` can mean "the 3 tests in the file I just wrote pass". Clarify scope when it matters: `"which suite did you run - just the new tests or the whole project?"` For safety-critical tasks: `"run the full suite"`.

## Two-phase "done"

Separate **implemented** from **verified**:

- `implemented`: the code is written.
- `verified`: a command I can name proves the behaviour.

Say which one you mean. `"is it done?"` gets the AI's opinion; `"has the test suite passed on this change?"` gets a fact.

## Catch regressions in the same session

If the task touches a module with existing tests, add to the proving command: `"…run `pytest` - including the pre-existing tests in that module, I care that I didn't break those."` Discovering a regression two sessions later is the most expensive place to find it.

## When you reject: reject with evidence

A rejection without the evidence you saw is a re-request; a rejection that names the failing check is a correction:

`"I ran `npm run typecheck` myself and it errors at src/store.ts:40. Expected a string union, got a string. Fix that and re-run."`

This also halves the AI's `re-runs` - it stops guessing what could be wrong and fixes exactly what you proved is wrong.
