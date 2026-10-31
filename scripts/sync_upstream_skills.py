from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def run(command: list[str]) -> None:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "command failed"
        raise RuntimeError(f"{' '.join(command)}: {detail}")


def tree_digest(root: Path) -> dict[str, str]:
    if root.is_file():
        paths = [root]
        base = root.parent
    else:
        paths = [path for path in root.rglob("*") if path.is_file()]
        base = root
    digest: dict[str, str] = {}
    for path in sorted(paths):
        relative = path.name if root.is_file() else path.relative_to(base).as_posix()
        digest[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def replace_managed_path(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    stage_root = Path(tempfile.mkdtemp(prefix=f".{target.name}-stage-", dir=target.parent))
    stage = stage_root / target.name
    backup = Path(tempfile.mkdtemp(prefix=f".{target.name}-backup-", dir=target.parent))
    backup.rmdir()
    try:
        if source.is_dir():
            shutil.copytree(source, stage)
        else:
            stage.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, stage)
        if target.exists():
            target.rename(backup)
        stage.rename(target)
    except Exception:
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        if backup.exists():
            backup.rename(target)
        raise
    finally:
        if backup.exists():
            if backup.is_dir():
                shutil.rmtree(backup)
            else:
                backup.unlink()
        if stage_root.exists():
            shutil.rmtree(stage_root)
        if backup.exists():
            shutil.rmtree(backup)


def checkout_repositories(repo_root: Path, specs: list[dict], temporary: Path) -> dict[tuple[str, str], Path]:
    groups: dict[tuple[str, str], list[dict]] = {}
    for spec in specs:
        key = (spec["repository"], spec.get("ref", "main"))
        groups.setdefault(key, []).append(spec)
    checkouts: dict[tuple[str, str], Path] = {}
    for index, ((repository, ref), group) in enumerate(sorted(groups.items())):
        checkout = temporary / f"repo-{index}"
        run([
            "git", "clone", "--depth", "1", "--branch", ref, "--filter=blob:none", "--sparse",
            f"https://github.com/{repository}.git", str(checkout),
        ])
        paths = sorted({spec["path"] for spec in group})
        run(["git", "-C", str(checkout), "sparse-checkout", "set", "--no-cone", *paths])
        checkouts[(repository, ref)] = checkout
    return checkouts


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--manifest", type=Path, default=Path(".cstack/upstreams.json"))
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    manifest_path = (repo_root / args.manifest).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    specs = manifest.get("skills")
    if not isinstance(specs, list) or not specs:
        raise SystemExit("upstream manifest has no skills")

    with tempfile.TemporaryDirectory(prefix="cstack-upstreams-") as temporary_name:
        checkouts = checkout_repositories(repo_root, specs, Path(temporary_name))
        mismatches: list[str] = []
        for spec in specs:
            key = (spec["repository"], spec.get("ref", "main"))
            source = checkouts[key] / spec["path"]
            target = (repo_root / spec["destination"]).resolve()
            if repo_root.resolve() not in target.parents:
                raise SystemExit(f"upstream destination escapes repository: {spec['destination']}")
            if not source.exists():
                raise SystemExit(f"upstream path is missing: {spec['repository']}:{spec['path']}")
            if args.check:
                if not target.exists() or tree_digest(source) != tree_digest(target):
                    mismatches.append(spec["name"])
            else:
                replace_managed_path(source, target)
                print(f"synced {spec['name']} from {spec['repository']}@{spec.get('ref', 'main')}")
        if mismatches:
            raise SystemExit("upstream skills are out of date: " + ", ".join(mismatches))
    if args.check:
        print("upstream skills are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
