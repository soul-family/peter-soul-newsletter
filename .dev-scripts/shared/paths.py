import os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
PREPS = BASE / 'src-preps'
DATE_MAP = BASE / '.dev-scripts' / 'date_map.csv'
SRC_CONTENT = BASE / 'src-prep-last'
