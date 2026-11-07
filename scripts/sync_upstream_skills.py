from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path, PurePosixPath


LOCK_PATH = Path('.cstack/upstreams.lock.json')
REPOSITORY_PATTERN = re.compile(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+')


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or 'command failed'
        raise RuntimeError(f"{' '.join(command)}: {detail}")
    return result.stdout.strip()


def relative_path(value: str, field: str) -> Path:
    if not isinstance(value, str) or not value or '\\' in value:
        raise ValueError(f'invalid upstream {field}: {value!r}')
    pure = PurePosixPath(value)
    if pure.is_absolute() or any(part in ('.', '..') for part in value.split('/')):
        raise ValueError(f'unsafe upstream {field}: {value!r}')
    return Path(*pure.parts)


def validate_specs(specs: object) -> list[dict]:
    if not isinstance(specs, list) or not specs:
        raise ValueError('upstream manifest has no skills')
    seen_names: set[str] = set()
    destinations: list[Path] = []
    for spec in specs:
        if not isinstance(spec, dict):
            raise ValueError(f'upstream entry must be a mapping: {spec!r}')
        if not isinstance(spec.get('name'), str) or not spec['name']:
            raise ValueError(f'upstream entry has no name: {spec!r}')
        if spec['name'] in seen_names:
            raise ValueError(f'duplicate upstream name: {spec["name"]}')
        seen_names.add(spec['name'])
        repository = spec.get('repository')
        if not isinstance(repository, str) or not REPOSITORY_PATTERN.fullmatch(repository):
            raise ValueError(f'invalid upstream repository: {repository!r}')
        ref = spec.get('ref', 'main')
        if not isinstance(ref, str) or not re.fullmatch(r'[A-Za-z0-9._/-]+', ref) or ref.startswith(('-', '/')) or '..' in ref:
            raise ValueError(f'invalid upstream ref: {ref!r}')
        relative_path(spec.get('path'), 'path')
        destination = relative_path(spec.get('destination'), 'destination')
        if len(destination.parts) < 3 or destination.parts[0] != 'skills':
            raise ValueError(f'upstream destination must be in skills/: {destination}')
        if any(destination == other or destination in other.parents or other in destination.parents for other in destinations):
            raise ValueError(f'overlapping upstream destinations: {destination}')
        destinations.append(destination)
    return specs


def tree_digest(root: Path) -> dict[str, str]:
    if root.is_symlink():
        raise ValueError(f'upstream contains symlink: {root}')
    if root.is_file():
        paths = [root]
        base = root.parent
    else:
        paths = [path for path in root.rglob('*') if path.is_file() or path.is_symlink()]
        base = root
    digest: dict[str, str] = {}
    for path in sorted(paths):
        if path.is_symlink():
            raise ValueError(f'upstream contains symlink: {path}')
        relative = path.name if root.is_file() else path.relative_to(base).as_posix()
        digest[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def directory_sha256(root: Path) -> str:
    encoded = json.dumps(tree_digest(root), sort_keys=True, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def replace_managed_path(source: Path, target: Path) -> None:
    if target.is_symlink():
        raise ValueError(f'refusing to replace symlink: {target}')
    tree_digest(source)  # Reject symlinks before touching an existing installation.
    target.parent.mkdir(parents=True, exist_ok=True)
    stage_root = Path(tempfile.mkdtemp(prefix=f'.{target.name}-stage-', dir=target.parent))
    stage = stage_root / target.name
    backup = Path(tempfile.mkdtemp(prefix=f'.{target.name}-backup-', dir=target.parent))
    backup.rmdir()
    backed_up = False
    try:
        if source.is_dir():
            shutil.copytree(source, stage)
        else:
            shutil.copy2(source, stage)
        if target.exists():
            target.rename(backup)
            backed_up = True
        stage.rename(target)
    except Exception:
        if backed_up:
            try:
                if target.exists() or target.is_symlink():
                    remove_path(target)
                backup.rename(target)
            except Exception as restore_error:
                raise RuntimeError(
                    f'upstream update failed; original preserved at {backup}. Restore it manually.'
                ) from restore_error
        raise
    else:
        if backed_up and backup.exists():
            remove_path(backup)
    finally:
        shutil.rmtree(stage_root, ignore_errors=True)


def checkout_repositories(specs: list[dict], temporary: Path) -> dict[tuple[str, str], Path]:
    groups: dict[tuple[str, str], list[dict]] = {}
    for spec in specs:
        key = (spec['repository'], spec.get('ref', 'main'))
        groups.setdefault(key, []).append(spec)
    checkouts: dict[tuple[str, str], Path] = {}
    for index, ((repository, ref), group) in enumerate(sorted(groups.items())):
        checkout = temporary / f'repo-{index}'
        run([
            'git', 'clone', '--depth', '1', '--branch', ref, '--filter=blob:none', '--sparse',
            f'https://github.com/{repository}.git', str(checkout),
        ])
        paths = sorted({spec['path'] for spec in group})
        run(['git', '-C', str(checkout), 'sparse-checkout', 'set', '--no-cone', *paths])
        checkouts[(repository, ref)] = checkout
    return checkouts


def entry_identity(spec: dict) -> dict[str, str]:
    return {key: spec.get(key, 'main') if key == 'ref' else spec[key]
            for key in ('name', 'repository', 'ref', 'path', 'destination')}


def verify_lock(repo_root: Path, specs: list[dict], lock_path: Path) -> None:
    lock = json.loads(lock_path.read_text(encoding='utf-8'))
    if not isinstance(lock, dict) or lock.get('version') != 1 or not isinstance(lock.get('skills'), list):
        raise ValueError('invalid upstream lockfile')
    entries = {item['name']: item for item in lock['skills']}
    if len(entries) != len(lock['skills']) or set(entries) != {item['name'] for item in specs}:
        raise ValueError('upstream lockfile does not match the manifest')
    for spec in specs:
        locked = entries[spec['name']]
        if any(locked.get(key) != value for key, value in entry_identity(spec).items()):
            raise ValueError(f'upstream lock identity differs: {spec["name"]}')
        if not re.fullmatch('[a-f0-9]{40}', str(locked.get('commit', ''))):
            raise ValueError(f'upstream lock missing commit SHA: {spec["name"]}')
        destination = repo_root / relative_path(spec['destination'], 'destination')
        if not destination.is_dir() or directory_sha256(destination) != locked.get('sha256'):
            raise ValueError(f'upstream content differs from lock: {spec["name"]}')
    print('verified pinned upstream snapshot (no network)')


def atomic_write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f'.{path.name}-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as output:
            json.dump(value, output, indent=2, ensure_ascii=False)
            output.write('\n')
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--manifest', type=Path, default=Path('.cstack/upstreams.json'))
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    manifest_path = (repo_root / args.manifest).resolve()
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    specs = validate_specs(manifest.get('skills'))
    lock_path = repo_root / LOCK_PATH

    if args.check and lock_path.is_file():
        verify_lock(repo_root, specs, lock_path)
        return 0

    if args.check:
        print('no upstream lock yet; verifying against current remote branches')
    with tempfile.TemporaryDirectory(prefix='cstack-upstreams-') as temporary_name:
        checkouts = checkout_repositories(specs, Path(temporary_name))
        mismatches: list[str] = []
        lock_entries: list[dict[str, str]] = []
        for spec in specs:
            key = (spec['repository'], spec.get('ref', 'main'))
            checkout = checkouts[key]
            raw_source = checkout / relative_path(spec['path'], 'path')
            raw_target = repo_root / relative_path(spec['destination'], 'destination')
            if raw_source.is_symlink():
                raise ValueError(f'upstream source is a symlink: {spec["name"]}')
            ancestor = repo_root
            for component in relative_path(spec['destination'], 'destination').parts:
                ancestor /= component
                if ancestor.is_symlink():
                    raise ValueError(f'upstream destination contains a symlink: {spec["name"]}')
            source = raw_source.resolve()
            target = raw_target.resolve()
            if checkout.resolve() not in source.parents or repo_root.resolve() not in target.parents:
                raise ValueError(f'upstream path escapes a repository: {spec["name"]}')
            if not source.exists():
                raise ValueError(f'upstream path is missing: {spec["repository"]}:{spec["path"]}')
            tree_digest(source)
            if args.check:
                if not target.exists() or tree_digest(source) != tree_digest(target):
                    mismatches.append(spec['name'])
            else:
                replace_managed_path(source, target)
                commit = run(['git', '-C', str(checkout), 'rev-parse', 'HEAD'])
                lock_entries.append({
                    **entry_identity(spec),
                    'commit': commit,
                    'sha256': directory_sha256(target),
                })
                print(f'synced {spec["name"]} from {spec["repository"]}@{commit}')
        if mismatches:
            raise SystemExit('upstream skills are out of date: ' + ', '.join(mismatches))
    if args.write:
        atomic_write_json(lock_path, {'version': 1, 'skills': sorted(lock_entries, key=lambda item: item['name'])})
        print(f'updated {LOCK_PATH}')
    else:
        print('upstream skills are current')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
