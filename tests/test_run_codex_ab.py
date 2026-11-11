import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "benchmarks" / "reproduction"))

from run_codex_ab import paired_deltas, skills_opened


class SkillsOpenedTests(unittest.TestCase):
    def opened(self, events):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "events.jsonl"
            log.write_text("\n".join(json.dumps(e) for e in events) + "\nnot json\n", encoding="utf-8")
            return skills_opened(log)

    def test_counts_explicit_reads(self):
        events = [
            {"item": {"type": "command_execution", "command": "bash -lc 'cat .agents/skills/tdd/SKILL.md'"}},
            {"item": {"command": ["sed", "-n", "1,40p", ".agents/skills/why/SKILL.md"]}},
        ]
        self.assertEqual(self.opened(events), ["tdd", "why"])

    def test_ignores_listings_and_output(self):
        events = [
            {"item": {"command": "ls .agents/skills", "aggregated_output": ".agents/skills/tdd/SKILL.md"}},
            {"item": {"command": "rg --files .agents/skills"}},
            {"item": {"command": "cat .agents/skills/*/SKILL.md"}},
            {"msg": "see .agents/skills/why/SKILL.md"},
        ]
        self.assertEqual(self.opened(events), [])


class PairedDeltaTests(unittest.TestCase):
    def row(self, variant, run, passed, status="finished"):
        return {"variant": variant, "run": run, "status": status, "grade": {"passed": passed}}

    def test_only_finished_pairs(self):
        rows = [
            self.row("baseline", 1, 5), self.row("skills", 1, 8),
            self.row("baseline", 2, 6), self.row("skills", 2, 0, "timeout"),
        ]
        self.assertEqual(paired_deltas(rows, 2), [3])


if __name__ == "__main__":
    unittest.main()
