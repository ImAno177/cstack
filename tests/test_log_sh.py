from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / 'skills' / 'show-me-your-work' / 'scripts' / 'log.sh'
HEADER = 'ts\tphase\tdecision\twhy\tevidence\tresult'


def run(logfile: Path, *cells: str) -> subprocess.CompletedProcess:
    return subprocess.run(['bash', str(SCRIPT), str(logfile), *cells], cwd=logfile.parent.parent, capture_output=True, text=True)


class LogShTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.log = Path(self._tmp.name) / 'nested' / 'decisions.tsv'

    def tearDown(self):
        self._tmp.cleanup()

    def rows(self) -> list[list[str]]:
        return [line.split('\t') for line in self.log.read_text(encoding='utf-8').splitlines()]

    def test_creates_directory_and_header_once(self):
        self.assertEqual(run(self.log, 'a', 'b', 'c', 'd', 'e').returncode, 0)
        self.assertEqual(run(self.log, 'a', 'b', 'c', 'd', 'e').returncode, 0)
        lines = self.log.read_text(encoding='utf-8').splitlines()
        self.assertEqual(lines[0], HEADER)
        self.assertEqual(len(lines), 3)
        self.assertTrue(all(len(row) == 6 for row in self.rows()))

    def test_flattens_tabs_and_newlines(self):
        run(self.log, 'phase', 'two\tcells', 'line\nbreak', 'ev', 'ok')
        row = self.rows()[1]
        self.assertEqual(len(row), 6)
        self.assertEqual(row[2], 'two cells')
        self.assertEqual(row[3], 'line break')

    def test_quotes_formula_prefixes_even_after_whitespace(self):
        run(self.log, '=A1', '+1', '-1', '@x', '\t=HYPERLINK("x")')
        row = self.rows()[1]
        self.assertEqual(row[1:5], ["'=A1", "'+1", "'-1", "'@x"])
        self.assertTrue(row[5].startswith("' "))

    def test_rejects_wrong_argument_count(self):
        result = run(self.log, 'only', 'three', 'cells')
        self.assertEqual(result.returncode, 1)
        self.assertIn('usage', result.stderr)


if __name__ == '__main__':
    unittest.main()
