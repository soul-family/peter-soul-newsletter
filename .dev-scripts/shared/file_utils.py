import os
from pathlib import Path

def read_enc(p):
    for enc in ('utf-8', 'cp1252', 'latin-1', 'iso-8859-1'):
        try:
            t = p.read_text(encoding=enc, errors='replace')
            if '\ufffd' not in t:
                return t
        except Exception:
            pass
    return p.read_text(encoding='utf-8', errors='replace')

def write_text(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')

def safe_relpath(path, base):
    return str(path.relative_to(base)).replace('\\', '/')
