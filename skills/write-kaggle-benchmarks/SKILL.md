---
name: write-kaggle-benchmarks
description: Write, push, run, publish, and manage Kaggle Benchmark tasks using the kaggle CLI and the kaggle-benchmarks Python
  SDK. Use when the user wants to create or push a benchmark task (optionally with attached Kaggle datasets), run benchmarks
  against LLM models, check task/run status, stream or fetch execution logs, download results and source notebooks, publish
  a task to make it public, or troubleshoot benchmark workflows.
---

# write-kaggle-benchmarks

Read [the full guide](references/full-guide.md) before the first command; it holds the flags, pacing rules, and gotchas.

## Readiness check

Check `kaggle --version` and `python --version`. `kaggle b init -y` writes `.env` (with a short-lived `MODEL_PROXY_*` key) and files into the folder: run it only after the user approves that step, then `python task.py` and `ls -1 *.run.json` before any push. Requires Python 3.11+, `kaggle`, and `kaggle-benchmarks` (`pip install kaggle kaggle-benchmarks`).

## Order

1. Write `task.py`: `# %%` cells, an `@kbench.task(...)` function, and a `.run(kbench.llm)` call (without it the push succeeds but the task silently does nothing).
2. Validate: `python task.py` exits 0 and `*.run.json` appears.
3. `kaggle b t push <slug> -f task.py --wait`, then `kaggle b t run <slug> -m <model> --wait`, then `kaggle b t status <slug>`.
4. `kaggle b t download <slug> -o ./results`; use `kaggle b t log <slug> -m <model>` for errored runs.

Run one step at a time: show its output and wait for the user's go-ahead before the next step, including `init`, as the guide's Pacing section requires. Publish with `kaggle b t publish <slug>` only on the user's request.

## Not for

- Creating or managing benchmark collections (the CLI handles tasks only) or deleting tasks (`delete` is unsupported server-side).

## Done when

- `kaggle b t status <slug>` shows every requested model run completed, and `<output>/<slug>/<version>/<model>/<run_id>/` exists for downloaded runs.

## If it fails

- Auth error: rerun `kaggle b auth -y`, then retry once.
- Errored run: read `kaggle b t log`, fix `task.py`, rerun the local validation, and repush before rerunning. Stop and report after two failures with the same error.

