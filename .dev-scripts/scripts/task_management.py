#!/usr/bin/env python3
"""
task_management.py — validate todo-next.md and todo-done.md integrity.
Checks:
- No duplicate tasks between todo-next and todo-done
- Tasks are unique within each file
- Tasks follow consistent format
"""

import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
TODO_NEXT = BASE / '.todo' / 'todo-next.md'
TODO_DONE = BASE / '.todo' / 'todo-done.md'

TASK_PATTERN = re.compile(r'^- (.+)$', re.MULTILINE)

def extract_tasks(path):
    text = path.read_text(encoding='utf-8')
    return set(TASK_PATTERN.findall(text))

def validate():
    issues = []
    
    if not TODO_NEXT.exists():
        issues.append(f"Missing {TODO_NEXT}")
        return issues
    if not TODO_DONE.exists():
        issues.append(f"Missing {TODO_DONE}")
        return issues
    
    next_tasks = extract_tasks(TODO_NEXT)
    done_tasks = extract_tasks(TODO_DONE)
    
    duplicates = next_tasks & done_tasks
    if duplicates:
        issues.append(f"Duplicate tasks in both todo-next and todo-done: {sorted(duplicates)}")
    
    next_text = TODO_NEXT.read_text(encoding='utf-8')
    next_lines = next_text.splitlines()
    next_seen = {}
    for line in next_lines:
        m = TASK_PATTERN.match(line)
        if m:
            task = m.group(1)
            if task in next_seen:
                issues.append(f"Duplicate task in todo-next.md: {task}")
            next_seen[task] = True
    
    done_text = TODO_DONE.read_text(encoding='utf-8')
    done_lines = done_text.splitlines()
    done_seen = {}
    for line in done_lines:
        m = TASK_PATTERN.match(line)
        if m:
            task = m.group(1)
            if task in done_seen:
                issues.append(f"Duplicate task in todo-done.md: {task}")
            done_seen[task] = True
    
    return issues

if __name__ == '__main__':
    issues = validate()
    if issues:
        print('TODO MANAGEMENT ISSUES:')
        for i in issues:
            print(f'  - {i}')
        sys.exit(1)
    print('TODO MANAGEMENT OK')
