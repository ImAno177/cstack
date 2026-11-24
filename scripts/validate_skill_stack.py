"""Validate skill content across every plugin: links, host markers, entry size,
overlap groups, and how many skills each plugin puts in the model's listing."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


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


def validate_links(plugin_root: Path, path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for raw_target in LINK_PATTERN.findall(text):
        target = raw_target.strip().strip("<>").split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:", "data:", "/")):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"broken internal link: {path}: {raw_target}")
        elif plugin_root.resolve() not in resolved.parents:
            errors.append(f"link leaves its plugin, so it breaks once installed: {path}: {raw_target}")


def validate_overlap_groups(groups: list, descriptions: dict[str, str], errors: list[str]) -> None:
    for group in groups:
        if not isinstance(group, list) or len(group) < 2:
            errors.append(f"invalid overlap group: {group}")
            continue
        for name in group:
            description = descriptions.get(name)
            if description is None:
                errors.append(f"overlap group names unknown skill: {name}")
                continue
            for sibling in group:
                if sibling != name and not re.search(rf"(?<![a-z0-9-]){re.escape(sibling)}(?![a-z0-9-])", description):
                    errors.append(f"description of {name} does not name overlapping skill {sibling}")


def listed(metadata: dict) -> bool:
    return not metadata.get("disable-model-invocation")


ROUTE_TARGET = re.compile(r"\?([a-z0-9][a-z0-9-]*)\"'\s*$", re.M)


def routing_coverage(evals: Path) -> dict[str, set[str]]:
    """Map each skill a routing case expects to the tags of the cases that expect it."""
    coverage: dict[str, set[str]] = {}
    for grader in sorted(evals.glob("*/graders/routes.md")):
        text = grader.read_text(encoding="utf-8")
        if "max: 0" in text:
            continue
        match = ROUTE_TARGET.search(text)
        if not match:
            continue
        prompt = (grader.parent.parent / "prompt.md").read_text(encoding="utf-8")
        tags = re.search(r"^tags: \[(.*)\]$", prompt, re.M)
        names = {t.strip() for t in tags.group(1).split(",")} if tags else set()
        coverage.setdefault(match.group(1), set()).update(names)
    return coverage


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--policy", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    policy = json.loads((args.policy or root / ".cstack" / "skill-policy.json").read_text(encoding="utf-8"))
    host_markers = [marker.casefold() for marker in policy.get("host_markers", [])]
    max_entry_lines = int(policy.get("max_entry_lines", 160))
    max_listed = int(policy.get("max_listed_skills_per_plugin", 30))
    errors: list[str] = []
    descriptions: dict[str, str] = {}
    total = 0
    evals = root / "evals" / "routing"
    coverage = routing_coverage(evals) if evals.is_dir() else None
    exempt = tuple(policy.get("routing_eval_exempt_prefixes", []))

    for plugin_root in sorted(p for p in (root / "plugins").iterdir() if p.is_dir()):
        listed_count = 0
        for entrypoint in sorted((plugin_root / "skills").glob("*/SKILL.md")):
            skill = entrypoint.parent
            total += 1
            try:
                metadata = frontmatter(entrypoint)
            except (ValueError, yaml.YAMLError) as error:
                errors.append(str(error))
                continue
            name = metadata.get("name")
            description = metadata.get("description")
            if isinstance(name, str) and isinstance(description, str):
                descriptions[name] = description
            if listed(metadata):
                listed_count += 1
                if coverage is not None and isinstance(name, str) and not name.startswith(exempt):
                    missing = {"train", "test"} - coverage.get(name, set())
                    if missing:
                        errors.append(
                            f"listed skill {name} has no routing eval tagged {', '.join(sorted(missing))} in evals/routing; "
                            "add a realistic prompt that should trigger it"
                        )
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
            for document in skill.rglob("*.md"):
                validate_links(plugin_root, document, errors)
        if listed_count > max_listed:
            errors.append(
                f"{plugin_root.name} lists {listed_count} model-invoked skills; the policy allows {max_listed}. "
                "Mark user-started workflows disable-model-invocation, merge overlapping skills, or move a group to its own plugin."
            )

    validate_overlap_groups(policy.get("overlap_groups", []), descriptions, errors)

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"validated skill stack: {total} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
