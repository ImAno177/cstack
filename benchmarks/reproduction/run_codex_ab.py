#!/usr/bin/env python3
"""Run independent Codex A/B reproduction trials. Requires Codex CLI and a configured login."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "benchmarks" / "reproduction" / "micrograd"
TASK = FIXTURE / "TASK.md"
GRADER = FIXTURE / "grade.py"


def stage_skills(source: Path, workspace: Path) -> int:
    skills_dir = workspace / ".agents" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for entry in sorted((source / "skills").rglob("SKILL.md")):
        original = entry.parent
        # Each skill is a complete bundle, even when the cstack repo nests it by platform.
        name = original.name
        target = skills_dir / name
        if target.exists():
            raise ValueError(f"skill directory collision: {name}")
        shutil.copytree(original, target, symlinks=False)
        count += 1
    if count == 0:
        raise ValueError(f"no skills in {source}")
    return count


def codex_tokens(log_path: Path) -> int | None:
    # The Codex event schema can evolve. Only collect explicit usage numbers.
    latest = None
    for line in log_path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        usage = event.get("usage")
        if usage is None and isinstance(event.get("item"), dict):
            usage = event["item"].get("usage")
        if isinstance(usage, dict):
            total = usage.get("total_tokens")
            if isinstance(total, int):
                latest = total
    return latest


SKILL_READ = re.compile(r"\.agents/skills/([a-z0-9][a-z0-9-]*)/SKILL\.md")
READ_COMMAND = re.compile(r"(?:^|[\s;&|('\"])(?:cat|head|tail|sed|less|more|nl|bat|awk)\s")


def commands(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "command" and isinstance(item, str):
                yield item
            elif key == "command" and isinstance(item, list):
                yield " ".join(str(part) for part in item)
            else:
                yield from commands(item)
    elif isinstance(value, list):
        for item in value:
            yield from commands(item)


def skills_opened(log_path: Path) -> list[str]:
    opened = set()
    for line in log_path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        for command in commands(event):
            if READ_COMMAND.search(command):
                opened.update(SKILL_READ.findall(command))
    return sorted(opened)


def paired_deltas(rows: list[dict], runs: int) -> list[int]:
    deltas = []
    for run in range(1, runs + 1):
        pair = {x["variant"]: x for x in rows if x["run"] == run}
        if all(v in pair and pair[v]["status"] == "finished" for v in ("baseline", "skills")):
            deltas.append(pair["skills"]["grade"]["passed"] - pair["baseline"]["grade"]["passed"])
    return deltas


async def run_trial(
    *,
    model: str,
    variant: str,
    run: int,
    codex_bin: str,
    cstack: Path,
    out: Path,
    timeout: int,
) -> dict:
    workspace = out / "workspaces" / f"{variant}-{run}"
    workspace.mkdir(parents=True, exist_ok=False)
    installed = stage_skills(cstack, workspace) if variant == "skills" else 0
    prompt = TASK.read_text(encoding="utf-8")
    prompt += (
        "\n\nImplement ONLY within the current workspace. Do not open files outside "
        "the workspace or inspect other trials. Do not inspect grader or reference code. "
        "Do not access network. Do not use preinstalled global skills.\n"
    )
    command = [
        codex_bin, "exec", "--json", "--skip-git-repo-check",
        "--sandbox", "workspace-write", "-C", str(workspace),
        "--model", model, "-"
    ]
    events_path = out / "logs" / f"{variant}-{run}.jsonl"
    errors_path = out / "logs" / f"{variant}-{run}.stderr"
    events_path.parent.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    status = "finished"
    try:
        process = await asyncio.create_subprocess_exec(
            *command, stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(prompt.encode("utf-8")), timeout=timeout
            )
        except asyncio.TimeoutError:
            process.kill()
            stdout, stderr = await process.communicate()
            status = "timeout"
        codex_rc = process.returncode
        events_path.write_bytes(stdout)
        errors_path.write_bytes(stderr)
    except OSError as exc:
        status = "launch_error"
        codex_rc = None
        events_path.write_text("", encoding="utf-8")
        errors_path.write_text(str(exc), encoding="utf-8")

    seconds = round(time.monotonic() - start, 3)
    # Scoring happens after the model has exited. The test file is never placed
    # inside the agent workspace.
    if status == "finished":
        try:
            checked = subprocess.run(
                [sys.executable, str(GRADER), str(workspace)],
                text=True, capture_output=True, timeout=30,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
            score = json.loads(checked.stdout.strip().splitlines()[-1])
            if checked.returncode not in (0, 1):
                status = "grader_error"
        except (OSError, ValueError, IndexError, subprocess.TimeoutExpired) as exc:
            score = {"passed": 0, "total": 9, "success": False, "error": str(exc)}
            status = "grader_error"
    else:
        score = {"passed": 0, "total": 9, "success": False}

    row = {
        "variant": variant,
        "run": run,
        "model": model,
        "skills_installed": installed,
        "status": status,
        "codex_exit_code": codex_rc,
        "seconds": seconds,
        "tokens_reported": codex_tokens(events_path),
        "skills_opened": skills_opened(events_path),
        "grade": score,
        "workspace": str(workspace),
        "events": str(events_path),
        "stderr": str(errors_path),
    }
    return row


async def main_async(args: argparse.Namespace) -> int:
    if not shutil.which(args.codex):
        raise SystemExit(f"Codex CLI not found: {args.codex}; install/authenticate it first")
    cstack = args.cstack.resolve()
    if not (cstack / "skills" / "default-mode" / "SKILL.md").is_file():
        raise SystemExit("Pass a checked-out cstack repo using --cstack")
    if not TASK.is_file() or not GRADER.is_file():
        raise SystemExit("Benchmark TASK.md/grade.py are missing")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    print(f"Benchmark: {args.runs} paired trials, model={args.model}, output={output}", flush=True)
    print("WARNING: Confirm no global cstack skills/AGENTS.md are loaded for the baseline.", flush=True)

    rows = []
    for run in range(1, args.runs + 1):
        # Two independent agent processes, run concurrently. No workspace is shared.
        pair = await asyncio.gather(*[
            run_trial(
                model=args.model, variant=variant, run=run,
                codex_bin=args.codex, cstack=cstack, out=output,
                timeout=args.timeout,
            )
            for variant in ("baseline", "skills")
        ])
        rows.extend(pair)
        for row in pair:
            print(f"{row['variant']} run={run}: "
                  f"{row['grade']['passed']}/{row['grade']['total']} "
                  f"status={row['status']} seconds={row['seconds']}", flush=True)
        (output / "results.json").write_text(
            json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    deltas = paired_deltas(rows, args.runs)
    opened = sum(1 for x in rows if x["variant"] == "skills" and x["skills_opened"])
    print(f"paired delta (skills - baseline, finished pairs only): {deltas}", flush=True)
    print(f"skills runs that opened at least one SKILL.md: {opened}/{args.runs}", flush=True)

    for variant in ("baseline", "skills"):
        values = [x for x in rows if x["variant"] == variant]
        mean_passed = sum(x["grade"]["passed"] for x in values) / len(values)
        mean_seconds = sum(x["seconds"] for x in values) / len(values)
        tokens = [x["tokens_reported"] for x in values if x["tokens_reported"] is not None]
        print(f"{variant}: average passed={mean_passed:.2f}/9, "
              f"mean_seconds={mean_seconds:.1f}, "
              f"reported_tokens_mean={sum(tokens)/len(tokens):.1f}" if tokens
              else f"{variant}: average passed={mean_passed:.2f}/9, "
                   f"mean_seconds={mean_seconds:.1f}, token usage unavailable")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cstack", type=Path, default=ROOT)
    parser.add_argument("--model", required=True, help="Use the same exact model for both agents")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=900, help="Per-agent deadline in seconds")
    parser.add_argument("--output", type=Path, required=True, help="New, nonexistent output directory")
    parser.add_argument("--codex", default="codex")
    args = parser.parse_args()
    if args.runs < 1 or args.timeout < 1:
        parser.error("runs and timeout must be positive")
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    raise SystemExit(main())
