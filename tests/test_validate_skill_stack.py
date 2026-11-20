import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from validate_skill_stack import validate_frontmatter, validate_overlap_groups


class OverlapGroupTests(unittest.TestCase):
    def check(self, groups, descriptions):
        errors: list[str] = []
        validate_overlap_groups(groups, descriptions, errors)
        return errors

    def test_members_naming_each_other_pass(self):
        descriptions = {"a-skill": "Not for x; use b-skill.", "b-skill": "Not for y; use `a-skill`."}
        self.assertEqual(self.check([["a-skill", "b-skill"]], descriptions), [])

    def test_missing_sibling_reported(self):
        descriptions = {"a-skill": "Does a.", "b-skill": "Use a-skill instead."}
        self.assertEqual(
            self.check([["a-skill", "b-skill"]], descriptions),
            ["description of a-skill does not name overlapping skill b-skill"],
        )

    def test_prefix_of_longer_name_does_not_count(self):
        descriptions = {"review": "Use change-review-x.", "change-review-x": "Use review."}
        self.assertEqual(
            self.check([["review", "change-review-x"]], descriptions),
            [],
        )
        descriptions = {"review": "Use change-review.", "change-review-x": "Use review."}
        self.assertIn(
            "description of review does not name overlapping skill change-review-x",
            self.check([["review", "change-review-x"]], descriptions),
        )

    def test_unknown_and_invalid_groups_reported(self):
        errors = self.check([["ghost", "a"], ["solo"]], {"a": "ghost"})
        self.assertIn("overlap group names unknown skill: ghost", errors)
        self.assertIn("invalid overlap group: ['solo']", errors)


class FrontmatterTests(unittest.TestCase):
    ALLOWED = {"name", "description", "compatibility"}

    def check(self, metadata):
        errors: list[str] = []
        validate_frontmatter(metadata, Path("skills/x/SKILL.md"), self.ALLOWED, errors)
        return errors

    def test_allowed_keys_pass(self):
        self.assertEqual(self.check({"name": "x", "description": "d", "compatibility": "needs gh"}), [])

    def test_unknown_key_reported(self):
        self.assertEqual(
            self.check({"name": "x", "description": "d", "class": "workflow"}),
            ["unsupported frontmatter key in skills/x/SKILL.md: class"],
        )

    def test_long_description_reported(self):
        self.assertEqual(len(self.check({"name": "x", "description": "d" * 1025})), 1)
        self.assertEqual(self.check({"name": "x", "description": "d" * 1024}), [])

    def test_long_or_non_string_compatibility_reported(self):
        self.assertEqual(len(self.check({"name": "x", "description": "d", "compatibility": "c" * 501})), 1)
        self.assertEqual(len(self.check({"name": "x", "description": "d", "compatibility": ["a"]})), 1)


if __name__ == "__main__":
    unittest.main()
