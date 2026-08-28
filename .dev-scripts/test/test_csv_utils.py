import unittest
import sys
import tempfile
import csv
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.csv_utils import load_date_map, write_date_map
from shared.date_utils import parse_dt

class TestCsvUtils(unittest.TestCase):
    def test_write_and_load_date_map(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'dates.csv'
            rows = [
                {'file': 'content/test.html', 'category': 'blog', 'candidate_date': parse_dt('2026-07-24 17:48:14'), 'source': 'filename', 'mtime': parse_dt('2026-07-24 17:48:14')},
            ]
            write_date_map(p, rows)
            dm = load_date_map(p)
            self.assertIn('content/test.html', dm)
            self.assertEqual(dm['content/test.html'].year, 2026)
            self.assertEqual(dm['content/test.html'].month, 7)
            self.assertEqual(dm['content/test.html'].day, 24)

    def test_load_date_map_backslash_normalization(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'dates.csv'
            with open(p, 'w', newline='', encoding='utf-8') as f:
                w = csv.DictWriter(f, fieldnames=['file','category','candidate_date','source','mtime'])
                w.writeheader()
                w.writerow({'file': 'content\\test.html', 'category': 'individual', 'candidate_date': '2026-07-24 17:48:14', 'source': 'batch-upload', 'mtime': '2026-07-24 17:48:14'})
            dm = load_date_map(p)
            self.assertIn('content/test.html', dm)

if __name__ == '__main__':
    unittest.main()
