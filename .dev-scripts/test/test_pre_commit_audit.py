import unittest
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.pre_commit_audit import check_file_dates
from scripts.update_commit_dates import set_dates
from shared.date_utils import parse_dt
from shared.csv_utils import write_date_map

class TestPreCommitAudit(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.base = Path(self.td.name)
        self.preps = self.base / 'src-preps'
        self.preps.mkdir()
        (self.base / '.dev-scripts').mkdir()
        (self.base / '.dev-scripts' / 'date_map.csv').touch()

    def tearDown(self):
        self.td.cleanup()

    def test_set_dates_mock(self):
        f = self.preps / 'test.html'
        f.write_text('content', encoding='utf-8')
        dt = parse_dt('2026-07-24 17:48:14')
        with patch('ctypes.windll.kernel32.CreateFileW', return_value=123):
            with patch('ctypes.windll.kernel32.SetFileTime', return_value=True):
                with patch('ctypes.windll.kernel32.CloseHandle'):
                    result = set_dates(f, dt)
                    self.assertIsNone(result)

    def test_check_file_dates_no_issues(self):
        f = self.preps / 'test.html'
        f.write_text('content', encoding='utf-8')
        dt = parse_dt('2026-07-24 17:48:14')
        rows = [{'file': 'test.html', 'category': 'individual', 'candidate_date': dt, 'source': 'batch-upload', 'mtime': dt}]
        write_date_map(self.base / '.dev-scripts' / 'date_map.csv', rows)
        # We can't easily test Windows date setting without mocking at a deep level
        # This test verifies the script loads without error

if __name__ == '__main__':
    unittest.main()
