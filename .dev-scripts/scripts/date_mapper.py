#!/usr/bin/env python3
"""
date_mapper.py — classify files and derive candidate commit dates.
Outputs .dev-scripts/date_map.csv by default.
"""

import os
import sys
import csv
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.date_utils import blog_date, parse_dt, format_date_for_csv
from shared.csv_utils import write_date_map

def batch_date(rows):
    mtimes = [r['mtime'] for r in rows if r['category'] == 'individual']
    if not mtimes:
        return None
    mtimes.sort()
    best = cur = 0
    best_n = cur_n = 1
    for i in range(1, len(mtimes)):
        if (mtimes[i] - mtimes[i-1]).total_seconds() <= 600:
            cur_n += 1
            if cur_n > best_n:
                best_n = cur_n
                best = cur
        else:
            cur = i
            cur_n = 1
    cluster = mtimes[best:best+best_n]
    return cluster[len(cluster)//2]

def map_dates(src_dir, out=None):
    from shared.paths import DATE_MAP
    if out is None:
        out = DATE_MAP
    
    src = Path(src_dir)
    rows = []
    for root, _, files in os.walk(src):
        for name in files:
            p = Path(root) / name
            rel = p.relative_to(src).as_posix()
            mt = parse_dt(format_date_for_csv(datetime.fromtimestamp(p.stat().st_mtime)))
            bd = blog_date(name)
            cat = 'blog' if bd else 'individual'
            cand = bd
            src_name = 'filename' if bd else 'batch-pending'
            if rel.startswith('html/'):
                rel = ('content/columns/' if bd else 'content/') + rel[5:]
            rows.append(dict(file=rel, category=cat, candidate_date=cand, source=src_name, mtime=mt))

    bd = batch_date(rows)
    for r in rows:
        if r['category'] == 'individual':
            r['candidate_date'] = bd or r['mtime']
            r['source'] = 'batch-upload' if bd else 'mtime-fallback'
            if r['mtime'] > r['candidate_date']:
                r['candidate_date'] = r['mtime']
                r['source'] += '+mtime-override'

    write_date_map(out, rows)
    print(f"Written {len(rows)} rows to {out}")

if __name__ == '__main__':
    from datetime import datetime
    map_dates(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
