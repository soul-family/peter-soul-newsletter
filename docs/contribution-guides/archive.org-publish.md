# Archive.org Publish

## Overview

This guide covers how to publish and discover the archive on Archive.org (Internet Archive). The goal is to ensure the original content is preserved, accessible, and findable through the Wayback Machine and Archive.org search.

## Prerequisites

- Archive.org account (free registration at archive.org)
- Built static site ready for upload
- Metadata prepared (title, description, collection, creator, date)

## Step 1: Prepare Upload Package

Before uploading, ensure the static site is complete:

- All HTML, CSS, images, and assets are in the output folder
- Links are relative and work offline
- `index.html` exists at the root
- No sensitive personal data (emails, phone numbers) is exposed

## Step 2: Create Archive.org Item

1. Log in to archive.org
2. Go to [Upload Page](https://archive.org/upload/)
3. Drag and drop the prepared site folder or upload as a ZIP archive
4. Wait for the upload to complete

## Step 3: Set Item Metadata

After upload, edit the item metadata:

| Field | Value |
| --- | --- |
| Title | Peter Soul newsletter |
| Creator | Peter Soul |
| Date | 2002-2019 |
| Description | Blog columns and personal website archive, published between July 2002 and March 2019. |
| Collection | web |
| Subject | blogs; driving; UK; personal |
| License | Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International |

## Step 4: Enable Web Archive Format

To ensure proper Wayback Machine archiving:

1. Go to **Item Settings** > **Web Archive**
2. Enable **Capture Outlinks**
3. Enable **Capture CSS and Images**
4. Set **Crawl Depth** to 3 or higher
5. Save settings

## Step 5: Trigger Wayback Machine Capture

1. From the item page, click **Trigger Capture**
2. Select **Full Web Archive**
3. Wait for the crawl to complete (may take minutes to hours)
4. Verify the snapshot appears in the Wayback Machine

## Step 6: Verify the Archive

After capture completes:

1. Visit `https://web.archive.org/web/*/https://<your-domain>` to see available snapshots
2. Check that navigation links work
3. Verify images load correctly
4. Test that the page links resolve

## Step 7: Share the Archive

Once verified, share the Archive.org links:

- **Item Page**: `https://archive.org/details/[item-identifier]`
- **Wayback Machine**: `https://web.archive.org/web/*/https://<your-domain>`
- **Direct Download**: Available from the item page for offline access

## Troubleshooting

| Issue | Solution |
| --- | --- |
| Links broken after upload | Ensure all href attributes use relative paths |
| Images missing | Check that asset paths are correct and files were uploaded |
| Crawl incomplete | Increase crawl depth or wait for automatic recrawl |
| Personal data exposed | Remove emails/phones from source and re-upload |
