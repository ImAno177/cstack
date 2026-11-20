from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / 'scripts' / 'validate_plugin.py'
spec = importlib.util.spec_from_file_location('validate_plugin', MODULE_PATH)
validate = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(validate)


def make_skill(path: Path) -> Path:
    path.mkdir(parents=True)
    (path / 'SKILL.md').write_text('---\nname: x\ndescription: x\n---\n', encoding='utf-8')
    return path.resolve()


class ClaudeDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = (Path(self._tmp.name) / 'plugin').resolve()
        self.top = make_skill(self.root / 'skills' / 'top')
        self.nested = make_skill(self.root / 'skills' / 'group' / 'nested')

    def tearDown(self):
        self._tmp.cleanup()

    def test_nested_group_is_not_discovered_by_default(self):
        found = validate.claude_discovered_skill_dirs(self.root, {})
        self.assertIn(self.top, found)
        self.assertNotIn(self.nested, found)

    def test_listed_group_is_discovered(self):
        found = validate.claude_discovered_skill_dirs(self.root, {'skills': ['./skills/group/']})
        self.assertIn(self.nested, found)

    def test_string_value_is_accepted(self):
        found = validate.claude_discovered_skill_dirs(self.root, {'skills': './skills/group'})
        self.assertIn(self.nested, found)

    def test_directory_holding_skill_md_is_one_skill(self):
        found = validate.claude_discovered_skill_dirs(self.root, {'skills': ['./skills/group/nested']})
        self.assertIn(self.nested, found)

    def test_plugin_root_dot_is_accepted(self):
        make_skill(self.root / 'rootskill')
        found = validate.claude_discovered_skill_dirs(self.root, {'skills': ['.']})
        self.assertIn((self.root / 'rootskill').resolve(), found)

    def test_path_escaping_plugin_root_is_rejected(self):
        make_skill(self.root.parent / 'outside' / 'escaped')
        with self.assertRaisesRegex(ValueError, 'outside plugin'):
            validate.claude_discovered_skill_dirs(self.root, {'skills': ['./../outside']})

    def test_missing_path_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'missing'):
            validate.claude_discovered_skill_dirs(self.root, {'skills': ['./nope']})

    def test_path_without_dot_slash_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'relative'):
            validate.claude_discovered_skill_dirs(self.root, {'skills': ['skills/group']})


if __name__ == '__main__':
    unittest.main()


class AgentValidationTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def agent(self, stem: str, frontmatter: str) -> Path:
        path = self.dir / f'{stem}.md'
        path.write_text(f'---\n{frontmatter}\n---\nbody\n', encoding='utf-8')
        return path

    def test_valid_agent_returns_name(self):
        path = self.agent('verifier', 'name: verifier\ndescription: checks\nmodel: inherit\ntools: Read, Bash')
        self.assertEqual(validate.validate_agent(path), 'verifier')

    def test_full_model_id_is_accepted(self):
        validate.validate_agent(self.agent('a', 'name: a\ndescription: d\nmodel: claude-opus-5-5'))

    def test_name_must_match_file(self):
        with self.assertRaises(ValueError):
            validate.validate_agent(self.agent('verifier', 'name: other\ndescription: checks'))

    def test_missing_description_is_rejected(self):
        with self.assertRaises(ValueError):
            validate.validate_agent(self.agent('a', 'name: a'))

    def test_unknown_model_is_rejected(self):
        with self.assertRaises(ValueError):
            validate.validate_agent(self.agent('a', 'name: a\ndescription: d\nmodel: gpt'))

    def test_missing_frontmatter_is_rejected(self):
        path = self.dir / 'a.md'
        path.write_text('no frontmatter\n', encoding='utf-8')
        with self.assertRaises(ValueError):
            validate.validate_agent(path)
