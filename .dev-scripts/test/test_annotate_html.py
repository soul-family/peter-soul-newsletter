import unittest
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.annotate_html import annotate

class TestAnnotateHtml(unittest.TestCase):
    def test_annotate_adds_tag(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'test.html'
            p.write_text('<html><body>content</body></html>', encoding='utf-8')
            annotate(p, '2026-07-24')
            text = p.read_text(encoding='utf-8')
            self.assertIn('<!-- Latest Updated on: 2026-07-24 -->', text)
            self.assertIn('</html>', text)

    def test_annotate_replaces_existing(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'test.html'
            p.write_text('<html><body>content\n<!-- Latest Updated on: 2025-01-01 -->\n</body></html>', encoding='utf-8')
            annotate(p, '2026-07-24')
            text = p.read_text(encoding='utf-8')
            self.assertIn('<!-- Latest Updated on: 2026-07-24 -->', text)
            self.assertNotIn('2025-01-01', text)

    def test_annotate_no_html_tag(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'test.html'
            p.write_text('just content', encoding='utf-8')
            annotate(p, '2026-07-24')
            text = p.read_text(encoding='utf-8')
            self.assertIn('<!-- Latest Updated on: 2026-07-24 -->', text)

if __name__ == '__main__':
    unittest.main()
