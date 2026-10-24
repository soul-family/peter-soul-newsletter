# Steering & Iteration

A session is a control loop. You set the direction, the AI executes, you correct. The skill is in **how early and how precisely** you correct - not in how much you correct.

This file is the antidote to two red stats: `corrections/redirects` and `re-requests` ("redo", "that's wrong", "try again").

## Timeliness beats thoroughness

The most expensive correction is the one that comes after the build. Waiting for a complete wrong thing "to see the whole picture" destroys more turns than you save.

Rule: the moment you see the direction is wrong, stop it. You don't need the finished product to know a wrong shape - a wrong shape is visible at turn 1.

Signals you should have corrected by turn 2, not turn 10:

- wrong file, wrong area of the code
- wrong approach / wrong library
- wrong interpretation of a requirement
- adds stuff you never asked for (scope is creeping early = headed for a later "no, not that" storm)

Correct early with a replay of the correct direction. The build cost you've already sunk is sunk; a re-request restarts it anyway.

## Corrections carry both halves

A correction has two parts and needs both:

1. what's wrong - `"you added MSW and set up a mock server"`
2. the correct direction - `"there's already a test double in test/utils; use that, and remove the MSW setup"`

Part 1 without part 2 makes the AI guess the replacement - often wrong again (second re-request). Part 2 without part 1 is an instruction amendment, which is fine when the work isn't wrong yet, but useless when it is.

## The re-request ladder - escalate, don't repeat

When output is wrong, climbing the ladder fixes it faster than repeating yourself:

| Rung | When | What you do |
| --- | --- | --- |
| 1. Same wording, louder | output mostly OK, small miss | `"the tooltip text is wrong - should read 'Save as draft'"` |
| 2. Add new info | the AI was missing something | add the error/constraint/file |
| 3. Lower the granularity | it got the concept wrong | `"don't touch pricing.ts. Do exactly: rename in config.ts only. Show me the diff before anything else."` |
| 4. Reset with full re-spec | it's lost the plot | start a new message with the full task re-written, explicitly noting what the previous attempt got wrong |

Repeating rung 1 never fixes a rung-3 problem. If the second `"no, that's not it"` comes from the same message, you've been on rung 1 twice - move up.

## Keep extensions out of the current task

When a completed task brings an obvious follow-up - `"also, while you're here…"` - resist. It reopens a closed loop, re-scopes the "done", and re-introduces the cramping failure mode.

Rules:

- Finish, accept, verify, then open a new message/task.
- If it's a genuinely small fix, at least say it's a new task: `"new task, unrelated to the last: …"`.
- Track deferred ideas in a notes file so they're not lost.

## Correct the spec, not the symptoms

If you want the AI to stop producing wrong things, look at what you fed it. Frequent corrections on the same topic mean the message is missing the constraint that would have prevented it. Two "no, not that" in a row on regular-expr design? The message needed `"no regex, use a small parser loop"`. Add the rule; the corrections stop.

## Say it once, correctly

Repeated instructions in the same wording (`repeat-of-own-message` in stats) signal the first message was ambiguous - repeating it louder won't help. Re-read your own message against the prompts guide (goal/boundaries/verify) before the second send. Usually one of the three is missing.

## Meta-commands when the AI is stuck

If the AI is circling (re-running the same command, re-reading the same files), steer with process commands, not content commands:

`"stop. Explain your current hypothesis in 2 lines, then list the files you've read and the ones you haven't, then read only the ones you haven't."`

This breaks the loop in a way that content feedback can't.
