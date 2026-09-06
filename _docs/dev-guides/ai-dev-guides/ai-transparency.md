# AI Transparency Guide

Guide for transparent AI-assisted development. Covers data governance, privacy, statistics, benefits, and AI-powered analysis.

## 1. AI Usage Overview

### Interaction Logging
AI assistants log all interactions for transparency:
- **Decisions** — Rationale behind key choices
- **Sources** — Research references and extractions
- **Tool usage** — Which tools were called and why
- **Session summaries** — High-level outcomes per session

### Data Storage
AI sessions are stored in a local SQLite database with three tables:
- `session` — metadata (ID, title, timestamps, token counts, cost)
- `message` — conversation turns (role, model, finish reason)
- `part` — content pieces (text, reasoning, tool calls/results)

All data stays on the local machine. No conversation content is shared with third parties.

### Transparency Principles
- One log entry per decision or significant action
- Structured format (tables, bullets) for readability
- No deletion of planning artifacts without explicit instruction
- Version-controlled logs provide audit trail

## 2. Data Governance

### Data Categories
| Category | Examples | Storage |
|----------|----------|---------|
| Session data | Prompts, responses, tool calls | SQLite database |
| Logs | Decisions, sources, tool usage | Version control (git) |
| Exports | Session transcripts | Local files (gitignored) |
| Code changes | Source code, configurations | Project directory |
| Credentials | API keys, passwords | Environment variables |

### Data Lifecycle
1. **Creation** — During active AI sessions
2. **Logging** — Immediately to structured logs
3. **Version control** — Logs committed; raw sessions gitignored
4. **Retention** — Logs kept indefinitely in git history
5. **Deletion** — Only on explicit user instruction

### Access Control
- Database file: local, user-controlled permissions
- Logs: visible to repository collaborators
- Credentials: never stored in files or logs

### Backup Strategy
- Version control serves as backup for structured logs
- Database backup: copy the SQLite file to a safe location
- No automated cloud backup of raw sessions

## 3. Data Privacy

### What Data is Collected
- User prompts and AI responses (full conversation)
- Tool call arguments and results (including file contents when read)
- File paths and project structure
- Timestamps, model used, token counts, cost

### What is NOT Collected
- System-level information beyond working directory
- Network requests (only URLs fetched via web tools)
- Passwords or secrets (never logged)
- Personal data beyond what is provided in the project

### Privacy Best Practices
- Review tool call results before they are logged
- Avoid pasting secrets, passwords, or sensitive data
- Use `.gitignore` to exclude sensitive files
- Regularly clean up exported session files after review
- Restrict database file permissions

### Compliance Considerations
- **GDPR**: Users can request deletion of session data
- **Data residency**: All data stays on the local machine
- **No third-party sharing**: Conversation content is not shared

## 4. Benefits

### Audit Trail
- Every decision traces to a session log entry
- File modifications recorded with context
- Useful for compliance, debugging, and knowledge transfer

### Reproducibility
- Structured logs define repeatable workflows
- Session transcripts can be replayed or referenced
- Decisions and rationale preserved for future review

### Learning and Improvement
- Review past sessions to identify patterns
- Analyze interaction quality over time
- Improve prompts and workflows iteratively

### Team Collaboration
- Logs can be shared via version control
- Documentation captures team conventions
- Workflows are shareable across team members

## 5. Statistics & Metrics

### Session-Level Metrics
| Metric | Definition | Purpose |
|--------|------------|---------|
| Messages per session | Total conversation turns | Session complexity |
| Tool calls per session | Number of tool invocations | AI activity level |
| Tokens per session | Input + output tokens | Resource consumption |
| Session duration | Time from first to last message | Efficiency |

### User Behaviour Metrics
| Metric | Definition | Interpretation |
|--------|------------|----------------|
| Prompt length | Average characters per user message | Specificity indicator |
| Clarification requests | User questions asking for details | Communication clarity |
| Revisions per task | Times user edits/adjusts requests | Task scoping |
| Approval rate | % of AI suggestions accepted | Trust and accuracy |
| Session restarts | New sessions vs. continuing | Context limits |

### AI Behaviour Metrics
| Metric | Definition | Interpretation |
|--------|------------|----------------|
| Tool diversity | Unique tools used | Versatility |
| Most used tool | Tool with highest call count | Efficiency focus |
| Error recovery attempts | Retries after failures | Robustness |
| Reasoning depth | Reasoning tokens vs. output | Thoughtfulness |
| First-attempt success | Tasks completed without revision | Quality |

### Collecting Statistics
```python
import sqlite3

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Session counts
c.execute("SELECT COUNT(*) FROM session")
total_sessions = c.fetchone()[0]

# Average messages per session
c.execute("""
  SELECT AVG(msg_count) FROM (
    SELECT session_id, COUNT(*) as msg_count
    FROM message GROUP BY session_id
  )
""")
avg_msgs = c.fetchone()[0]

# Most active tools
c.execute("""
  SELECT json_extract(data, '$.tool') as tool, COUNT(*)
  FROM part WHERE json_extract(data, '$.type') = 'tool-uses'
  GROUP BY tool ORDER BY COUNT(*) DESC LIMIT 10
""")

conn.close()
```

### KPI Dashboard Queries
- **Weekly activity**: Sessions created per week
- **Token consumption**: Daily/weekly token usage trends
- **Tool effectiveness**: Success rate per tool (successful vs. failed calls)
- **Task completion**: Sessions ended with user satisfaction vs. abandonment

## 6. AI Analysis

### Analyzing AI Usage Patterns
Use AI to analyze your own AI usage for optimization:

```python
import sqlite3, json, re
from collections import Counter

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Find most common user requests
c.execute("SELECT data FROM message WHERE json_extract(data, '$.role') = 'user'")
user_msgs = c.fetchall()

intent_patterns = []
for row in user_msgs:
    data = json.loads(row["data"])
    text = data.get("content", "")
    # Extract first 5 words as intent pattern
    words = text.split()[:5]
    intent_patterns.append(" ".join(words))

common_intents = Counter(intent_patterns).most_common(10)
for intent, count in common_intents:
    print(f"{count}x: {intent}")

conn.close()
```

### Session Stats Analysis
AI-powered session analysis reveals:
- Prompt specificity trends over time
- Tool usage efficiency improvements
- Common error patterns and failure points
- Session outcome comparisons (completed vs. abandoned)

### Pattern Recognition Questions
Ask AI to analyze session data:
- "What task types do I delegate to AI most often?"
- "Which tools are underutilized?"
- "Where do sessions most commonly fail or get abandoned?"
- "What is my average token cost per completed task?"
- "Are my prompts becoming more or less specific over time?"

### Metrics Dashboard Suggestions
| Category | Metrics | Tools |
|----------|---------|-------|
| Volume | Sessions/day, Messages/session | SQLite queries |
| Quality | Error rate, Revision rate | Part type analysis |
| Efficiency | Tool calls/task, Time/session | Timestamp deltas |
| Engagement | Approval rate, Clarification rate | Role-based analysis |

## 7. Implementation Checklist

- [ ] Structured logging enabled (decisions, sources, tools per session)
- [ ] Session data stored in encrypted local database
- [ ] Regular database backups configured
- [ ] Access permissions set (user-only read/write)
- [ ] No credentials stored in conversation logs
- [ ] Export capability tested and verified
- [ ] Privacy policy documented and communicated
