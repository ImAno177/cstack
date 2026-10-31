from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


INDEX_PATH = Path(".grok-plugin/plugin-index.json")
CATALOG_PATH = Path(".grok-plugin/marketplace.json")


def read_metadata(path: Path) -> dict:
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


def resolve_local(repo_root: Path, source: object, name: str) -> Path:
    if isinstance(source, str):
        path = source
    elif isinstance(source, dict) and isinstance(source.get("path"), str):
        path = source["path"]
    else:
        raise ValueError(f"plugin '{name}' has an unsupported source")
    resolved = (repo_root / path).resolve()
    if resolved != repo_root.resolve() and repo_root.resolve() not in resolved.parents:
        raise ValueError(f"plugin '{name}' source escapes the repository: {path}")
    if not resolved.is_dir():
        raise ValueError(f"plugin '{name}' source is missing: {path}")
    return resolved


def components(plugin_root: Path) -> dict:
    result: dict[str, list[dict[str, str]]] = {}
    skills = []
    skills_root = plugin_root / "skills"
    if skills_root.is_dir():
        for skill in sorted(skills_root.iterdir()):
            entrypoint = skill / "SKILL.md"
            if not entrypoint.is_file():
                continue
            metadata = read_metadata(entrypoint)
            skills.append({"name": metadata["name"], "description": str(metadata["description"]).strip()})
    if skills:
        result["skills"] = skills

    hooks_path = plugin_root / "hooks" / "hooks.json"
    if hooks_path.is_file():
        hooks = json.loads(hooks_path.read_text(encoding="utf-8")).get("hooks", {})
        result["hooks"] = [
            {"name": name, "description": ", ".join(item.get("matcher", "") for item in entries if item.get("matcher"))}
            for name, entries in sorted(hooks.items())
        ]
    return result


def generate(repo_root: Path) -> dict:
    catalog = json.loads((repo_root / CATALOG_PATH).read_text(encoding="utf-8"))
    plugins = {}
    for entry in catalog.get("plugins", []):
        name = entry.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError("catalog entry without a name")
        root = resolve_local(repo_root, entry.get("source"), name)
        manifest = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
        plugins[name] = {
            "version": manifest.get("version", "0.0.0"),
            "components": components(root),
        }
    return {"version": 1, "plugins": {name: plugins[name] for name in sorted(plugins)}}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    output = json.dumps(generate(repo_root), indent=2, ensure_ascii=False) + "\n"
    index = repo_root / INDEX_PATH
    if args.check:
        if not index.is_file() or index.read_text(encoding="utf-8") != output:
            raise SystemExit(f"{INDEX_PATH} is out of date; regenerate it")
        print(f"validated Grok plugin index: {INDEX_PATH}")
        return 0
    index.write_text(output, encoding="utf-8", newline="\n")
    print(f"generated Grok plugin index: {INDEX_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
