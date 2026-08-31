# Kilo AI Assistant Guide

## What is Kilo

Kilo is an AI coding assistant that works through a set of tools — file I/O, shell commands, web fetch, subagents, and more. Each conversation is a **session** that persists in a database.

## Architecture

```
┌─────────────────────────────────────────┐
│          Kilo CLI / VS Code Extension    │
├─────────────────────────────────────────┤
│  Session Manager  │  Tool Router         │
│  Agent Manager    │  Skill Loader        │
├─────────────────────────────────────────┤
│  Built-in Tools (read, write, bash, etc) │
│  Subagent System (task tool)            │
│  Plugin/MCP Support                     │
└─────────────────────────────────────────┘
                               │
                               ▼
                SQLite Database (kilo.db)
                Tables: session, message, part
```

## Installation & Setup

### Prerequisites
- Python 3.10+ (for CLI mode)
- VS Code 1.85+ (for extension mode)

### VS Code Extension
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Kilo"
4. Install the extension
5. Configure credentials via `kilo config`

### CLI Mode
```bash
pip install kilo
kilo config
```

### First-Time Setup
1. Run `kilo` in your project directory
2. Kilo auto-detects project structure
3. Create an `AGENTS.md` file at project root for project-specific instructions
4. Configure `.kilo/kilo.json` for advanced settings

## Configuration

### AGENTS.md
At project root. Instructions Kilo reads at session start. Define conventions, build/test commands, paths.

### kilo.json (optional)
Structured config at project root: model override, permissions, API providers.

### Commands (.kilo/command/)
Markdown templates for common tasks. Run with `/command-name` in Kilo chat.

### Agents (.kilo/agent/)
Reusable agent personas with system prompt, required tools, and model preferences.

### Skills (.skills/)
Pre-written workflows providing specialized instructions. Each has Goal, When to Use, Prerequisites, Workflow, and Verification.

Load: `skill(name="kilo-config")`

See [skills-guide.md](../ai-dev-guides/skills-guide.md) for all available project skills.

## Sessions

### Storage
Sessions stored in SQLite database with three tables:

| Table | Purpose |
|-------|---------|
| `session` | Session metadata (ID, title, directory, tokens, cost) |
| `message` | Chat turns (user, assistant, tool) with JSON data |
| `part` | Individual content pieces (text, reasoning, tool calls/results) |

Database locations:
- Windows: `%LOCALAPPDATA%\kilo\kilo.db` or `~/.local/share/kilo/kilo.db`
- macOS: `~/Library/Application Support/kilo/kilo.db`
- Linux: `~/.local/share/kilo/kilo.db`

### Session Lifecycle
1. **Start** — New session created on first interaction
2. **Active** — Messages and tool calls accumulate
3. **Update** — `time_updated` changes with each message
4. **Close** — Session ends (idle timeout archives)
5. **Archive** — Old sessions can be archived

## How to Use Kilo

### Starting a Session
- Open Kilo in your project directory
- Kilo reads `AGENTS.md` automatically for conventions
- Each session gets a unique ID (`ses_xxxxxxxx...`)

### Interacting Effectively
- **Be specific**: include file paths, line numbers, expected outcomes
- **Batch independent actions**: multiple tool calls in one response
- **Use `todowrite`**. for multi-step tasks (3+ steps)
- **Load skills**: `skill(name="...")` for specialized guidance

### Tools Summary
| Category | Key Tools |
|----------|-----------|
| File I/O | read, write, edit, glob, grep |
| Shell | bash, background_process |
| Web | webfetch, websearch |
| Orchestration | task, agent_manager, skill |
| Utilities | todowrite, chart, suggest, question |

### Tool Usage Tips
- Batch independent calls in one response
- Use `workdir` parameter instead of `cd` in bash
- Quote paths with spaces using double quotes
- Always verify changes with `read` or `glob`
- Chain dependent commands: `cmd1; if ($?) { cmd2 }`

### Commands
- `/help` — Get Kilo help
- `/review` — Request code review (see [github-dev-guide.md](github-dev-guide.md))

## Exporting Sessions

Export sessions to markdown for persistence and analysis:

```python
import sqlite3, json, datetime

DB = r"path\to\kilo.db"
SESSION_ID = "ses_..."

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Get session info
c.execute("SELECT * FROM session WHERE id=?", (SESSION_ID,))
s = c.fetchone()

# Get and export messages
c.execute("SELECT id, data FROM message WHERE session_id=? ORDER BY time_created ASC", (SESSION_ID,))
messages = c.fetchall()

with open("export.md", "w", encoding="utf-8") as f:
    for msg in messages:
        data = json.loads(msg["data"])
        role = data.get("role", "unknown")
        f.write(f"## {role}\n\n{data.get('content', '')}\n\n---\n\n")

conn.close()
```

Or use the project script (multi-session backup):
```bash
python .dev-scripts/ai-assistant/ai-sessions-backup.py --db-path <kilo.db> --developer kilo-code --current-session
```

The script auto-discovers the current session from the developer's session knowledge folder or queries the database directly. See [skills-guide.md](../ai-dev-guides/skills-guide.md) for the `ai-session-backup` skill.

### Co-Developer Support

The project supports multiple AI co-developers, each with their own session directories under `.ai-activity/ai-sessions/`:

| Developer | Directory | Purpose |
|-----------|-----------|---------|
| `kilo-code` | `.ai-activity/ai-sessions/kilo-code/` | Primary Kilo session databases (most complete) |
| `kilo-code-2` | `.ai-activity/ai-sessions/kilo-code-2/` | Alternate Kilo session database |
| `opencode` | `.ai-activity/ai-sessions/opencode/` | OpenCodeco-developer sessions |
| `github-copilot` | `.ai-activity/ai-sessions/github-copilot/` | GitHub Copilot sessions |

Use `--developer <name>` to select which developer's session IDs to use. The script loads session IDs from `session-ids-*.json` keyed by developer name.

## Agent Manager

Orchestrate multiple AI sessions in parallel worktrees:

```python
# List all sessions
agent_manager(action="list")

# Start sessions
agent_manager(mode="worktree", tasks=[
  {"prompt": "Task 1", "name": "Task1", "branchName": "task-1"},
  {"prompt": "Task 2", "name": "Task2", "branchName": "task-2"}
])

# Control sessions
agent_manager(action="stop", sessionID="ses_xxx")
agent_manager(action="prompt", sessionID="ses_xxx", prompt="...")
agent_manager(action="move", sessionID="ses_xxx", sectionID="...")
```

## Troubleshooting

### Common Issues
| Problem | Fix |
|---------|-----|
| "OldString not found" | Check exact text, including whitespace |
| "Found multiple matches" | Add more surrounding context |
| Unicode errors | Ensure UTF-8 encoding; use `sys.stdout.reconfigure(encoding='utf-8')` |
| "Tool not found" | Check tool name and parameters |
| "No AGENTS.md found" | Create one at project root with project conventions |
| "Permission denied" | Check `.kilo/kilo.json` permissions config |
| Session too long | Start a new session for fresh context |

### Debugging
- Check database: Query `kilo.db` directly
- Export sessions: Save transcripts for offline analysis
- Use `background_process`: Run long commands, check logs later
- Verify file ops: Use `glob` and `read` to confirm changes

### Performance Tips
- Use grep: Faster than reading large files
- Limit glob depth: Use `max_depth` to avoid scanning large trees
- Background long tasks: Use `background_process` for servers/watchers

---

See also: [github-dev-guide.md](github-dev-guide.md) | [ai-transparency-guide.md](../ai-dev-guides/ai-transparency-guide.md) | [skills-guide.md](../ai-dev-guides/skills-guide.md)
