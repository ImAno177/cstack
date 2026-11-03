---
name: agent-context
description: Keep long-running agent work coherent with bounded phases, capped outputs, checkpoints, compact handoffs, and loop detection. Use for large repositories, many tool calls, compaction, repeated reads, or delegated work; not for short tasks.
---

# Agent context

Protect the context budget while preserving the state needed to continue correctly.

- Define the current phase, scope, done condition, and next checkpoint before broad exploration.
- Cap unknown or potentially large command output before reading it. Inspect narrow files and ranges, then widen only when evidence requires it.
- Keep a compact state summary containing decisions, constraints, evidence, changed paths, blockers, and the next action. Reuse an existing task record for long work; do not create a one-off repository file for a short task.
- Put the goal, invariants, done predicate, and next action at the front of the state capsule. Keep detailed evidence as source pointers rather than pasting long transcripts, and retrieve only the task-family slices needed for the next decision.
- After each meaningful milestone, checkpoint what is verified and what remains. On compaction or handoff, restore from the checkpoint and authoritative files instead of rereading the whole repository.
- Detect loops: repeated reads, retries, plans, or corrections without new evidence. Stop and diagnose the cause before spending another context window.
- Send delegated agents only the context they need and request a compact result with evidence, not a raw transcript.
