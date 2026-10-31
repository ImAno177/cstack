from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml


NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")


def validate_skill(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing frontmatter: {path}")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError(f"unclosed frontmatter: {path}")
    frontmatter = yaml.safe_load(text[4:end])
    if not isinstance(frontmatter, dict):
        raise ValueError(f"frontmatter is not a mapping: {path}")
    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
        raise ValueError(f"invalid skill name: {path}")
    if not isinstance(description, str) or not description.strip():
        raise ValueError(f"invalid skill description: {path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = root / "plugin.json"
    package = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(package.get("name"), str) or not NAME_PATTERN.fullmatch(package["name"]):
        raise ValueError("plugin.json has an invalid name")
    if not isinstance(package.get("version"), str) or not package["version"]:
        raise ValueError("plugin.json has no version")
    skills_root = root / "skills"
    seen = set()
    for manifest_path in sorted(skills_root.rglob("SKILL.md")):
        skill = manifest_path.parent
        validate_skill(manifest_path)
        name = yaml.safe_load(manifest_path.read_text(encoding="utf-8").split("\n---", 1)[0][4:])["name"]
        if name in seen:
            raise ValueError(f"duplicate skill name: {name}")
        seen.add(name)
    print(f"validated plugin {package['name']} with {len(seen)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
