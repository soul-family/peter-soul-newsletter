import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.date_utils import parse_dt, blog_date, format_date_for_csv, format_date_for_tag

class TestDateUtils(unittest.TestCase):
    def test_parse_dt_with_time(self):
        dt = parse_dt('2026-07-24 17:48:14')
        self.assertEqual(dt.year, 2026)
        self.assertEqual(dt.month, 7)
        self.assertEqual(dt.day, 24)

    def test_parse_dt_date_only(self):
        dt = parse_dt('2026-07-24')
        self.assertEqual(dt.year, 2026)
        self.assertEqual(dt.month, 7)
        self.assertEqual(dt.day, 24)

    def test_parse_dt_invalid(self):
        self.assertIsNone(parse_dt('not-a-date'))

    def test_blog_date_underscore(self):
        dt = blog_date('july_2002.html')
        self.assertEqual(dt.year, 2002)
        self.assertEqual(dt.month, 7)
        self.assertEqual(dt.day, 1)
        self.assertEqual(dt.hour, 13)

    def test_blog_date_no_separator(self):
        dt = blog_date('july2002.html')
        self.assertEqual(dt.year, 2002)
        self.assertEqual(dt.month, 7)

    def test_blog_date_not_blog(self):
        self.assertIsNone(blog_date('familytree.html'))

    def test_format_date_for_csv(self):
        from datetime import datetime
        dt = datetime(2026, 7, 24, 17, 48, 14)
        self.assertEqual(format_date_for_csv(dt), '2026-07-24 17:48:14')

    def test_format_date_for_tag(self):
        from datetime import datetime
        dt = datetime(2026, 7, 24, 17, 48, 14)
        self.assertEqual(format_date_for_tag(dt), '2026-07-24')

if __name__ == '__main__':
    unittest.main()
