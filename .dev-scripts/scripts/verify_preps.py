#!/usr/bin/env python3
"""
verify_preps.py — validate src-preps/ structure, duplicates, and date constraints.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.paths import PREPS

def dates(p):
    s = os.stat(p)
    return datetime.fromtimestamp(s.st_ctime), datetime.fromtimestamp(s.st_mtime), datetime.fromtimestamp(s.st_atime)

def verify(preps=None):
    if preps is None:
        preps = PREPS
    pp = Path(preps)
    if not pp.exists():
        print('FAIL: directory not found')
        sys.exit(1)
    commits = sorted(d.name for d in pp.iterdir() if d.is_dir() and d.name.startswith('commit'))
    warns = []
    issues = []
    seen = {}
    for c in commits:
        cd = pp/c
        files = [f for f in cd.rglob('*') if f.is_file()]
        if c == 'commit0':
            names = [f.name.lower() for f in files]
            if 'readme.md' not in names:
                issues.append(f'{c}: missing README.md')
            if not any(f.name.lower().startswith('license') for f in files):
                issues.append(f'{c}: missing LICENSE')
        for f in files:
            ct, mt, _ = dates(f)
            if ct > mt:
                warns.append(f'{c}/{f.relative_to(cd)}: created > modified')
            rel = str(f.relative_to(pp)).replace('\\','/')
            if rel in seen:
                issues.append(f'duplicate: {rel}')
            seen[rel] = True
    if warns:
        print('WARNINGS:')
        for w in warns:
            print(f'  - {w}')
    if issues:
        print('FAILED')
        for i in issues:
            print(f'  - {i}')
        sys.exit(1)
    print('VERIFIED')

if __name__ == '__main__':
    verify(sys.argv[1] if len(sys.argv) > 1 else None)
