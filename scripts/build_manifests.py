"""Generate every host manifest from .cstack/catalog.json.

Run with no arguments to write the files, or with --check to fail when any
generated file is missing or differs from what the catalog produces.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CATALOG = Path(".cstack/catalog.json")


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


def dump(value: object) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def plugin_dir(name: str) -> str:
    return f"plugins/{name}"


def skills_of(root: Path, name: str) -> list[dict]:
    skills = []
    for entry in sorted((root / plugin_dir(name) / "skills").glob("*/SKILL.md")):
        meta = frontmatter(entry)
        skills.append({"name": meta["name"], "description": str(meta["description"]).strip()})
    return skills


def hooks_of(root: Path, name: str) -> list[dict]:
    path = root / plugin_dir(name) / "hooks" / "hooks.json"
    if not path.is_file():
        return []
    hooks = json.loads(path.read_text(encoding="utf-8")).get("hooks", {})
    return [
        {"name": event, "description": ", ".join(item.get("matcher", "") for item in entries if item.get("matcher"))}
        for event, entries in sorted(hooks.items())
    ]


def outputs(root: Path) -> dict[str, str]:
    catalog = json.loads((root / CATALOG).read_text(encoding="utf-8"))
    version = catalog["version"]
    common = {
        "author": catalog["author"],
        "repository": catalog["repository"],
        "license": catalog["license"],
    }
    owner = catalog["author"]
    license_text = (root / "LICENSE").read_text(encoding="utf-8")
    files: dict[str, str] = {}

    claude_entries, codex_entries, grok_entries, cursor_entries = [], [], [], []
    grok_index = {}
    for plugin in catalog["plugins"]:
        name = plugin["name"]
        base = plugin_dir(name)
        if not (root / base / "skills").is_dir():
            raise ValueError(f"plugin {name} has no {base}/skills directory")
        description = plugin["description"]

        files[f"{base}/.claude-plugin/plugin.json"] = dump(
            {"name": name, "version": version, "description": description, **common,
             "homepage": catalog["repository"], "keywords": plugin["keywords"]}
        )
        files[f"{base}/.codex-plugin/plugin.json"] = dump(
            {"name": name, "version": version, "description": description, **common,
             "skills": "./skills/",
             "interface": {"displayName": plugin["displayName"], "shortDescription": description,
                           "developerName": owner["name"], "category": plugin["category"],
                           "websiteURL": catalog["repository"]}}
        )
        files[f"{base}/.grok-plugin/plugin.json"] = dump(
            {"name": name, "version": version, "description": description, **common, "skills": "./skills/"}
        )
        files[f"{base}/.cursor-plugin/plugin.json"] = dump(
            {"name": name, "displayName": plugin["displayName"], "version": version, "description": description,
             **common, "keywords": plugin["keywords"], "skills": "./skills/"}
        )
        files[f"{base}/LICENSE"] = license_text

        claude_entries.append({"name": name, "source": f"./{base}", "description": description,
                               "version": version, **common})
        codex_entries.append({"name": name, "source": {"source": "local", "path": f"./{base}"},
                              "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                              "category": plugin["category"]})
        grok_entries.append({"name": name, "description": description,
                             "source": {"type": "local", "path": f"./{base}"},
                             "category": plugin["category"].lower(), "homepage": catalog["repository"],
                             "keywords": plugin["keywords"]})
        cursor_entries.append({"name": name, "source": f"./{base}", "description": description})

        components: dict[str, list] = {"skills": skills_of(root, name)}
        hooks = hooks_of(root, name)
        if hooks:
            components["hooks"] = hooks
        grok_index[name] = {"version": version, "components": components}

    marketplace = {"name": catalog["name"], "owner": owner}
    files[".claude-plugin/marketplace.json"] = dump(
        {**marketplace, "metadata": {"description": catalog["description"], "version": version},
         "plugins": claude_entries}
    )
    files[".agents/plugins/marketplace.json"] = dump(
        {"name": catalog["name"], "interface": {"displayName": catalog["name"]}, "plugins": codex_entries}
    )
    files[".grok-plugin/marketplace.json"] = dump(
        {**marketplace, "description": catalog["description"], "plugins": grok_entries}
    )
    files[".grok-plugin/plugin-index.json"] = dump({"version": 1, "plugins": grok_index})
    files[".cursor-plugin/marketplace.json"] = dump({**marketplace, "plugins": cursor_entries})
    files["skills.sh.json"] = dump({"paths": [f"./{plugin_dir(p['name'])}/skills" for p in catalog["plugins"]]})
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    stale = []
    for relative, content in outputs(root).items():
        path = root / relative
        current = path.read_text(encoding="utf-8") if path.is_file() else None
        if current == content:
            continue
        if args.check:
            stale.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
    if stale:
        raise SystemExit("generated files are out of date; run python scripts/build_manifests.py:\n  " + "\n  ".join(stale))
    print("manifests are up to date" if args.check else "wrote manifests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
