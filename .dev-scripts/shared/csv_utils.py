import csv
from .date_utils import parse_dt, format_date_for_csv

def load_date_map(path):
    dm = {}
    with open(path, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            key = r['file'].replace('\\', '/')
            dm[key] = parse_dt(r['candidate_date'])
    return dm

def write_date_map(path, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['file', 'category', 'candidate_date', 'source', 'mtime'])
        w.writeheader()
        for r in rows:
            w.writerow({k: (format_date_for_csv(v) if hasattr(v, 'strftime') and k in ('candidate_date', 'mtime') else v) for k, v in r.items()})
