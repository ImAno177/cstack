from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from skill_artifacts import ignore_test_artifacts


def replace_tree(source: Path, destination: Path) -> list[str]:
    source = source.resolve()
    destination = destination.resolve()
    if not source.is_dir():
        raise FileNotFoundError(source)
    destination.mkdir(parents=True, exist_ok=True)
    for child in destination.iterdir():
        if child.is_dir() or child.is_symlink():
            shutil.rmtree(child)
        else:
            child.unlink()
    names = []
    for skill in sorted(source.iterdir()):
        if skill.is_dir() and (skill / "SKILL.md").is_file():
            shutil.copytree(skill, destination / skill.name, ignore=ignore_test_artifacts)
            names.append(skill.name)
    return names


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--upstream", action="append", nargs=2, metavar=("NAME", "PATH"), required=True)
    args = parser.parse_args()
    manifest = {}
    for name, path_value in args.upstream:
        destination = args.source / name / "skills"
        manifest[name] = replace_tree(Path(path_value), destination)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({name: len(skills) for name, skills in manifest.items()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
