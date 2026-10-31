from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import yaml


ALLOWED_FRONTMATTER = {"name", "description", "license", "metadata", "allowed-tools"}


def skill_dirs(root: Path) -> list[Path]:
    return [path for path in sorted(root.iterdir()) if path.is_dir() and (path / "SKILL.md").is_file()]


def copy_tree(source: Path, destination: Path) -> None:
    if not source.is_dir():
        return
    for skill in skill_dirs(source):
        target = destination / skill.name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(skill, target)


def normalize_skill(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing frontmatter: {path}")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError(f"unclosed frontmatter: {path}")
    frontmatter = yaml.safe_load(text[4:end])
    if not isinstance(frontmatter, dict):
        raise ValueError(f"frontmatter is not a mapping: {path}")
    normalized = {key: frontmatter[key] for key in frontmatter if key in ALLOWED_FRONTMATTER}
    if not normalized.get("name") or not normalized.get("description"):
        raise ValueError(f"name and description are required: {path}")
    body = text[end + len("\n---"):]
    serialized = yaml.safe_dump(normalized, allow_unicode=True, sort_keys=False, width=120).strip()
    path.write_text(f"---\n{serialized}\n---{body}", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    args = parser.parse_args()
    source_root = args.source_root.resolve()
    destination = args.destination.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    for child in destination.iterdir():
        if child.is_dir() or child.is_symlink():
            shutil.rmtree(child)
        else:
            child.unlink()
    copy_tree(source_root / "local" / "skills", destination)
    copy_tree(source_root / "upstream" / "pstack" / "skills", destination)
    copy_tree(source_root / "upstream" / "ponytail" / "skills", destination)
    for skill in skill_dirs(destination):
        normalize_skill(skill / "SKILL.md")
    print(f"built {len(skill_dirs(destination))} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
