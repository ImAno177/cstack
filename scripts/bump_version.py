from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    major, minor, patch = (int(part) for part in manifest["version"].split("."))
    manifest["version"] = f"{major}.{minor}.{patch + 1}"
    args.manifest.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(manifest["version"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
