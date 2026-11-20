---
name: principle-guard-the-context-window
description: 'Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to
  subagents; keep summaries in the main thread, not raw payloads.'
disable-model-invocation: true
---

# Guard the Context Window

Treat context as a budget. Keep decisions, constraints, and pointers in the main thread, and keep bulk out of it.

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.
- **Measure before reading.** Check size first (`wc -l`, `rg -l`, `git diff --stat`), then read the range the next decision needs, not the whole file or log.
- **Route bulk to subagents.** Hand broad searches, long logs, and many-file reads to a worker, and ask it for a compact result with `path:line` pointers instead of raw output.
- **Keep pointers, not payloads.** Record a path, command, or commit that reproduces the evidence. Do not paste the evidence into the thread.
- **Stop repeated reads.** A second read of the same file with no new question means the state summary is missing something. Fix the summary.

For the full long-run procedure (checkpoints, handoffs, loop detection), use the `agent-context` skill.
