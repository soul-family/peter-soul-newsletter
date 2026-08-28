# Report v1 — Original 2002–2019

## Overview

Version 1 represents the original published website as authored by Peter Soul between 2002 and 2019, committed to GitHub with backdated Git timestamps.


## Current State

- Newsletter posts organized under `content/columns/` by publish date
- Posts span from July 2002 to March 2019 (167 posts)
- Each post is a static HTML file with original content and assets
- Prep commits (`commit1` to `commit167`) contain progressive newsletter post additions
- All file and directory meta dates set to corresponding newsletter post creation dates
- Columns index pages (`index.html` and `columns/index.html`) progressively list posts available at each commit date
- Contact pages use updated obfuscated email
- Removed external dependencies (Google search forms)
- Index pages fixed for cp1252 encoding and proper future-post filtering


## Content

- Newsletter columns posts from July 2002 to March 2019
- Family tree pages for multiple families
- Personal notes, letters, and escapology content
- Info and links pages

## Structure

- `content/` — non-blog HTML pages
- `content/columns/` — newsletter columns posts, each with publish year-month
- `assets/` — images, GIFs, and static assets

## Original Features

- Static HTML pages with original design
- Newsletter archive navigation by month/year
- Family tree HTML pages with character-by-character ASCII layouts
- Image galleries and embedded images
- Original navigation links between pages

## Preservation Decisions

- External dependencies remove: Google search form remove from all pages
- Remove author email address as no longer active
- Add an active contact email address
- Author text and navigation preserve exactly as published
- HTML files annotate with latest update dates

## Technical Baseline

- Plain HTML/CSS, no build step
- Encoding: Windows-1252 byte encoding restored with ISO-8859-1 charset declarations
- Character preservation: apostrophes, hyphens, and special characters maintained exactly as authored
- Blog columns created using [NetObjects Fusion 7 for Windows](https://en.wikipedia.org/wiki/NetObjects_Fusion), a WYSIWYG web editor that generated the original table-based layouts and navigation structure
- Family trees created using [GenoPro](https://en.wikipedia.org/wiki/GenoPro), a genealogy software application that produced the family tree diagrams and data embedded in the HTML pages