"""Validate the marketplace packaging: catalog, generated manifests, skills, agents, and hooks."""

from __future__ import annotations

import argparse
import json
import re
import sys

import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_manifests import CATALOG, frontmatter, outputs  # noqa: E402

NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?$")
MAX_DESCRIPTION = 1024
HOOK_SCRIPT = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^\"\\\s]+)")


def validate_skill(entry: Path, errors: list[str]) -> str | None:
    try:
        meta = frontmatter(entry)
    except (ValueError, yaml.YAMLError) as error:
        errors.append(str(error))
        return None
    name, description = meta.get("name"), meta.get("description")
    if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
        errors.append(f"invalid skill name: {entry}")
        return None
    if name != entry.parent.name:
        errors.append(f"skill name {name} differs from its folder: {entry}")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"missing skill description: {entry}")
    elif len(description) > MAX_DESCRIPTION:
        errors.append(f"description over {MAX_DESCRIPTION} characters: {entry}")
    return name


def validate_plugin_dir(root: Path, plugin: str, errors: list[str], seen: dict[str, str]) -> int:
    base = root / "plugins" / plugin
    count = 0
    for entry in sorted(base.rglob("SKILL.md")):
        relative = entry.relative_to(base)
        if len(relative.parts) != 3 or relative.parts[0] != "skills":
            errors.append(f"SKILL.md must sit at skills/<name>/SKILL.md: plugins/{plugin}/{relative.as_posix()}")
            continue
        name = validate_skill(entry, errors)
        if name is None:
            continue
        if name in seen:
            errors.append(f"duplicate skill name {name} in {plugin} and {seen[name]}")
        seen[name] = plugin
        count += 1
    for agent in sorted((base / "agents").glob("*.md")):
        try:
            meta = frontmatter(agent)
        except ValueError as error:
            errors.append(str(error))
            continue
        if not meta.get("name") or not meta.get("description"):
            errors.append(f"agent needs name and description: {agent}")
        for skill in meta.get("skills") or []:
            if not (base / "skills" / skill / "SKILL.md").is_file():
                errors.append(f"agent {agent.name} preloads a skill outside its plugin: {skill}")
    hooks = base / "hooks" / "hooks.json"
    if hooks.is_file():
        text = hooks.read_text(encoding="utf-8")
        json.loads(text)
        for script in HOOK_SCRIPT.findall(text):
            if not (base / script).is_file():
                errors.append(f"hook command points at a missing file: plugins/{plugin}/{script}")
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []

    catalog = json.loads((root / CATALOG).read_text(encoding="utf-8"))
    if not VERSION_PATTERN.fullmatch(str(catalog.get("version", ""))):
        errors.append("catalog version is not semantic")
    if catalog.get("license") != "MIT" or not (root / "LICENSE").is_file():
        errors.append("MIT license declaration requires a root LICENSE file")
    names = [p.get("name") for p in catalog.get("plugins", [])]
    for name in names:
        if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
            errors.append(f"invalid plugin name in catalog: {name}")
    on_disk = sorted(p.name for p in (root / "plugins").iterdir() if p.is_dir())
    if sorted(names) != on_disk:
        errors.append(f"catalog plugins {sorted(names)} differ from plugins/ folders {on_disk}")
    stray = [p.relative_to(root).as_posix() for p in root.glob("*/SKILL.md")] + (
        ["skills/"] if (root / "skills").exists() else []
    )
    if stray:
        errors.append(f"skills must live inside a plugin: {stray}")

    for relative, content in outputs(root).items():
        path = root / relative
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            errors.append(f"generated file out of date: {relative} (run python scripts/build_manifests.py)")

    seen: dict[str, str] = {}
    counts = {name: validate_plugin_dir(root, name, errors, seen) for name in names if name in on_disk}

    if errors:
        raise SystemExit("\n".join(errors))
    summary = ", ".join(f"{name} {count}" for name, count in counts.items())
    print(f"validated cstack {catalog['version']}: {summary} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
