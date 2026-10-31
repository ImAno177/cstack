from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", action="append", required=True, type=Path)
    args = parser.parse_args()
    versions = []
    for manifest_path in args.manifest:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        major, minor, patch = (int(part) for part in manifest["version"].split("."))
        manifest["version"] = f"{major}.{minor}.{patch + 1}"
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        versions.append(manifest["version"])
    if len(set(versions)) != 1:
        raise ValueError("all manifests must have the same version")
    print(versions[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
