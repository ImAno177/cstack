from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"


def run(script: str, root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), "--root", str(root), *args], capture_output=True, text=True
    )


def skill(root: Path, plugin: str, name: str, description: str = "Does one thing. Use when testing.", extra: str = "") -> Path:
    path = root / "plugins" / plugin / "skills" / name
    path.mkdir(parents=True, exist_ok=True)
    (path / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {description}\n{extra}---\n\n# {name}\n", encoding="utf-8")
    return path


class MarketplaceTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / ".cstack").mkdir()
        shutil.copy(REPO / "LICENSE", self.root / "LICENSE")
        catalog = json.loads((REPO / ".cstack" / "catalog.json").read_text(encoding="utf-8"))
        catalog["plugins"] = catalog["plugins"][:2]
        self.names = [p["name"] for p in catalog["plugins"]]
        (self.root / ".cstack" / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
        skill(self.root, self.names[0], "alpha")
        skill(self.root, self.names[1], "beta")

    def tearDown(self):
        self._tmp.cleanup()

    def build(self):
        result = run("build_manifests.py", self.root)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_generated_marketplace_validates_and_lists_each_plugin(self):
        self.build()
        result = run("validate_plugin.py", self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        claude = json.loads((self.root / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual([p["source"] for p in claude["plugins"]], [f"./plugins/{n}" for n in self.names])
        for host in (".claude-plugin", ".codex-plugin", ".grok-plugin", ".cursor-plugin"):
            self.assertTrue((self.root / "plugins" / self.names[0] / host / "plugin.json").is_file(), host)
        self.assertEqual(run("build_manifests.py", self.root, "--check").returncode, 0)

    def test_check_reports_stale_manifest(self):
        self.build()
        skill(self.root, self.names[0], "gamma")
        result = run("build_manifests.py", self.root, "--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(".grok-plugin/plugin-index.json", result.stderr)
        self.assertNotEqual(run("validate_plugin.py", self.root).returncode, 0)

    def test_duplicate_skill_across_plugins_is_rejected(self):
        skill(self.root, self.names[1], "alpha")
        self.build()
        result = run("validate_plugin.py", self.root)
        self.assertIn("duplicate skill name alpha", result.stderr)

    def test_bad_skills_are_rejected(self):
        skill(self.root, self.names[0], "Bad_Name")
        skill(self.root, self.names[0], "long", description="x" * 1025)
        nested = self.root / "plugins" / self.names[0] / "skills" / "group" / "inner"
        nested.mkdir(parents=True)
        (nested / "SKILL.md").write_text("---\nname: inner\ndescription: d\n---\n", encoding="utf-8")
        self.build()
        errors = run("validate_plugin.py", self.root).stderr
        self.assertIn("invalid skill name", errors)
        self.assertIn("description over 1024", errors)
        self.assertIn("skills/<name>/SKILL.md", errors)

    def test_plugin_folder_missing_from_catalog_is_rejected(self):
        skill(self.root, "stray", "delta")
        self.build()
        self.assertIn("differ from plugins/ folders", run("validate_plugin.py", self.root).stderr)

    def test_listing_budget_and_cross_plugin_links(self):
        policy = self.root / "policy.json"
        policy.write_text(json.dumps({"max_listed_skills_per_plugin": 1}), encoding="utf-8")
        skill(self.root, self.names[0], "listed-two")
        skill(self.root, self.names[0], "hidden", extra="disable-model-invocation: true\n")
        result = run("validate_skill_stack.py", self.root, "--policy", str(policy))
        self.assertIn("lists 2 model-invoked skills", result.stderr)
        policy.write_text(json.dumps({"max_listed_skills_per_plugin": 5}), encoding="utf-8")
        link = self.root / "plugins" / self.names[0] / "skills" / "alpha" / "SKILL.md"
        link.write_text(link.read_text(encoding="utf-8") + "\nSee [beta](../../../" + self.names[1] + "/skills/beta/SKILL.md).\n", encoding="utf-8")
        result = run("validate_skill_stack.py", self.root, "--policy", str(policy))
        self.assertIn("link leaves its plugin", result.stderr)


if __name__ == "__main__":
    unittest.main()
