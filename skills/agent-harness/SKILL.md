---
name: agent-harness
description: "Design, debug, or evaluate the runtime around a model-driven agent: loop, model adapter, tools, context, permissions, orchestration, extensibility, and verification. Use for Codex, Claude Code, DSH, Pi, Prime Agent, local-model integrations, or coding-agent harnesses; not for ordinary application code."
---

# Agent harness

Turn a model into a bounded, inspectable agent. Read [the harness matrix](references/harness-matrix.md) before choosing an architecture, [the LFM3/Pi notes](references/lfm3-pi.md) for that integration, and [the incident guards](references/incident-guards.md) before proposing a new hook, evaluator, batch path, or delegation policy.

## Not for

- Ordinary application code with no model-driven loop.
- Measuring agents across tasks; use `agent-evaluation`. Choosing parallel or async tool calls; use `tool-orchestration`.

## Define the boundary

Write the smallest user-visible outcome and the actual artifact or side effect that proves it. Decide whether the task needs a deterministic workflow or a model-directed loop. Start with one agent; delegate only for independent context isolation that beats serial work.

Before coding, record one decision for each subsystem in the matrix:

- loop and stop states;
- model protocol and normalized events;
- tools, argument contracts, output limits, and idempotency;
- context discovery, memory, compaction, and replay;
- permissions, approvals, sandbox, and failure policy;
- subagent ownership, isolation, communication, and shared-write rules;
- skills, hooks, extensions, plugins, and external integration boundaries.

## Implement the smallest reliable loop

Use this lifecycle:

1. Load scoped instructions and task state deterministically.
2. Send the model a normalized request and only the tools it can use now.
3. Validate every structured response at the boundary.
4. Apply policy before execution; never let a prompt or model output widen permissions.
5. Execute actions with bounded output, timeout, cancellation, and an operation identity for writes.
6. Append the assistant call, tool result, policy decision, and artifact receipt to the session trail.
7. Continue, recover, interrupt, compact, or stop from explicit state. Do not infer completion from text alone.

Start serial. Batch only calls that are all read-only or have disjoint declared resources, with a defined result order. Make steering interrupt the current run and make follow-up wait until current tool work completes.

## Context and memory

Discover hierarchical instruction files and neighboring conventions from the current path. Load metadata eagerly and large skills, tools, and references just in time. Use deterministic code search before adding vector retrieval. Compact before the effective context limit, preserve the system contract and recent task tail, merge prior summaries, and keep a replayable boundary or checkpoint.

Treat durable memory as a reviewed artifact. Let a refinement process propose a patch, skill, or memory entry, and record source episode, scope, evidence, privacy class, rollback, and expiry. Never let it silently rewrite the base prompt or shared skills.

## Tools, hooks, and extensions

- Keep tool schemas small, typed, discoverable, and honest about side effects. Use exact unique matching for edits; never make line numbers the write contract.
- Use a skill for procedures, a hook for deterministic lifecycle behavior, an extension for runtime events/tools/UI, a plugin for a replaceable service, and MCP or another adapter for an external process.
- Hooks must declare whether they observe, warn, block, or inject a continuation. Keep stdout/protocol output machine-readable and diagnostics separate. Fail open only where host policy explicitly allows it.
- In a Node/Pi project, use ESM `.mjs` or TypeScript with package scripts; add a `.ps1` helper only where the repository owns a Windows-only boundary. Keep comments to non-obvious contracts, generated sections, license facts, public APIs, or tool requirements.

## Multi-agent and long-running work

Give each worker an isolated path or session, a bounded budget, an explicit tool allowlist, and a typed evidence contract. Keep shared writes with one owner. Persist resumable session state, goals, heartbeats, and stop reasons, but do not call daemon persistence or worker isolation a security sandbox.

## Evaluation gate

Run production-shaped trials in clean environments. Include no-tool answers, valid and malformed calls, deferred discovery, duplicate-write prevention, timeout and tool failure, steering, follow-up, compaction, partial completion, and false completion claims. Grade outcome and trajectory separately: artifact state, tool choice, arguments, policy decisions, errors, turns, latency, tokens, retries, cleanup, and stop reason. Classify model, harness, tool, environment, and evaluator failures separately.

## Operational guardrails

- Tie each new hook, evaluator, or automation to a reproduced incident, a measurable success predicate, a cost budget, and a retirement condition.
- Make verifiers non-vacuous: record the expected subject count and matched-evidence count; zero matches are `unknown`, never a passing result.
- Bound delegated work by model, depth, concurrency, time, tokens, and cleanup receipt. A worker report is not evidence that its side effects happened.
- Write a durable handoff before compaction or a phase boundary. Keep the system contract and tool catalog stable inside a phase; discover new tools at the next boundary.
- Measure activation and outcome before adding another skill or reference. Retire additions that add load without improving a representative task.

## Done when

- The real artifact or side effect is inspected, and the event trail shows the expected stop reason.
- The relevant failure is replayed and passes, with a control case; any later edit to loop, tools, or policy invalidates earlier replays.
- Temporary output is removed, and the report lists attempted, executed, verified, skipped, partial, and blocked work separately (see `agent-completion`).

## If it fails

- Classify the failure as model, harness, tool, environment, or evaluator from the trail before editing.
- Change the guard or contract at the boundary where it first became observable, then rerun the failing and control cases. Keep the success predicate fixed.
- Stop and report blocked when two distinct fixes fail to reproduce a pass.
