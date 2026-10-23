All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

> **Contribution rules**: All entries must follow `_docs/contribution-guides/shared/adding-text.md` file for rules.


## [v2.0.1]

### Added

- Add year-grouped column listing with month badges and year navigation
- Add newsletter access from mobile navigation
- Add arrow-only pagination in the title bar
- Add immediate in-page navigation that updates the reading area while the surrounding sidebars stay in place
- Add a distinct colour for each column, shown on hover and carried into the left sidebar while reading

### Changed

- Link the site title to home and reverse left sidebar header images
- Move GitHub Pages workflow to dev storage and optimise post-processing
- Restructure right sidebar for easier year and month browsing
- Present the archive introduction on the front page and streamline the navigation
- Sort the column list by publication date with the date above each title

### Fixed

- Correct missing spaces around emphasis and links across content
- Give the active navigation entry a clean, borderless appearance
- Keep sidebars in place with immediate in-page navigation and clean active states

## [v2.0.0]

### Added

- Links page collecting the external websites referred to across the columns
- Navigation entry for the links page ahead of the about page
- External links open in a new tab with a safe link relationship
- Floating navigation panel that opens on hover when the sidebar is collapsed
- Pinned navigation state for tablet screens where the panel stays open

### Changed

- Design sidebar moved to the right of the main content
- Main content border moved to the left edge beside the design sidebar
- Left sidebar collapses automatically on tablet and small screens
- Discontinued external destinations replaced with pages carrying the same information

### Fixed

- Broken external links replaced with working equivalents
- Design sidebar background no longer overridden by the right sidebar rule

### Added

- Two-column layout with collapsible left sidebar (300px expanded / 50px collapsed)
- External sidebar.js (IIFE pattern) with cookie-persisted toggle state
- Navigation via sidebar.md + markdownify pattern in navigation.html
- Custom Liquid pagination for column articles (sorting site.pages by date)
- Sticky post pagination with format: {←} {→} {Month Year} {Post Title}
- External link indicator (↗) via CSS ::after pseudo-element
- GitHub Action sed step converting .md links to directory URLs
- _docs/contribution-guides/jekyll-markdown-links.md documenting .md link convention
- Column cross-reference paths fixed for correct resolution after Jekyll build

### Changed

- Restructured from content/ to columns/ flat structure (168 articles)
- Removed right sidebar entirely; header images moved to sidebar-design
- Main content: 4px right border in original color (#07038d)
- Front page column list reversed (newest first, oldest bottom)
- Grid transition-delay sequencing for smooth collapse/expand animations
- Sidebar toggle moved inside <aside> as .sidebar-toggle with ▶/◀ icons
- Site title centered; .sidebar-expander button removed
- collections config removed; retained collections_dir: "src-content"

### Fixed

- Column article cross-references: ./YYYY/MM/ → ../../../YYYY/MM/
- Home link uses {{ site.baseurl }}/ instead of index.md for pretty permalinks
- Pagination prev/next arrows correctly positioned left of date/title
- External links only marked on public site via CSS (not HTML modification)

## [v1.7.0]

### Added

- Database schema JSON for AI session databases
- Database schema documentation for AI session databases
- Deduplicated AI user outcomes documentation
- Incremental stats generation with caching for existing sessions
- Config loader module for multi-AI-developer support
- Separate stats generation into standalone tool
- Auto-detect developer configuration from database metadata
- Contributor quick-start guide for backup and stats workflow
- Dry-run mode for session backup
- Automated verification of path anonymization
- Unit tests for session stats normalization
- Session auto-discovery utility
- Database schema version table and migration support
- Database optimization and integrity checks in backup workflow
- Backup database checksum verification tool
- Documentation link validation in project audit
- Database indexes on frequently queried columns
- Session metadata enrichment during backup
- Database vacuum scheduler
- Orphaned session file management utility
- Unified stats aggregator across all developer databases
- Session archive manager for cold storage
- Incremental backup change detection using timestamps
- AI-activity retention policy
- Cleanup stale caches
- Duplicate documentation detection and consolidation
- Shared database schema source for all developers
- HTML5 doctype and modern markup standards
- Column post titles to each page

### Changed

- AI co-developer references generalized
- Agent documentation updated with project contribution rules
- Anonymized project name mentions in session databases
- Session backup and stats generation separated into independent workflows
- Cross-references updated across all documentation
- Documentation reorganized into dedicated, self-contained guides
- Documentation updated with generalized AI co-developer references
- Anonymized paths and project names in backup database
- Generalized stats field naming convention
- Path anonymization improved to handle additional patterns
- Session backup supports incremental updates via append mode
- Session backup creates target database when missing, with safeguards against accidental deletion
- Session databases updated with current session entries
- Session stats generation optimized with bulk data loading
- Stats calculation methodology updated with separated input/output phases
- Stats generation separated from backup workflow
- Stats guide documentation updated with new methodology
- Stats normalization removes obsolete field names from output
- Stats totals include human-readable duration fields
- Stats generation auto-detects output filename from database metadata
- Duplicate documentation files consolidated
- Shared documentation serves as single source of truth
- Database schema consolidated into single shared source
- Project audit enhanced with session stats and documentation link checks
- Active task list reflects current work only
- Task workflow hooks expanded with standard session stages
- Task lists organized by current and completed work
- Archive modernized to HTML5 doctype
- Table-based layouts converted to div-based structure
- Styling extracted using CSS3 variables
- Contact info with obfuscated email
- Column URL structure restructured for better navigation
- Documentation organized into topic-based folders
- Statistics documentation cross-references validated
- Normalization of cached session stats from older format
- Documentation references canonical path replacement source
- Stats generation isolates database-specific stats during processing
- Word distribution calculation added to stats generation
- Duplicate documentation consolidated
- Version control ignores local Python cache directories
- Per-developer placeholder documentation consolidated into shared source
- Missing schema version table added to existing backup databases
- Broken markdown links in documentation fixed
- Duplicate task numbers resolved in task tracking
- Session backup references database schema for discoverability
- Session backup append mode preserves existing data while adding missing entries
- Read-only path replacement configuration support
- Path replacement rules deduplicated across fallback locations
- Documentation and skills updated with correct script paths

### Fixed

- Duplicate session discovery function definition resolved
- Path replacement configuration now loads from the canonical configuration location
- Duplicate path replacement rules deduplicated
- Incorrect script paths corrected in documentation guides
- Session backup documentation now includes database schema reference
- Streamline page footers to copyright-only content
- Replace vague inline link text with descriptive link text for external references
- Restrict sticky sidebar behavior to large-screen layouts
- Consolidate report documentation into version-specific subdirectories
- Move header images from right sidebar to header middle container
- Make site title clickable linking to home
- Add license link to left sidebar navigation
- Move copyright line from footer to end of main content
- Update columns index to year-grouped list with clickable titles
- Keep self portrait visible on small screens
- Add previous/next arrow navigation to post-date
- Make pagination titles clickable with correct page titles
- Replace generic "here" links with descriptive link text for external references

## [v1.6.0]

### Added

- Session stats documentation with tiered word-count user input time methodology
- AI development project totals report and human-readable statistics report
- Repository separation tasks for family tree migration
- Tiered word-count user input time calculation in session statistics
- Per-session word count distribution in session statistics
- Stats documentation covering all field units and time calculations
- Project-wide aggregates report for AI development activity
- Human-readable stakeholder statistics report
- Session statistics generated alongside backup databases with message and part counts
- Multi-AI co-developer support for session backup with automatic current session discovery
- Session backup skill for exporting session data to anonymized SQLite databases
- Session analysis skill for reviewing transcripts for behavioural insights
- Skills guide documenting all active and archived skills

### Changed

- AI transparency skill updated to reflect archived skills and simplified workflow
- Documentation updated to reflect current archive structure
- Research documentation updated with current project state
- Task management and tools documentation updated
- Path replacement configuration simplified to human-friendly bare root paths
- Changelog management guide documents unreleased entry workflow
- AI development statistics report focuses on current archive work
- Session databases consolidated in shared co-developer directory
- Session statistics time estimation uses tiered word-count model
- Co-developer directory structure documented
- Activity log entries document co-developer support and database relocation
- Session databases moved to shared co-developer directory
- Session backup defaults to co-developer output directory
- Skills and development guides updated for new database location
- Version control ignores session database directories
- Path replacement configuration uses human-friendly root paths without drive letters
- Path variation generation enhanced to handle all slash-form variations
- Session backup skill updated with co-developer and current session discovery
- Multiple AI co-developers added to tools and research logs
- Reorganized documentation with dedicated subfolder for AI-specific guides
- Session backup relocated to dedicated assistant scripts directory
- Configuration loading updated to use JSON files
- Skills guide and transparency skill updated for current organization
- Path references and cross-references updated for current folder structure

### Retired

- v1 migration preparation folders and intermediate files
- Local Python cache directories
- Obsolete version-control entries for v1 migration temp folders

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

## [v1.0.0]

### Added

- Original website content backup with complete migration workflow
- Establish archive repository with complete backup of original website content
- Create preparation folder structure for staged history
- Implement date mapping system to preserve original publication dates
- Developer tools for migration, verification, and version control
- AI transparency logging and task tracking practices
- Define archive purpose, audience, and preservation boundaries
- Organize repository with separate sections for columns and family trees
- Privacy safeguards including email obfuscation
- Backdate version control timestamps matching original publication dates
- Link verification
- Privacy checks to prevent personal data exposure
- Documentation reorganized into topic folders
- Admin guide for archive access management
- User guides for requesting and submitting archive updates
- Multi-user access documentation with permission levels
- Updated archive to modern HTML5 standards while preserving original content
- Family tree folder structure with per-tree folders
- Progressive index pages for all preparation commits
- Date-aware backup and commit preparation verification
- AI transparency logging with structured audit trail
- Encoding restoration with ISO-8859-1 charset declarations
- Timestamp accuracy fix for Windows filesystem
- Present tense standardization across all non-archive documentation
- Changelog folder structure with unreleased entries

### Changed

- Restructure file paths for content organization
- Encoding recovery for special characters
- Assets deduplicated across versions
- Original HTML preserved with path restructuring
- Navigation links standardized across all archive pages
- Project checks verify documentation and privacy
- Date validation flexible for different filesystem behaviors
- Documentation filenames follow consistent pattern
- Documentation refers to "the Archive" instead of domain names

### Fixed

- Date parsing for publication filenames
- Timestamp handling for archive-extracted files
- Duplicate skill registry entries
- Encoding corruption: preserve apostrophes and special characters

### Improved

- Columns page navigation correctly links to related content
- Main index pages properly organize blog posts and static pages
- Link validation understands folder-style URLs
- Archive preparation process more reliable and maintainable
