from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from skill_artifacts import ignore_test_artifacts


def copy_skill_tree(source: Path, destination: Path) -> int:
    source = source.resolve()
    destination = destination.resolve()
    if source == destination:
        raise ValueError("source and destination must be different")
    if not source.is_dir():
        raise FileNotFoundError(source)
    skills = [path for path in source.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()]
    destination.mkdir(parents=True, exist_ok=True)
    for child in destination.iterdir():
        if child.is_dir() or child.is_symlink():
            shutil.rmtree(child)
        else:
            child.unlink()
    for skill in skills:
        shutil.copytree(skill, destination / skill.name, ignore=ignore_test_artifacts)
    return len(skills)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    args = parser.parse_args()
    count = copy_skill_tree(args.source, args.destination)
    print(f"synced {count} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
