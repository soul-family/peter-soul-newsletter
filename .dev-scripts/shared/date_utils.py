import re
from datetime import datetime

BLOG_RE = re.compile(r'^(january|february|march|april|may|june|july|august|september|october|november|december)[_\-]?(\d{4})\.html$', re.IGNORECASE)
MONTHS = {m: i for i, m in enumerate(['january','february','march','april','may','june','july','august','september','october','november','december'], 1)}

def parse_dt(s):
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None

def blog_date(name):
    m = BLOG_RE.match(name)
    if not m:
        return None
    return datetime(int(m.group(2)), MONTHS[m.group(1).lower()], 1, 13, 0, 0)

def format_date_for_csv(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S') if dt else ''

def format_date_for_tag(dt):
    return dt.strftime('%Y-%m-%d') if dt else ''
