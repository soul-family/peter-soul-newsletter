import unittest
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.encoding_utils import (
    check_encoding_mismatch,
    check_charsets,
    restore_windows1252,
    restore_charset_declarations,
    verify_encoding,
)


class TestEncodingUtils(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.base = Path(self.td.name)
        self.preps = self.base / 'src-preps'
        self.preps.mkdir()

    def tearDown(self):
        self.td.cleanup()

    def test_check_encoding_mismatch_detects_utf8_in_iso(self):
        f = self.preps / 'test.html'
        content = '<meta charset="ISO-8859-1">hello \u2019 world'
        f.write_bytes(content.encode('utf-8'))
        issues = check_encoding_mismatch(self.preps)
        self.assertEqual(len(issues), 1)

    def test_check_encoding_mismatch_clean_file(self):
        f = self.preps / 'test.html'
        f.write_bytes(b'<meta charset="ISO-8859-1">hello')
        issues = check_encoding_mismatch(self.preps)
        self.assertEqual(len(issues), 0)

    def test_check_charsets_counts(self):
        (self.preps / 'utf8.html').write_bytes(b'<meta charset=UTF-8>')
        (self.preps / 'iso.html').write_bytes(b'<meta charset=ISO-8859-1>')
        charsets = check_charsets(self.preps)
        self.assertEqual(charsets.get('UTF-8'), 1)
        self.assertEqual(charsets.get('ISO-8859-1'), 1)

    def test_restore_windows1252_converts_utf8_to_cp1252(self):
        f = self.preps / 'test.html'
        content = '<meta charset="ISO-8859-1">hello \u2019 world'
        f.write_bytes(content.encode('utf-8'))
        fixed, errors = restore_windows1252(self.preps)
        self.assertEqual(fixed, 1)
        self.assertEqual(errors, 0)
        raw = f.read_bytes()
        self.assertIn(b'\x92', raw)
        self.assertNotIn(b'\xe2\x80\x99', raw)

    def test_restore_charset_declarations(self):
        f = self.preps / 'test.html'
        f.write_bytes(b'<meta charset=UTF-8>hello')
        count = restore_charset_declarations(self.preps, 'ISO-8859-1')
        self.assertEqual(count, 1)
        content = f.read_text(encoding='cp1252')
        self.assertIn('charset=ISO-8859-1', content)
        self.assertNotIn('charset=UTF-8', content)

    def test_verify_encoding_valid_cp1252(self):
        f = self.preps / 'test.html'
        f.write_bytes(b'<meta charset="ISO-8859-1">hello \x92 world')
        results = verify_encoding(self.preps)
        self.assertIn(str(f), results['valid_windows1252'])
        self.assertIn(str(f), results['smart_quotes_present'])
        self.assertEqual(len(results['invalid_encoding']), 0)
        self.assertEqual(len(results['charset_mismatch']), 0)


if __name__ == '__main__':
    unittest.main()
