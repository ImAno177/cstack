"""Summarize the cstack skill-usage log written by hooks/usage-log.js and hooks/model-skill.js."""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
from pathlib import Path


def default_log() -> Path:
    data = os.environ.get("CLAUDE_PLUGIN_DATA") or str(Path.home() / ".claude" / "plugins" / "data" / "cstack-cstack")
    return Path(data) / "logs" / "skill-usage.jsonl"


def listed_skills(root: Path) -> set[str]:
    names = set()
    for entry in root.glob("plugins/*/skills/*/SKILL.md"):
        text = entry.read_text(encoding="utf-8")
        front = text.split("---", 2)[1] if text.startswith("---") else ""
        if not re.search(r"^disable-model-invocation:\s*true\s*$", front, re.M):
            names.add(entry.parent.name)
    return names


def load(path: Path) -> list[dict]:
    rows = []
    if not path.is_file():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def short(skill: str) -> str:
    return skill.split(":", 1)[-1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, default=default_log())
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    rows = load(args.log)
    if not rows:
        print(f"no usage records in {args.log}")
        return 0

    sessions = {r.get("session_id") for r in rows if r.get("event") == "SessionStart"}
    subagents = {(r.get("session_id"), r.get("agent_id")) for r in rows if r.get("event") == "SubagentStart"}
    injected = collections.Counter((r.get("model"), r.get("skill")) for r in rows if r.get("via") == "hook")
    opened = collections.Counter(short(r["skill"]) for r in rows if r.get("via") in ("Skill", "Read") and r.get("skill"))

    print(f"log: {args.log}")
    print(f"sessions started: {len(sessions)}; subagents started: {len(subagents)}")
    print("\nmodel skill injected by hook:")
    for (model, skill), n in injected.most_common():
        print(f"  {n:5d}  {skill}  ({model})")
    print("\nskills opened by the agent (Skill tool or a read of SKILL.md):")
    for skill, n in opened.most_common():
        print(f"  {n:5d}  {skill}")

    never = sorted(listed_skills(args.root) - set(opened))
    print(f"\nlisted skills never opened ({len(never)}):")
    for skill in never:
        print(f"  {skill}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
