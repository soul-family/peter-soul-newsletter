#!/usr/bin/env python3
"""
pre_commit_audit.py — verify project state before Git commit.

Checks:
1. File dates in src-preps match date_map.csv
2. Todo management: no duplicate T-numbers, valid structure
3. AI transparency log: INTERACTIONS.md exists and is self-contained
4. Changelog: CHANGELOG.md exists and follows format
5. Documentation: guides exist and reference current tasks
6. Content dates: source content dates are older than or equal to log/guide dates

Fails with actionable list of what to fix.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.paths import BASE, PREPS, DATE_MAP
from shared.date_utils import parse_dt
from shared.csv_utils import load_date_map
from shared.encoding_utils import check_encoding_mismatch, check_charsets, verify_encoding
from shared.html_utils import check_href_issues
from scripts.task_management import validate as validate_todos

def check_file_dates():
    dm = load_date_map(DATE_MAP)
    issues = []
    warnings = []
    
    for f in PREPS.rglob('*'):
        if not f.is_file():
            continue
        rel = str(f.relative_to(PREPS)).replace('\\', '/')
        key = rel
        parts = rel.split('/')
        if len(parts) >= 2 and parts[0].startswith('commit') and parts[1] == 'src-content':
            key = '/'.join(parts[2:])
        if key not in dm:
            continue
        
        expected = dm[key]
        if expected is None:
            continue
        
        stat = f.stat()
        mt = datetime.fromtimestamp(stat.st_mtime).replace(microsecond=0)
        ct = datetime.fromtimestamp(stat.st_ctime).replace(microsecond=0)
        at = datetime.fromtimestamp(stat.st_atime).replace(microsecond=0)
        
        if mt != expected:
            issues.append(f'{rel}: modified time mismatch, expected {expected}, got {mt}')
        if ct != expected:
            warnings.append(f'{rel}: created time mismatch, expected {expected}, got {ct}')
        if at != expected:
            warnings.append(f'{rel}: accessed time mismatch, expected {expected}, got {at}')
    
    if issues:
        print('DATE AUDIT ISSUES:')
        for i in issues:
            print(f'  {i}')
        if warnings:
            print('DATE AUDIT WARNINGS:')
            for w in warnings:
                print(f'  {w}')
        return False
    if warnings:
        print('DATE AUDIT WARNINGS (non-fatal):')
        for w in warnings:
            print(f'  {w}')
    print('DATE AUDIT OK')
    return True

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
    path = BASE / '.ai-activity' / 'INTERACTIONS.md'
    
    if not path.exists():
        issues.append('AI transparency log missing: .ai-activity/INTERACTIONS.md')
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
    
    if not path.exists():
        issues.append('Changelog missing: CHANGELOG.md')
        return issues
    
    content = path.read_text(encoding='utf-8')
    
    if '## [' not in content:
        issues.append('Changelog has no version entries')
    
    import re
    version_headers = re.findall(r'^## \[.+?\]', content, re.MULTILINE)
    for header in version_headers:
        if re.search(r'^## \[.+?\]\s+\S', header):
            issues.append(f'Changelog version header has descriptive title: {header}')
    
    if issues:
        print('CHANGELOG ISSUES:')
        for i in issues:
            print(f'  - {i}')
    else:
        print('CHANGELOG OK')
    
    return len(issues) == 0

def check_guides():
    issues = []
    guides = [
        BASE / '.docs' / 'reports' / 'update-guide-v1-to-v2.md',
        BASE / '.docs' / 'reports' / 'updates-guide-v0-to-v1.md',
        BASE / '.docs' / 'contribution-guides' / 'ai-transparency.md',
        BASE / '.docs' / 'contribution-guides' / 'changelog-management.md',
        BASE / '.docs' / 'contribution-guides' / 'task-management.md',
        BASE / '.docs' / 'contribution-guides' / 'archive.org-publish.md',
        BASE / '.docs' / 'contribution-guides' / 'storage-manage.md',
        BASE / '.docs' / 'archive-guides' / 'about-archive.md',
        BASE / '.docs' / 'archive-guides' / 'browsing-newsletter.md',
        BASE / '.docs' / 'contribution-guides' / 'archive.org-searching.md',
        BASE / '.docs' / 'contribution-guides' / 'storage-manage-invite.md',
        BASE / '.docs' / 'contribution-guides' / 'submit-new-info.md',
        BASE / '.docs' / 'family-tree' / 'archive-guide.md',
    ]
    
    for g in guides:
        if not g.exists():
            issues.append(f'Guide missing: {g.relative_to(BASE)}')
    
    if issues:
        print('GUIDES ISSUES:')
        for i in issues:
            print(f'  - {i}')
    else:
        print('GUIDES OK')
    
    return len(issues) == 0

def check_content_dates_older_than_logs():
    issues = []
    
    ai_log = BASE / '.ai-activity' / 'INTERACTIONS.md'
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

def check_encoding():
    issues = []
    
    mismatch = check_encoding_mismatch(PREPS)
    if mismatch:
        issues.append(f'Encoding mismatch: {len(mismatch)} files declare ISO-8859-1 but contain UTF-8 multibyte sequences')
        for p in mismatch[:5]:
            issues.append(f'  - {p}')
        if len(mismatch) > 5:
            issues.append(f'  ... and {len(mismatch) - 5} more')
    
    charsets = check_charsets(PREPS)
    if 'UTF-8' in charsets:
        issues.append(f'UTF-8 charset declarations found: {charsets["UTF-8"]} files (expected ISO-8859-1 or windows-1252)')
    
    verify = verify_encoding(PREPS)
    if verify['invalid_encoding']:
        issues.append(f'Invalid Windows-1252 bytes: {len(verify["invalid_encoding"])} files')
        for p in verify['invalid_encoding'][:5]:
            issues.append(f'  - {p}')
    
    if issues:
        print('ENCODING ISSUES:')
        for i in issues:
            print(f'  - {i}')
    else:
        print('ENCODING OK')
    
    return len(issues) == 0

def check_hrefs():
    issues = []
    
    href_issues = check_href_issues(PREPS)
    if href_issues:
        issues.append(f'Broken href patterns: {len(href_issues)} occurrences')
        for p, line in href_issues[:5]:
            issues.append(f'  - {p}: {line}')
        if len(href_issues) > 5:
            issues.append(f'  ... and {len(href_issues) - 5} more')
    
    if issues:
        print('HREF ISSUES:')
        for i in issues:
            print(f'  - {i}')
    else:
        print('HREFS OK')
    
    return len(issues) == 0

def main():
    results = []
    
    print('=== Pre-Commit Audit ===\n')
    
    results.append(('File dates', check_file_dates()))
    results.append(('Todo management', check_todos()))
    results.append(('AI transparency', check_ai_transparency()))
    results.append(('Changelog', check_changelog()))
    results.append(('Guides', check_guides()))
    results.append(('Encoding', check_encoding()))
    results.append(('Hrefs', check_hrefs()))
    results.append(('Date order', check_content_dates_older_than_logs()))
    
    print('\n=== Summary ===')
    failed = [name for name, ok in results if not ok]
    if failed:
        print(f'FAILED: {", ".join(failed)}')
        sys.exit(1)
    print('ALL CHECKS PASSED')
    sys.exit(0)

if __name__ == '__main__':
    main()
