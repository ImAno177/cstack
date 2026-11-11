---
name: agent-context
description: Keep long-running agent work coherent with bounded phases, capped outputs, checkpoints, compact handoffs, and loop detection. Use for large repositories, many tool calls, compaction, repeated reads, or delegated work. Not for short tasks that fit in one pass.
---

# Agent context

Protect the context budget while preserving the state needed to continue correctly.

- Define the current phase, scope, done condition, and next checkpoint before broad exploration.
- Cap unknown or potentially large command output before reading it, for example `| head -n 80`, `wc -l` first, or `rg -l` before `rg -n`. Read narrow files and line ranges, then widen only when evidence requires it.
- Keep a compact state summary with goal, invariants, done predicate, next action, then decisions, constraints, changed paths, and blockers. Reuse the existing task record for long work; create no repository file for a short task.
- Keep evidence as source pointers (`path:line`, command, commit), not pasted transcripts. Retrieve only the slices the next decision needs.
- Checkpoint what is verified and what remains after each milestone. On compaction or handoff, restore from the checkpoint and authoritative files; do not reread the whole repository.
- Stop and diagnose the cause before another pass whenever reads, retries, plans, or corrections repeat without new evidence.
- Send delegated agents only the context they need, and ask for a compact result with evidence, not a raw transcript.

## Not for

- Tasks that fit in one short pass with a few tool calls.

## Done when

- The state summary alone lets a fresh agent name the goal, the verified facts, and the next action.
- No large output was read uncapped, and no read or retry repeated without new evidence.
