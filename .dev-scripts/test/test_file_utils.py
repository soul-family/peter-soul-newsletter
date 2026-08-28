import unittest
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.file_utils import read_enc, write_text, safe_relpath

class TestFileUtils(unittest.TestCase):
    def test_write_and_read_utf8(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'test.txt'
            write_text(p, 'hello world')
            self.assertEqual(p.read_text(encoding='utf-8'), 'hello world')

    def test_read_enc_fallback(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'test.txt'
            p.write_bytes('café'.encode('cp1252'))
            text = read_enc(p)
            self.assertIn('café', text)

    def test_safe_relpath(self):
        base = Path('/tmp/base')
        target = Path('/tmp/base/sub/file.txt')
        self.assertEqual(safe_relpath(target, base), 'sub/file.txt')

    def test_safe_relpath_windows_style(self):
        base = Path('C:/base')
        target = Path('C:/base/sub\\file.txt')
        self.assertEqual(safe_relpath(target, base), 'sub/file.txt')

if __name__ == '__main__':
    unittest.main()
