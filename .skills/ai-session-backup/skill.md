# AI Session Backup Skill

## Goal

Export AI co-developer session data from the local SQLite database into project-specific backup databases, anonymizing all local filesystem paths to avoid exposing the local directory structure.

## When to Use

- When archiving AI co-developer sessions for long-term storage
- Before pushing session data to a shared repository
- When offline analysis of sessions is needed
- When local paths must be hidden from collaborators

## Prerequisites

- Access to the AI co-developer SQLite database
- The session backup tool
- Database schema documentation
- Session IDs to back up (from project session lists or auto-discovered from the current session)
- Output directory for backup databases

## Workflow

### Step 1: Identify Session IDs

1. Query the local AI co-developer database for session IDs belonging to the target project
2. Group sessions by project (e.g., website, famtree)
3. Session IDs can be listed in project-specific session list files or auto-discovered

### Step 2: Run the Backup Tool

Provide the database path and session IDs via command-line arguments or configuration:

- The database path argument points to the source SQLite database
- The developer selection argument chooses which AI co-developer's session IDs to load
- The current session flag auto-discovers the most recent session from the developer's session directory or by querying the SQLite database directly

If session-specific options are omitted, the tool loads defaults from project configuration files.

If no session IDs are found in configuration or arguments, the tool falls back to interactive mode.

### Step 3: Verify Output

1. Confirm backup databases are created in the output directory
2. Verify path anonymization by checking that the replacement placeholder appears instead of local paths
3. Review generated statistics files for per-session counts and totals
4. Confirm session, message, and part counts match expected data

### Path Anonymization

The path replacement function generates all slash-form variations automatically. The configuration files only need to list each base path once.

## Output Format

Backup databases and statistics files are created in the output directory:

- Project-specific session databases and corresponding statistics files

Each backup database contains three tables:

| Table | Purpose |
| --- | --- |
| Session metadata | Session identifiers, titles, directories, tokens, and cost |
| Message | Conversation turns with role, model, and finish reason |
| Part | Content pieces including text, reasoning, and tool calls or results |

Each statistics file contains:

- Database filename reference
- Generation timestamp
- Total counts across all sessions
- Per-session statistics including identifiers, titles, directories, timestamps, and message or part counts

## Verification

- [ ] Backup database files exist in the output directory
- [ ] Statistics files exist alongside databases
- [ ] Session directories show the replacement placeholder instead of local paths
- [ ] No local project path strings found in any database column
- [ ] Session, message, and part counts match source database

## Notes

- The source database path is provided at runtime, not hardcoded
- Local paths are replaced with the placeholder before writing to the output database
- New AI co-developers can be added by extending the developer configuration and adding per-developer session ID and path replacement files
- After updating the backup database, regenerate the statistics files so that per-session and project totals stay in sync with the database contents
