from __future__ import annotations

import argparse
import json
import posixpath
import re
import shutil
from pathlib import Path

import yaml

from skill_artifacts import ignore_test_artifacts


ALLOWED_FRONTMATTER = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def skill_dirs(root: Path, excluded: set[str]) -> list[Path]:
    return [path for path in sorted(root.iterdir()) if path.name not in excluded and path.is_dir() and (path / "SKILL.md").is_file()]


def copy_tree(source: Path, destination: Path, excluded: set[str], resource_exclude: dict[str, set[str]]) -> None:
    if not source.is_dir():
        return
    for skill in skill_dirs(source, excluded):
        target = destination / skill.name
        if target.exists():
            shutil.rmtree(target)
        excluded_resources = resource_exclude.get(skill.name, set())

        def ignore(path: str, names: list[str]) -> set[str]:
            ignored = set(ignore_test_artifacts(path, names))
            if Path(path).resolve() == skill.resolve():
                ignored.update(excluded_resources)
            return ignored

        shutil.copytree(skill, target, ignore=ignore)


def normalize_skill(path: Path) -> None:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
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
    path.write_text(f"---\n{serialized}\n---{body}", encoding="utf-8", newline="\n")


def relocate_link(link: str) -> str:
    target, separator, fragment = link.partition("#")
    if not target or target.startswith(("http://", "https://", "mailto:")):
        return link
    relocated = posixpath.relpath(target, "references")
    return relocated + (separator + fragment if separator else "")


def compact_skill(skill: Path, max_lines: int) -> None:
    manifest_path = skill / "SKILL.md"
    lines = manifest_path.read_text(encoding="utf-8").splitlines(keepends=True)
    if len(lines) <= max_lines:
        return
    text = "".join(lines)
    end = text.find("\n---", 4)
    body = text[end + len("\n---"):].lstrip("\r\n")
    body = re.sub(r"(\]\()((?!https?://|mailto:)[^)#]+)", lambda match: match.group(1) + relocate_link(match.group(2)), body)
    references = skill / "references"
    references.mkdir(exist_ok=True)
    (references / "full-guide.md").write_text(body, encoding="utf-8", newline="\n")
    frontmatter = yaml.safe_load(text[4:end])
    title = frontmatter.get("name", skill.name)
    manifest_path.write_text(text[:end + len("\n---")] + f"\n\n# {title}\n\nRead [the full guide](references/full-guide.md) when this skill applies.\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--policy", required=True, type=Path)
    args = parser.parse_args()
    source_root = args.source_root.resolve()
    destination = args.destination.resolve()
    policy = json.loads(args.policy.read_text(encoding="utf-8"))
    excluded = set(policy.get("exclude", []))
    resource_exclude = {name: set(paths) for name, paths in policy.get("resource_exclude", {}).items()}
    max_entry_lines = int(policy.get("max_entry_lines", 160))
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("skills", "hooks", ".codex-plugin", ".grok-plugin"):
        target = destination / name
        if target.exists():
            shutil.rmtree(target)
    skills_destination = destination / "skills"
    skills_destination.mkdir(parents=True, exist_ok=True)
    copy_tree(source_root / "skills", skills_destination, excluded, resource_exclude)
    hooks_source = source_root / "hooks"
    if hooks_source.is_dir():
        shutil.copytree(hooks_source, destination / "hooks")
    for name in (".codex-plugin", ".grok-plugin"):
        source = source_root / name
        if source.is_dir():
            shutil.copytree(source, destination / name)
    manifest = source_root / "plugin.json"
    if manifest.is_file():
        shutil.copy2(manifest, destination / "plugin.json")
    readme = source_root / "README.md"
    if readme.is_file():
        shutil.copy2(readme, destination / "README.md")
    for skill in skill_dirs(skills_destination, excluded):
        normalize_skill(skill / "SKILL.md")
        compact_skill(skill, max_entry_lines)
    print(f"built general plugin with {len(skill_dirs(skills_destination, excluded))} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
