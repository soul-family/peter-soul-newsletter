# Storage Manage

## Overview

This guide explains how to manage the archive on GitHub. It covers who can access the repository, how to invite people, and how to keep the archive safe and organized.

## What is GitHub Storage?

GitHub is where the archive lives online. Think of it like a shared folder that:
- Keeps all the files safe
- Tracks every change made
- Lets multiple people work together
- Stores the history of the archive

## Who Needs Access?

### Archive Owner
- Full control over everything
- Can add or remove people
- Makes final decisions

### Archive Maintainers
- Can update content and fix issues
- Helps keep the archive running
- Usually family members or trusted helpers

### Viewers
- Can read and download the archive
- Cannot make changes
- Useful for family members who want to browse

## How to Invite Someone

### Step 1: Get Their GitHub Username

Ask the person to:
1. Go to github.com
2. Create a free account if they don't have one
3. Send you their GitHub username

### Step 2: Invite Them

1. Go to the archive repository on GitHub
2. Click **Settings** (top right)
3. Click **Collaborators** or **Manage access**
4. Click **Invite a collaborator**
5. Type their GitHub username
6. Choose what they can do:
   - **Read** - they can only view (best for most people)
   - **Write** - they can make changes (for maintainers)
   - **Admin** - full control (for owners only)
7. Click **Send invitation**

They will receive an email with a link to accept.

## What Can Each Person Do?

| Role | What They Can Do | Best For |
|------|------------------|----------|
| **Read** | View files, download the archive | Family members, researchers |
| **Write** | Edit files, fix issues | Active maintainers |
| **Admin** | Everything | Repository owner |

## Keeping the archive Safe

### Protect the Main Branch

The `main` branch is the master copy. To protect it:

1. Go to **Settings** > **Branches**
2. Click **Add rule**
3. Type `main` as the branch name
4. Turn on:
   - **Require pull request before merging** - changes must be reviewed
   - **Block history rewrites** - prevents accidental history changes
     - **Require review before content retirement** - protects against accidental retirement
5. Click **Create**

This means:
- Nobody can accidentally remove the archive
- All changes are reviewed before going live
- The history stays intact

### Use Pull Requests

When someone wants to make a change:

1. They create a **pull request**
2. You review the change
3. If it looks good, you approve it
4. The change is added to the archive

This keeps the archive safe and lets you review all changes.

## Managing Who Has Access

### Check Current Access

1. Go to **Settings** > **Manage access**
2. You will see a list of everyone with access
3. Each person shows their permission level

### Change Someone's Access

1. Find the person in the list
2. Click the pencil icon
3. Change their role
4. Click **Save**

### Remove Someone's Access

1. Find the person in the list
2. Click the trash icon
  3. Confirm access retirement

They will immediately lose access.

## Best Practices

### Start with Read-Only

When inviting new people:
- Start with **Read** access
- Promote to **Write** only if they actively contribute
- Keep **Admin** for yourself only

### Regular Check-Ups

Every few months:
- Review the list of people with access
- Remove people who no longer need it
- Update roles if responsibilities change

### Keep Backups

GitHub is safe, but also:
- Download the archive periodically
- Store a copy on your computer
- Keep backups in a separate location

## Common Tasks

### Invite a New Family Member

1. Ask for their GitHub username
2. Invite with **Read** access
3. They can now view the archive
4. Send them the link to the repository

### Add a New Maintainer

1. Make sure they have a GitHub account
2. Invite with **Write** access
3. Show them how to create pull requests
4. Review their first few changes personally

### Remove Access

1. Go to **Settings** > **Manage access**
2. Find the person
3. Click the trash icon
4. Confirm

## Getting Help

If you get stuck:
- Check GitHub's help documentation
- Ask another repository admin
- The archive owner can always reset permissions

## Summary

Managing GitHub storage is about:
- Inviting the right people with the right access
- Protecting the main branch from accidents
- Reviewing changes before they go live
- Keeping the archive safe and organized

The archive is a shared family resource. Good management ensures it stays safe and accessible for everyone.
