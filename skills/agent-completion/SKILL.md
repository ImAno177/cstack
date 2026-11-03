---
name: agent-completion
description: Establish whether an agent task actually completed after tool calls or side effects by separating attempted, executed, verified, partial, blocked, and failed states. Use when changing files, running commands, or handing off work; not for abstract explanations.
---

# Agent completion

Use an observable done condition and an authoritative state source before acting.

## Verify

- Track each important action as requested, attempted, executed, and verified. Do not collapse these states.
- Inspect the real artifact or external state after a side effect. A clean exit, tool acknowledgement, or generated message proves execution only.
- Use the smallest check that can disprove completion, and inspect the resulting paths, values, records, or user-visible effect.
- Treat timeout, interruption, partial output, missing artifact, and contradictory evidence as incomplete until resolved.

## Report

- Classify the outcome as verified, partial, blocked, or failed.
- State the changed paths or resources, the commands or tools actually run, the evidence observed, skipped checks, and remaining risk.
- Never claim a test, deployment, write, merge, upload, or cleanup succeeded without observing its result.
