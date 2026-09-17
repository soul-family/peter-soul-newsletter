# Newsletter Archive - v1 (2002–2019)

## About This Report

This report documents the original Peter Soul newsletter archive, authored between July 2002 and March 2019.

## Archive Purpose and Boundaries

The archive preserves the original website published by the author between 2002 and 2019; "A Physicist Writes..." as published in the Thames Valley Group of Advanced Motorists newsletter. Committed to GitHub with backdated Git timestamps. Preservation boundaries validate and document: original author intent is respected, and the archive is maintained through the author's family.

## Content Summary

- 167 newsletter columns organized by publish date
- Motoring and physics articles written by Peter Soul
- Original HTML pages with their design and assets
- Navigation links between pages
- Image galleries and embedded images
- Original author notes and commentary
- Family tree pages with ASCII diagrams

## Preservation Approach

- **Consulting** - Defined archive purpose, audience, preservation boundaries, and GitHub organisation setup
- **Planning** - Established milestones, documented preservation decisions, captured AI planning decisions, and defined AI transparency requirements
- **Skills & Tools** - Created `.skills` folder, moved AI skill definitions out of archive pages, added verification skills for commit-prep folders and file metadata, and preserved all intermediate Python scripts
- **File & Folder Planning** - Researched static site generation, built local archive site, generated sitemap, added schema metadata, defined URL routing, and established Git workflow
- **v1 Migration** - Created progressive index pages with correct encoding and filtering, defined commit sequence for blog posts, and ensured each commit included blog post content, updated archive file, and newly referenced assets
- **Execution** - Updated archive to HTML5 doctype, created page-type templates, obfuscated contact information, rebuilt prep folders with updated structure, and created developer and user guidance
- **Family tree separation**: Family tree content was separated from newsletter columns to a dedicated repository.

- **Exact wording preserved** - All text, notes, and author commentary appear exactly as originally written
- **Original diagrams intact** - ASCII family tree charts retain their original layout and spacing
- **Sources maintained** - All references, bibliography entries, and external links are intact
- **Character fidelity** - Special characters, apostrophes, and formatting match the original (Windows-1252 encoding)

## Technology: Then and Now

| Aspect | Original Website (2002–2019) | This Archive (v1) |
| --- | --- | --- |
| **Editing tool** | NetObjects Fusion 7 (visual editor) | Any text editor |
| **Diagram tool** | GenoPro genealogy software | Preserved as-is (ASCII text) |
| **File format** | Proprietary project + static HTML | Plain HTML, UTF-8 encoding |
| **Character encoding** | Windows-1252 / ISO-8859-1 | UTF-8 throughout |
| **Version control** | None - files published as-is | Full Git history with backdated timestamps |
| **Hosting** | Traditional web hosting | GitHub Pages (free, reliable) |
| **Offline access** | Not supported | Works completely offline |
| **Navigation** | Original links only | Main index + column indexes |
| **Privacy** | Public contact info | Emails obfuscated, living members protected |
| **Dependencies** | External search, third-party scripts | Self-contained, no external calls |

## What Changed from the Original

- Reorganised into a clear folder structure (`content/` and `content/columns/`)
- `links.html` renamed to `content/columns/index.html`
- `index.html` moved from root to `content/index.html`
- All internal links updated to relative paths
- HTML files annotated with `<!-- Latest Updated on: YYYY-MM-DD -->`
- External dependencies excluded (Google search form)
- Original author email address obfuscated; active contact email added
- Each page marked with its last update date

## Known Limitations

- Filesystem dates were reset by archive extraction; Git history provides accurate chronology
- Original design targeted older screen sizes; modern responsive behavior is planned for v2

## Version Control

- Full Git history with backdated timestamps matching original publish dates
- Prep commits (`commit1` to `commit167`) contain progressive newsletter post additions
- All file and directory meta dates set to corresponding newsletter post creation dates
- Columns index pages progressively list posts available at each commit date
