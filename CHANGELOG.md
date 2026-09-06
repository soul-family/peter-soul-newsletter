All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).


## [v1.6.1]

[unreleased]

> **Changelog rules**: Only record completed work here. Do not add planned tasks or todo items. See `_docs/contribution-guides/changelog-management.md` for full guidelines.

## Added
- Database schema JSON for AI session databases
- Database schema documentation for AI session databases
- Deduplicated AI user outcomes documentation
- Incremental stats generation with caching for existing sessions
- Config loader module for multi-AI-developer support
- Separate stats generation script with incremental processing support
- Famtree database developer config entry for stats script auto-detection
- Contributor quick-start guide for backup and stats workflow
- Dry-run mode for session backup script
- Automated path-anonymization verification script
- Unit tests for session stats normalization
- Session auto-discovery utility
- Database schema version table and migration support
- SQLite VACUUM and integrity checks in backup workflow
- Backup database checksum verification tool
- Documentation link validation in pre-commit audit
- Database indexes on frequently queried columns
- Session metadata enrichment during backup
- Database vacuum scheduler
- Orphaned session file cleanup utility
- Unified stats aggregator across all developer databases
- Session archive manager for cold storage
- Incremental backup change detection using timestamps
- `.ai-activity` retention policy and cleanup script
- `.dev-scripts` cleanup script for stale caches
- Duplicate documentation detection and consolidation
- Shared database schema source for all developers

## Changed
- AI activity logs updated to remove specific filenames and task references
- AI co-developer references generalized (no tool-specific mentions)
- AI logging guidelines created for future-proof log entries
- Agent documentation updated with contribution guidelines and changelog principles
- Anonymized project name mentions in session databases (conversation text)
- Backup script separated from stats generation
- Changelog entries made future-proof (removed specific filenames and paths)
- Cross-references fixed across all documentation files
- Documentation cross-references updated across all files
- Documentation reorganized into dedicated, self-contained guides
- Documentation updated with generalized AI co-developer references
- Famtree database anonymized (paths and project names)
- Generalized stats naming from user_input_* to user_activity_*
- Path anonymization improved to handle additional patterns
- Session backup script enhanced with append mode for incremental updates
- Session backup script now creates database if not existing, with safeguards against accidental deletion
- Session databases updated with current session entries
- Session stats script optimized with bulk data loading
- Stats calculation updated with separated input/output phases: writing prompts + waiting for output, reviewing response summary + verifying file changes
- Stats generation separated from backup script into standalone tool
- Stats guide documents updated with new methodology
- Stats normalization now removes old field names from output (user_input_*, user_writing_*, etc.)
- Stats totals now include human-readable duration fields
- Stats script auto-detects stats filename from database filename when developer config does not match
- Duplicate documentation files consolidated
- Per-developer placeholder documentation removed
- Database schema consolidated into single shared source
- Pre-commit audit enhanced with session stats and documentation link checks
- Todo files cleaned up to remove completed tasks and duplicates
- Todo hooks expanded with workflow cards for session start, backup, and commit
- Todo ignore list cleaned to remove completed items

## Fixed
- Broken cross-references in statistics reports and guides
- Normalization of cached session stats from older format
- Path replacement artifacts in documentation
- Stats script overwriting wrong database stats file when processing multiple databases
- Word distribution calculation in stats generation
- Duplicate documentation files in `_docs/`
- Stale `__pycache__` directories in `.dev-scripts`
- Redundant per-developer placeholder documentation
- Missing schema version table in existing backup databases
- Broken markdown links in documentation
- Duplicate task numbers in todo files

## [v1.6.0]

### Added
- Session stats documentation with tiered word-count user input time methodology
- AI development project totals report and human-readable statistics report
- Repository separation tasks for family tree migration
- Tiered word-count user input time calculation in stats JSON files
- Per-session word count distribution in stats JSON durations
- Stats documentation covering all field units and time calculations
- Project-wide aggregates report for AI development activity
- Human-readable stakeholder statistics report
- Stats JSON generation alongside session backup databases with per-session message/part counts, timestamps, and totals
- Multi-AI co-developer support for session backup with automatic current session discovery
- Session backup skill for exporting session data to anonymized SQLite databases
- Session analysis skill for reviewing transcripts for behavioural insights
- Skills guide documenting all active and archived skills

### Changed
- Updated AI transparency skill to reflect archived skills and simplified workflow
- Updated documentation to remove v1 prep folder references and reflect v1.5 URL structure
- Filled in research log with actual project state and key findings
- Updated task management guide and tools log for current project state
- Path replacement configuration simplified to human-friendly bare root paths
- About-archive guide reduced family tree mention to a single cross-reference
- Changelog management guide documents unreleased workflow
- AI development statistics report focuses on current archive work
- Session databases consolidated in shared co-developer directory
- Stats JSON user input time now uses tiered word-count estimation instead of flat rate
- Co-developer directory structure documentation updated
- Interaction and session log entries for co-developer support and database relocation work
- Session databases moved to shared co-developer directory
- Session backup script defaults to co-developer output directory
- Updated skills guide and dev guide to reference new database location
- Updated gitignore to exclude session database directories
- Path replacement configuration uses human-friendly root paths without drive letters
- Enhanced path variation generation to automatically generate all slash-form variations
- Updated session backup skill with co-developer and current session discovery documentation
- Added multiple AI co-developers to tools logs and research log
- Reorganized documentation with dedicated subfolder for AI-specific guides
- Moved session backup script to dedicated assistant scripts directory
- Updated script to load configuration from JSON files
- Updated skills guide and AI transparency skill to reflect current skills organization
- Updated all path references and cross-references for the new folder structure

### Removed
- v1 migration preparation folders and intermediate files
- Python cache directories from dev-scripts
- Obsolete gitignore entries for v1 migration temp folders

## [v1.5.0]

### Added
- HTML5 doctype and modern markup standards
- Column post titles to each page

### Changed
- Archive modernized to HTML5 doctype
- Table-based layouts converted to div-based structure
- Styling extracted using CSS3 variables
- Contact info with obfuscated email
- Column URL structure restructured for better navigation
- Documentation organized into topic-based folders

### Archived
- Migration-related skills moved from active to archived skills folder

## [v1.0.0]

### Added
- Original website content backup with complete migration workflow
- Establish archive repository with complete backup of original website content
- Create preparation folder structure for staged commit history
- Implement date mapping system to preserve original publication dates
- Developer tools for migration, verification, and Git operations
- AI transparency logging and task tracking practices
- Define archive purpose, audience, and preservation boundaries
- Organize GitHub repository with separate sections for columns and family trees
- Privacy safeguards including email removal and obfuscation
- Backdate Git commits matching original publication dates
- Link verification
- Privacy checks to prevent personal data exposure
- Documentation reorganized into topic folders
- Admin guide for archive access management
- User guides for requesting and submitting archive updates
- Multi-user access documentation with permission levels
- Updated archive to modern HTML5 standards while preserving original content
- Family tree folder structure with per-tree folders and shared credits page
- Progressive index pages for all prep commits
- Date-aware backup skill and commit preparation verifier
- AI transparency logging with structured audit trail
- Encoding restoration with ISO-8859-1 charset declarations
- Timestamp accuracy fix for Windows filesystem
- Present tense standardization across all non-archive documentation
- Changelog folder structure with versioned files and generator command

### Changed
- Restructure file paths for content organization
- Encoding recovery for special characters
- Assets deduplicate across versions
- Original HTML preserved with path restructuring
- Navigation links standardized across all archive pages
- Pre-commit checks now verify documentation and privacy
- Date validation flexible for different filesystem behaviors
- Documentation filenames follow consistent pattern
- Documentation refers to "the Archive" instead of domain names

### Fixed
- Date parsing for blog filenames
- Timestamp handling for archive-extracted files
- Duplicate skill registry entries
- Encoding corruption: preserve apostrophes and special characters

### Improved
- Columns page navigation correctly links to related content
- Main index pages properly organize blog posts and static pages
- Link checking understands folder-style URLs
- Archive preparation process more reliable and maintainable
