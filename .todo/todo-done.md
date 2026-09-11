# Todo — Done

Completed work from the todo-next.md file.

> **Contribution rules**: All entries must follow future-proof naming conventions. See `_docs/contribution-guides/shared/adding-text.md` for rules on avoiding file names, function names, and implementation-specific details in permanent records.

## Consulting

- T-1: Confirm migration consent
- T-2: Establish hosting and preservation on GitHub
- T-3: Define archive purpose, audience, and success criteria
- T-4: Create GitHub organisation for Soul Family with separate repositories
- T-5: Validate author intent and preservation boundaries
- T-6: add Readme and License files

## Github date-aware migration

- T-11: Obfuscate contact email addresses on contact pages

- T-30: Capture and preserve original website files (HTML, CSS, scripts, images)
- T-31: Extract content structure, metadata, and publication dates
- T-32: Document original design and visual styling
- T-33: Preserve author text exactly as published
- T-34: Create inventory of all source files and assets
- T-35: Verify backup completeness
- T-36: Preserve AI-generated migration code and planning artifacts
- T-37: Maintain transparency log for all decisions and interactions

- T-17: Fix progressive index pages for all preparation commits
- T-18: Verify index pages exist for all column commits
- T-19: Create shared utilities for managing navigation links across all pages
- T-20: Fix all navigation links in preparation folders
- T-21: Add verification checks to ensure links work correctly
- T-22: Add privacy checks to prevent personal data exposure
- T-23: Reorganize documentation into topic-based folders
- T-24: Standardize documentation filenames
- T-25: Remove unnecessary domain references from documentation
- T-26: Create admin guide for managing archive access
- T-27: Create user guide for requesting archive changes
- T-28: Create user guide for submitting new information
- T-54: Remove external search forms from all pages
- T-55: Remove all plaintext email addresses from family tree HTML pages
- T-56: Obfuscate contact email addresses on contact pages
- T-57: Add privacy policy for living family members to family-trees guide
- T-58: Remove empty notes page from archive and all references
- T-59: Update family tree index links to trailing-slash URLs
- T-60: Set all prep commit file meta dates to corresponding newsletter post creation dates
- T-61: Set commit0-famtree meta dates to first column post date.
- T-62: Fix progressive index pages encoding and filtering for all prep commits
- T-63: Verify index pages are created for all 167 column commits

## Github Family Trees migration

- T-7: Separate each family tree into its own folder with index pages
- T-8: Create credits pages for family tree attribution
- T-9: Move family tree files into dedicated commit preparation folders

## v1.5.0 Modernisation

- T-38: Update to modern HTML standards
- T-42: Modernise table-based layout structure
- T-43: Update contact information for the archives
- T-44: Remove outdated email assets and references
- T-45: Improve file structure
- T-46: Create archive guides
- T-47: Create management guides
- T-48: Add updates and report files
- T-52: Review and update newsletter post metadata and dates for consistency.
- T-53: Convert newsletter content to Markdown for v2 static site generation.
- T-66: Encode pages to UTF-8
- T-67: Convert to HTML5, replace table layouts with div-based structure
- T-68: Extract styling using CSS3 variables
- T-69: Remove duplicate images
- T-71: Add captions under all images with rights info
- T-73: Standardize column URLs for consistency
- T-74: Add column post title to each page
- T-75: Update changelog management guide to describe unreleased workflow
- T-76: Remove right sidebar, move portrait to header and cars to left sidebar
- T-77: Create human-readable statistics report in the project documentation
- T-78: Create AI development project totals report in the project analysis directory
- T-99: Document backup preparation process and issues (missed links, restructuring, text relocation)
- T-101: Clean local AI session backups and enhance backup script with append mode
- T-102: Update documentation management with contribution guidelines and self-contained docs policy
- T-108: Add version file management and synchronization

## AI Tooling and Dev Guide Updates

- T-80: Remove GitHub CLI section from GitHub dev guide; add commit metadata documentation
- T-81: Merge duplicate troubleshooting content into AI assistant dev guide; remove obsolete project guide
- T-83: Rename uppercase filenames in ai-logs to lowercase
- T-84: Write documentation content for AI activity subdirectories
- T-85: Update all cross-references for folder restructure across documentation and scripts
- T-86: Create session backup script with configuration loading
- T-87: Add session identifier and path replacement configuration files
- T-88: Create session backup skill definition
- T-89: Create skills guide with skill calling syntax and benefits
- T-90: Back up AI sessions as anonymized databases
- T-91: Separate transparency skill from session backup skill
- T-92: Add session database directories to version control ignore
- T-93: Add multi-AI-developer support to session backup
- T-94: Add current session auto-discovery
- T-95: Simplify path replacement configuration to human-friendly format
- T-96: Move session databases to shared co-developer directory
- T-97: Generate per-session statistics files with counts and tokens
- T-98: Add tiered word-count user input time calculation
- T-79: Document session stats units and time calculation methodology
- T-103: AI logging guidelines - created contribution doc for future-proof logging
- T-104: Stats calculation update - comprehensive user input time model
- T-50: Add page footer fixed to bottom of viewport across all screen sizes
- T-82: Keep original images in print-ready format alongside web-optimized versions
- T-105: Separate stats generation from backup script into standalone tool
- T-106: Fix cross-references across documentation files
- T-107: Normalize stats field names to user_activity_* across all databases and reports
- T-108: Update ai-reports with normalized user_activity naming and human-readable totals
- T-109: Add famtree database support to stats script with auto-detection
- T-110: Fix stats script overwrite bug and add multi-database config support
- T-111: Add automated pre-commit hook to verify session stats are regenerated after database changes
- T-112: Create contributor quick-start guide covering backup workflow, stats generation, and reporting in one place
- T-113: Add dry-run mode to backup script to preview sessions and path replacements before writing
- T-114: Implement automated path-anonymization verification that scans all database columns for exposed local paths
- T-115: Add unit tests for stats script normalization and user activity calculation
- T-116: Create session auto-discovery utility that queries the source database for project-relevant sessions
- T-117: Add database schema version and migration path to support future schema evolution without data loss
- T-118: Consolidate duplicate documentation files in `_docs/` that exist in multiple locations
- T-119: Clean up runtime cache directories in `.dev-scripts` and ensure they are gitignored
- T-121: Review and remove redundant per-developer documentation now that config is generalized
- T-122: Add `.ai-activity` retention policy and cleanup script to prevent unbounded growth
- T-123: Consolidate duplicate database schema files across `.dev-scripts/ai-assistant/*/` into a single shared source
- T-125: Add `.dev-scripts` cleanup script to remove stale caches and temporary files
- T-126: Implement database size monitoring for `.ai-activity/ai-sessions/*.db` to track growth trends
- T-127: Add automated duplicate detection to prevent future duplication in docs and configs
- T-128: Create unified session stats viewer that works across all developers without manual file selection
- T-129: Add session database integrity check to pre-commit audit
- T-130: Implement incremental backup deduplication to reduce database growth
- T-132: Create session stats dashboard script for quick project health overview
- T-133: Add SQLite VACUUM and integrity checks to backup workflow
- T-135: Add documentation link validation to pre-commit audit
- T-136: Implement backup database checksum verification
- T-137: Add automated session cleanup for temporary/scratch sessions
- T-138: Create unified stats aggregator across all developer databases
- T-140: Implement automated backup rotation strategy
- T-143: Implement message/part deduplication within backup databases
- T-144: Add database indexing on frequently queried columns for performance
- T-145: Create session archive manager for cold storage of old sessions
- T-146: Add automated cleanup of orphaned session files
- T-148: Add session metadata enrichment during backup
- T-149: Create database vacuum scheduler for periodic optimization
- T-150: Add incremental backup change detection using timestamps

- T-10: Separate the family tree content into its own dedicated repository
- T-12: Reduce family tree mentions in this repository's documentation to focus on the current newsletter archive
- T-13: Move family-tree-specific documentation to the new repository
- T-14: Update cross-references in remaining docs to point to the family tree repository
