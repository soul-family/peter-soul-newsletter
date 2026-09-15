# Service & Prompt Hooks (Automating the Rules)

Everything in the earlier guides is discipline: you *remember* to do it each session.
Hooks are the upgrade - they make the AI environment **do the discipline for
you**. Instead of trusting yourself to name files and demand tests every time,
you write the rule once into a hook and every session inherits it.

This file covers opencode's hook surface, split into the two families:

- **Service hooks** - fire around the *machine*: tool execution, permissions,
  commands, shell, events. They guard and observe what the AI does.
- **Prompt hooks** - fire around the *message*: chat send, params, headers,
  system-prompt and message transforms, compaction. They shape what the AI
  sees.

Hooks live in **plugins** - `.ts`/`.js` files in `.opencode/plugin/`
(auto-discovered) or registered via the `plugin` key in `opencode.json`.
A plugin exports a function that returns a hooks object; you mutate `output`
in place and return `void`.

```ts
import type { Plugin } from "@opencode-ai/plugin"

export default (async ({ project, directory, $ }) => {
  return {
    "tool.execute.after": async (input, output) => {
      // runs after every tool call
    },
  }
}) satisfies Plugin
```

Loading notes: config and plugins load at startup and are **not** hot-reloaded
- quit and restart opencode after adding/editing a hook. A broken hook (or
config shape) can stop opencode from starting; validate against
[`https://opencode.ai/config.json`](https://opencode.ai/config.json).

## The hook map - which hook does what

| Family | Hook | Fires when | Great for |
| --- | --- | --- | --- |
| prompt | `chat.message` | a chat message exists | logging, telemetry for your stats |
| prompt | `chat.params` | a request is about to be sent | shaping request params |
| prompt | `chat.headers` | provider request headers built | auth/env appends |
| prompt | `experimental.chat.system.transform` | system prompt assembled | injecting permanent rules / preamble (C1–C7) |
| prompt | `experimental.chat.messages.transform` | context messages assembled | auto-rewrites, context diet (05.4) |
| prompt | `experimental.text.complete` | streaming text | output observation |
| service | `tool.execute.before` | before any tool runs | blocking/rewriting risky calls (e.g. force `git` allow rules) |
| service | `tool.execute.after` | after any tool call | auto-run gate: after an edit, append a reminder to test |
| service | `permission.ask` | a permission prompt fires | overriding allow/deny for known patterns |
| service | `command.execute.before` | a slash command runs | pre-filling command context |
| service | `shell.env` | a bash tool spawns | injecting env vars (tokens, paths) |
| service | `event` | every bus event | full session telemetry → feeds `ai-stats.md` |
| lifecycle | `config` | once on init | pre-merging config defaults |
| lifecycle | `experimental.session.compacting`, `experimental.compaction.autocontinue` | on context compaction | preserving rules across a compaction |

## Automating each golden rule

The 7 rules from `README.md`, and the hook that enforces each so you stop
relying on your own memory:

| Rule | Manual fix | Hook automation |
| --- | --- | --- |
| C1 one task per message | split the message yourself | `chat.message` or `messages.transform`: detect cramming tokens ("also", "and then", bulleted list >1 item) and inject a prompt asking the AI to enumerate tasks and number them |
| C2 name the files | remember to type paths | `system.transform`: append `"Always begin by listing the file paths involved; if the user omitted one, ask before searching."` - turns hunting into an asked question |
| C3 constraints upfront | remember declarations | `system.transform`: append the static part of your preamble permanently; dynamic constraints still come from you |
| C4 define "done" | add a proving command | `tool.execute.after` on `edit`/`write`: if this turn touched code and no `bash`/test ran after it, inject `"You changed code. Before you finish, propose the test/lint command and offer to run it."` |
| C5 correct within 1–2 turns | correct fast yourself | can't be automated - but `tool.execute.after` can shrink the blast radius by making big unverified diffs visible |
| C6 no hedges | say yes/no | `messages.transform`: leave this to humans - rewriting your voice is not what you want; instead log hedges to telemetry so they show up in stats |
| C7 review before accept | review the diff | `tool.execute.after` on `write`/`edit`: require the result to include the file path + line count, making review cheap; or a `permission` gate `"edit": "ask"` until you trust the project |

## Telemetry hooks - feed your own stats

The session-stats skill you use to build `ai-stats.md`/`ai-history.md` parses
exports; `event` and `chat.message` hooks can emit the same data as JSONL so
your exports are already structured:

- `chat.message` → emit `{}` per message: role, length, hedge-flag,
  cramming-flag, file paths cited.
- `event` → emit tool events: tool, duration, success/error, identical-rerun
  flag (compare command+args to the previous event of the same session).
- `tool.execute.after` → tag edits rejected by "oldString not found" so your
  re-request/retry stats are captured at the source.

Write one line per event (`{"ts":...,"type":"tool","tool":"edit","ok":false}`) -
that file *is* a machine-readable transcript your skill can read directly.

## Guardrail hooks (permission as policy)

`permission.ask` + `permission` config turn guardrails into code instead of
vigilance:

```jsonc
{
  "permission": {
    "bash": { "git *": "allow", "rm -rf *": "deny", "*": "ask" },
    "external_directory": { "~/.ssh/**": "deny", "*": "allow" }
  }
}
```

Remember the two foot-guns from the schema: rules are evaluated **last-match
wins** (put broad first, narrow last), and `"permission": "allow"` at the top
level means *everything* is allowed - not "ask first". Start from `"ask"`.

A `permission.ask` hook can also reuse the stats/skill infrastructure to ask
you smarter: `tool.execute.before` seeing a `write` to a file you've
previously marked do-not-touch can inject a pre-empted question, or `deny`.

## Keep rules alive across compaction

When a session gets long, compaction rewrites the transcript (`tail_turns`,
`compaction.auto` in config). Rules injected once via `system.transform` are
safe - they re-apply on every request. Rules that lived only in your words get
lost. So: **anything you want to survive a long session goes in a hook or an
`instructions` file**, not in a one-off message:

```jsonc
{
  "compaction": { "auto": true, "tail_turns": 15 },
  "instructions": ["AGENTS.md", "ai-user-training/quick-reference.md"]
}
```

`instructions` files are fed to every session - they are the cheapest
permanent hook that needs no code.

## When hooks are the wrong answer

- **Your rules aren't stable yet.** Hooks codify behaviour; if your preamble
  changes week to week, a hook makes churn expensive. Use `instructions` +
  session preambles until the rules stop moving.
- **You're using a hook to fix a one-off.** A missed verification last
  session is a C4 failure, not a hook problem. Hooks pay off on *recurring*
  stats (your red stats across ≥3 sessions).
- **Voice:** never auto-rewrite your own prompt language - auto-de-hedging
  makes the AI output read as yours when it isn't. Log it to telemetry
  instead.

## Rollout plan

1. Pick your single most repeated red stat from the last batch of `ai-stats.md`.
2. Encode it as the *cheapest* layer first (`instructions` file or
   `system.transform` one-liner).
3. Run 2–3 sessions, re-export, re-run `session-stats` - did the stat move?
4. Only then add the code-grade hook (`tool.execute.after`, telemetry) -
   and stick a `config`-time guard on it so a bug in the hook fails loud,
   not silent.
5. Restart opencode after every plugin/config edit.