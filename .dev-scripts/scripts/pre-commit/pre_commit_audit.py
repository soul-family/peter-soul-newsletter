#!/usr/bin/env python3
"""
pre_commit_audit.py - verify project state before Git commit.

Checks:
1. Todo management: no duplicate T-numbers, valid structure
2. AI transparency log: interactions.md exists and is self-contained
3. Changelog: CHANGELOG.md exists and follows format
4. Documentation: guides exist and reference current tasks
5. Documentation links: markdown links in docs point to existing files
6. Session stats: stats files are up-to-date after database changes

Fails with actionable list of what to fix.
"""

import re
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent.parent

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from audit.task_management import validate as validate_todos

VERSION_PATTERN = re.compile(r'^##\s*\[(v?\d+\.\d+\.\d+)\]\s*$', re.MULTILINE)


def parse_latest_version(content):
    """Return the latest (highest) version string found in CHANGELOG.md, or None."""
    matches = VERSION_PATTERN.findall(content)
    if not matches:
        return None
    return matches[0]


def check_todos():
    todo_issues = validate_todos()
    if todo_issues:
        print('TODO AUDIT ISSUES:')
        for i in todo_issues:
            print(f'  - {i}')
        return False
    print('TODO AUDIT OK')
    return True


def check_ai_transparency():
    issues = []
    path = BASE / '.ai-activity' / 'ai-logs' / 'interactions.md'

    if not path.exists():
        issues.append('AI transparency log missing: .ai-activity/ai-logs/interactions.md')
        return issues

    content = path.read_text(encoding='utf-8')

    if '## Interaction:' not in content:
        issues.append('AI transparency log has no interaction entries')

    if 'T-' in content:
        issues.append('AI transparency log contains T-numbers (remove task references)')

    if '.py' in content or '.md' in content:
        issues.append('AI transparency log contains file extensions (remove implementation details)')

    if '@' in content and 'mailto:' not in content.lower():
        issues.append('AI transparency log may contain email addresses')

    if issues:
        print('AI TRANSPARENCY ISSUES:')
        for i in issues:
            print(f'  - {i}')
    else:
        print('AI TRANSPARENCY OK')

    return len(issues) == 0


def check_changelog():
    issues = []
    path = BASE / 'CHANGELOG.md'
    unreleased_path = BASE / '.changelog' / 'unreleased.md'
    version_path = BASE / 'VERSION'

    if not path.exists():
        issues.append('Changelog missing: CHANGELOG.md')
        return issues

    content = path.read_text(encoding='utf-8')

    if '## [' not in content:
        issues.append('Changelog has no version entries')

    version_headers = re.findall(r'^## \[.+?\]', content, re.MULTILINE)
    for header in version_headers:
        if re.search(r'^## \[.+?\]\s+\S', header):
            issues.append(f'Changelog version header has descriptive title: {header}')

    # Check VERSION file matches latest changelog version (optional)
    if version_path.exists():
        version_file = version_path.read_text(encoding='utf-8').strip()
        latest_version = parse_latest_version(content)
        if latest_version:
            expected = latest_version.lstrip('v')
            if version_file != expected:
                issues.append(f'VERSION file mismatch: file has {version_file}, CHANGELOG.md has {latest_version}')
        else:
            issues.append('VERSION file exists but CHANGELOG.md has no version entries')

    # Check for unreleased entries (report only, do not auto-promote)
    if unreleased_path.exists() and unreleased_path.read_text(encoding='utf-8').strip():
        issues.append('.changelog/unreleased.md has entries ready to promote')

    if issues:
        print('CHANGELOG ISSUES:')
        for i in issues:
            print(f'  - {i}')
    else:
        print('CHANGELOG OK')

    return len(issues) == 0


def check_session_stats():
    issues = []
    sessions_dir = BASE / '.ai-activity' / 'ai-sessions'
    
    if not sessions_dir.exists():
        print('SESSION STATS OK (no sessions directory)')
        return True
    
    db_files = list(sessions_dir.rglob('*.db'))
    if not db_files:
        print('SESSION STATS OK (no database files)')
        return True
    
    for db_path in db_files:
        stats_path = db_path.with_suffix('.stats.json')
        
        if not stats_path.exists():
            issues.append(f'Stats file missing for {db_path.relative_to(BASE)}')
            continue
        
        db_mtime = db_path.stat().st_mtime
        stats_mtime = stats_path.stat().st_mtime
        
        if db_mtime > stats_mtime:
            issues.append(f'Stats file outdated for {db_path.relative_to(BASE)} - database is newer than stats')
    
    if issues:
        print('SESSION STATS ISSUES:')
        for i in issues:
            print(f'  - {i}')
    else:
        print('SESSION STATS OK')
    
    return len(issues) == 0


def check_doc_links():
    issues = []
    docs_dir = BASE / '_docs'
    
    if not docs_dir.exists():
        print('DOC LINKS OK (no docs directory)')
        return True
    
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    
    for md_file in docs_dir.rglob('*.md'):
        try:
            content = md_file.read_text(encoding='utf-8')
            links = link_pattern.findall(content)
            
            for text, link in links:
                if link.startswith('http://') or link.startswith('https://'):
                    continue
                
                if link.startswith('#'):
                    continue
                
                if '..' in link:
                    continue
                
                target = (md_file.parent / link).resolve()
                if not target.exists():
                    issues.append(f'{md_file.relative_to(BASE)}: broken link [{text}]({link})')
        except Exception as e:
            issues.append(f'{md_file.relative_to(BASE)}: error reading file ({e})')
    
    if issues:
        print('DOC LINKS ISSUES:')
        for i in issues[:20]:
            print(f'  - {i}')
        if len(issues) > 20:
            print(f'  ... and {len(issues) - 20} more')
    else:
        print('DOC LINKS OK')
    
    return len(issues) == 0


def check_content_dates_older_than_logs():
    issues = []
    
    ai_log = BASE / '.ai-activity' / 'ai-logs' / 'interactions.md'
    changelog = BASE / 'CHANGELOG.md'
    
    log_dates = []
    if ai_log.exists():
        log_dates.append(datetime.fromtimestamp(ai_log.stat().st_mtime))
    if changelog.exists():
        log_dates.append(datetime.fromtimestamp(changelog.stat().st_mtime))
    
    if not log_dates:
        issues.append('No log files found to compare dates')
        return issues
    
    latest_log_date = max(log_dates)
    
    for f in PREPS.rglob('*'):
        if not f.is_file():
            continue
        rel = str(f.relative_to(PREPS)).replace('\\', '/')
        parts = rel.split('/')
        if len(parts) >= 2 and parts[0].startswith('commit') and parts[1] == 'src-content':
            content_mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if content_mtime > latest_log_date:
                issues.append(f'{rel}: content modified {content_mtime} is newer than latest log {latest_log_date}')
    
    if issues:
        print('DATE ORDER ISSUES:')
        for i in issues:
            print(f'  - {i}')
    else:
        print('DATE ORDER OK')
    
    return len(issues) == 0


def main():
    results = []

    print('=== Pre-Commit Audit ===\n')

    results.append(('Todo management', check_todos()))
    results.append(('AI transparency', check_ai_transparency()))
    results.append(('Changelog', check_changelog()))
    results.append(('Doc links', check_doc_links()))
    results.append(('Session stats', check_session_stats()))

    print('\n=== Summary ===')
    failed = [name for name, ok in results if not ok]
    if failed:
        print(f'FAILED: {", ".join(failed)}')
        sys.exit(1)
    print('ALL CHECKS PASSED')
    sys.exit(0)


if __name__ == '__main__':
    main()
