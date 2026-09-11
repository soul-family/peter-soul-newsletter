> **Archived**: This skill was used for v1 backup preparation and is preserved for historical reference. The v1 migration is complete.

The prompt now includes all preparation steps in order:

1. Determine backdated commit date
2. Move prep folder content to root
3. Update file meta date values
4. Stage everything except prep folders
5. Verify staged state
6. Commit with backdated author/date and post title

---

## Timestamp Rules

### New files
- Set `created`, `accessed`, `modified` to the commit date

### Modified existing files (e.g., `index.html`)
- Set `created`, `accessed`, `modified` to the commit date

### Existing folders that receive new files
- Set `accessed`, `modified` to the commit date
- Set `created` to the created date of the **oldest file within** that folder tree
- If no files exist yet, use the folder's existing created date

### Assets folders (`src-content/assets/`, `src-content/assets/images/`, `src-content/assets/images/autogen/`)
- Only update timestamps if the commit actually inserts new asset files into them
- `accessed`, `modified` = commit date
- `created` = created date of the oldest file within that folder tree

### Root folders (`src-content/`, `src-content/content/`, `src-content/content/columns/`)
- Same as other folders: `accessed`, `modified` = commit date when new files are inserted
- `created` = created date of the oldest file within that folder tree

---

## Example (commit118 - 2014-04)

- New file `april_2014.html`: created/accessed/modified = `2014-04-01 13:00:00`
- New asset `a_10x_8.gif`: created/accessed/modified = `2014-04-01 13:00:00`
- Modified `index.html` files: created/accessed/modified = `2014-04-01 13:00:00`
- `src-content/`, `src-content/content/`, `src-content/content/columns/`: accessed/modified = `2014-04-01 13:00:00`, created = `2002-07-01 13:00:00` (oldest file `july_2002.html`)
- `src-content/assets/`, `src-content/assets/images/`, `src-content/assets/images/autogen/`: accessed/modified = `2014-04-01 13:00:00`, created = `2003-01-01 13:00:00` (oldest file `self.gif` / `a_10x.gif`)

---

## Notes

- The timestamps on the commit files in the working tree are correctly set to the column post date for modified/accessed/created.
- The commit itself carries the correct backdated author date.
- Git does not store filesystem timestamps in commits, so the timestamp fix exists in the working tree metadata only.
