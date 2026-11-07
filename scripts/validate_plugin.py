from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml


NAME_PATTERN = re.compile(r'^[a-z0-9][a-z0-9-]{0,63}$')
VERSION_PATTERN = re.compile(r'^\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?$')


def validate_skill(path: Path) -> str:
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        raise ValueError(f'missing frontmatter: {path}')
    end = text.find('\n---', 4)
    if end < 0:
        raise ValueError(f'unclosed frontmatter: {path}')
    frontmatter = yaml.safe_load(text[4:end])
    if not isinstance(frontmatter, dict):
        raise ValueError(f'frontmatter is not a mapping: {path}')
    name = frontmatter.get('name')
    description = frontmatter.get('description')
    if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
        raise ValueError(f'invalid skill name: {path}')
    if not isinstance(description, str) or not description.strip():
        raise ValueError(f'invalid skill description: {path}')
    return name


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as error:
        raise ValueError(f'invalid JSON: {path}: {error}') from error


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True, type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    package = load_json(root / 'plugin.json')
    if not isinstance(package, dict):
        raise ValueError('plugin.json must be an object')
    if not isinstance(package.get('name'), str) or not NAME_PATTERN.fullmatch(package['name']):
        raise ValueError('plugin.json has an invalid name')
    version = package.get('version')
    if not isinstance(version, str) or not VERSION_PATTERN.fullmatch(version):
        raise ValueError('plugin.json has an invalid semantic version')
    if package.get('license') != 'MIT' or not (root / 'LICENSE').is_file():
        raise ValueError('MIT license declaration requires a root LICENSE file')

    for relative in ('.codex-plugin/plugin.json', '.grok-plugin/plugin.json'):
        manifest = load_json(root / relative)
        if not isinstance(manifest, dict) or manifest.get('version') != version or manifest.get('name') != package['name']:
            raise ValueError(f'inconsistent plugin version/name in {relative}')
    for relative in ('.grok-plugin/marketplace.json', '.agents/plugins/marketplace.json'):
        manifest = load_json(root / relative)
        if not isinstance(manifest, dict) or not isinstance(manifest.get('plugins'), list):
            raise ValueError(f'invalid marketplace: {relative}')

    claude_path = root / '.claude-plugin/marketplace.json'
    claude = load_json(claude_path)
    if not isinstance(claude, dict) or not isinstance(claude.get('plugins'), list):
        raise ValueError('invalid Claude Code marketplace')
    matches = [entry for entry in claude['plugins'] if isinstance(entry, dict) and entry.get('name') == package['name']]
    if len(matches) != 1 or matches[0].get('version') != version:
        raise ValueError('Claude Code marketplace version/name differs from plugin.json')

    skills_root = root / 'skills'
    seen: set[str] = set()
    for entry in sorted(skills_root.rglob('SKILL.md')):
        name = validate_skill(entry)
        if name in seen:
            raise ValueError(f'duplicate skill name: {name}')
        seen.add(name)
    print(f'validated plugin {package["name"]} {version} with {len(seen)} skills')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
