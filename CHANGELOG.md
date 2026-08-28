All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [unreleased]

### Changed
- Updated AI transparency skill to reflect archived skills and simplified workflow
- Updated documentation to remove v1 prep folder references and reflect v1.5 URL structure
- Filled in research log with actual project state and key findings
- Updated task management guide and tools log for current project state

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
- Commit prep verifier, date-aware backup, commit preparation, and date-aware pre-commit skills moved from `.skills/` to `.skills-archived/` (v1 migration complete)

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
- Windows-1252 byte encoding restoration with ISO-8859-1 charset declarations
- FILETIME DST fix for accurate Windows timestamp setting
- Present tense standardization across all non-archive documentation
- Changelog folder structure with versioned files and generator command

### Changed
- Restructure file paths from `html/` to `content/` and `content/columns/`
- Encoding recover to Windows-1252 byte encoding with ISO-8859-1 charset declarations
- Assets deduplicate across versions
- Original HTML preserve with path restructuring
- Navigation links standardized across all archive pages
- Pre-commit checks now verify documentation and privacy
- Date validation flexible for different filesystem behaviors
- Documentation filenames follow consistent pattern
- Documentation refers to "the Archive" instead of domain names

### Fixed
- Date mapper parsing for blog filenames
- Prep verifier handling of archive-extracted timestamps
- Duplicate skill registry entries
- Encoding corruption: preserve apostrophes and special characters

### Improved
- Columns page navigation correctly links to related content
- Main index pages properly organize blog posts and static pages
- Link checking understands folder-style URLs
- Archive preparation process more reliable and maintainable
