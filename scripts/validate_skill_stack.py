from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml


ROUTE_PATTERN = re.compile(r"→|->")
BACKTICK_PATTERN = re.compile(r"`([^`]+)`")
LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def skill_dirs(root: Path, excluded: set[str]) -> list[Path]:
    if not root.is_dir():
        return []
    return [
        path
        for path in sorted(root.iterdir())
        if path.is_dir() and path.name not in excluded and (path / "SKILL.md").is_file()
    ]


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing frontmatter: {path}")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError(f"unclosed frontmatter: {path}")
    value = yaml.safe_load(text[4:end])
    if not isinstance(value, dict):
        raise ValueError(f"frontmatter is not a mapping: {path}")
    return value


def route_allowed(route: str, catalog: set[str], external: set[str]) -> bool:
    if route in catalog or route in external:
        return True
    if route.endswith(":*"):
        prefix = route[:-1]
        return any(name.startswith(prefix) for name in catalog | external)
    return False


def validate_links(catalog_root: Path, path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for raw_target in LINK_PATTERN.findall(text):
        target = raw_target.strip().strip("<>").split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:", "data:", "/")):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.is_file() or catalog_root.resolve() not in resolved.parents:
            errors.append(f"broken internal link: {path}: {raw_target}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--plugin-root", required=True, type=Path)
    parser.add_argument("--policy", required=True, type=Path)
    args = parser.parse_args()

    policy = json.loads(args.policy.read_text(encoding="utf-8"))
    excluded = set(policy.get("exclude", []))
    host_markers = [marker.casefold() for marker in policy.get("host_markers", [])]
    external_routes = set(policy.get("external_routes", []))
    max_entry_lines = int(policy.get("max_entry_lines", 160))
    errors: list[str] = []

    plugin_skills = skill_dirs(args.plugin_root / "skills", excluded)
    catalog: set[str] = set()
    for skill in plugin_skills:
        entrypoint = skill / "SKILL.md"
        try:
            metadata = frontmatter(entrypoint)
        except ValueError as error:
            errors.append(str(error))
            continue
        name = metadata.get("name")
        description = metadata.get("description")
        if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
            errors.append(f"invalid skill name: {entrypoint}")
        if not isinstance(description, str) or not description.strip():
            errors.append(f"missing skill description: {entrypoint}")
        if isinstance(name, str):
            if name in catalog:
                errors.append(f"duplicate skill name: {name}")
            catalog.add(name)
        if len(entrypoint.read_text(encoding="utf-8").splitlines()) > max_entry_lines:
            errors.append(f"entrypoint exceeds {max_entry_lines} lines: {entrypoint}")
        for artifact in skill.rglob("*"):
            if not artifact.is_file():
                continue
            try:
                text = artifact.read_text(encoding="utf-8").casefold()
            except UnicodeDecodeError:
                continue
            for marker in host_markers:
                if marker in text:
                    errors.append(f"host-specific instruction in {artifact}: {marker}")
        validate_links(args.plugin_root / "skills", entrypoint, errors)

    for excluded_name in excluded:
        if (args.plugin_root / "skills" / excluded_name).exists():
            errors.append(f"excluded skill is present in plugin: {excluded_name}")

    standalone_root = args.source_root / "skills"
    if not standalone_root.is_dir():
        errors.append(f"canonical source root is missing: {standalone_root}")
    source_roots = [standalone_root]
    source_catalog = {skill.name for root in source_roots for skill in skill_dirs(root, excluded)}
    for name in sorted(catalog - source_catalog):
        errors.append(f"plugin skill has no source provenance: {name}")

    router = args.plugin_root / "skills" / "skills-router" / "SKILL.md"
    if router.is_file():
        for line in router.read_text(encoding="utf-8").splitlines():
            if not ROUTE_PATTERN.search(line):
                continue
            routes = BACKTICK_PATTERN.findall(line.split("→", 1)[-1].split("->", 1)[-1])
            for route in routes:
                if route_allowed(route, catalog, external_routes):
                    continue
                errors.append(f"router points to missing skill: {route}")

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"validated skill stack: {len(catalog)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
