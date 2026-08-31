#!/usr/bin/env python3
"""
pre_commit_audit.py — verify project state before Git commit.

Checks:
1. Todo management: no duplicate T-numbers, valid structure
2. AI transparency log: interactions.md exists and is self-contained
3. Changelog: CHANGELOG.md exists and follows format
4. Documentation: guides exist and reference current tasks

Fails with actionable list of what to fix.
"""

import re
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.task_management import validate as validate_todos


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

    # Promote unreleased entries on every pre-commit
    if unreleased_path.exists() and unreleased_path.read_text(encoding='utf-8').strip():
        result = subprocess.run(
            [sys.executable, str(BASE / '.dev-scripts' / 'scripts' / 'generate_changelog.py')],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            issues.append(f'Changelog generator failed: {result.stderr.strip()}')
        else:
            print('CHANGELOG promoted from unreleased.md')

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
        BASE / '_docs' / 'reports' / 'update-guide-v1-to-v2.md',
        BASE / '_docs' / 'reports' / 'updates-guide-v0-to-v1.md',
        BASE / '_docs' / 'contribution-guides' / 'ai-transparency.md',
        BASE / '_docs' / 'contribution-guides' / 'changelog-management.md',
        BASE / '_docs' / 'contribution-guides' / 'task-management.md',
        BASE / '_docs' / 'contribution-guides' / 'archive.org-publish.md',
        BASE / '_docs' / 'contribution-guides' / 'storage-manage.md',
        BASE / '_docs' / 'archive-guides' / 'about-archive.md',
        BASE / '_docs' / 'archive-guides' / 'browsing-newsletter.md',
        BASE / '_docs' / 'contribution-guides' / 'archive.org-searching.md',
        BASE / '_docs' / 'contribution-guides' / 'storage-manage-invite.md',
        BASE / '_docs' / 'contribution-guides' / 'submit-new-info.md',
        BASE / '_docs' / 'family-tree' / 'archive-guide.md',
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
    results.append(('Guides', check_guides()))

    print('\n=== Summary ===')
    failed = [name for name, ok in results if not ok]
    if failed:
        print(f'FAILED: {", ".join(failed)}')
        sys.exit(1)
    print('ALL CHECKS PASSED')
    sys.exit(0)


if __name__ == '__main__':
    main()
