---
name: tool-orchestration
description: Choose direct, parallel, programmatic, async, or offline batch tool execution from dependencies, side effects, and latency. Use when optimizing tool calls or designing an agent workflow; not for building the runtime loop (`agent-harness`) or for fanning out whole agents (`multi-agent-workflow`).
---

# Tool orchestration

Choose an execution mode from the task graph, not from a generic speed rule.

## Select a mode

- **Direct:** one result is needed, the next decision depends on it, or the call needs approval, citations, or a native artifact.
- **Parallel:** independent read-only work shares a stable snapshot, or isolated idempotent resources have separate ownership.
- **Programmatic:** a bounded loop, join, filter, deduplication, ranking, or validation can reduce many tool results to one structured result.
- **Async:** a slow external operation can run while the agent does independent work. Correlate the result with its call or job ID.
- **Offline batch:** requests are independent, non-interactive, and can tolerate delayed completion and per-request reconciliation.

## Guard the graph

1. Write the dependency graph and mark serial barriers before calling tools.
2. Batch only nodes without data or mutable-state dependencies.
3. Bound concurrency using the host and tool rate limits, memory, output budget, and cancellation support.
4. Keep writes, deletes, migrations, approvals, and final validation serial unless the tool contract proves safe isolation.
5. Reduce intermediate results before returning them, but preserve the evidence needed to audit the decision.
6. Treat missing, timed-out, cancelled, or partial results as failed branches. Never fill them with guesses.

## Host-specific contracts

- On the OpenAI Responses API, use strict schemas for parallel function calls where supported. Set `parallel_tool_calls` to `false` for ordering, shared state, or a single-call invariant. Keep hosted built-in tools out of a parallel function-call batch unless the host documents support.
- For async function or custom tools, bind a unique task handle to the original call ID and return the result on that original call. Keep async off hosted built-in and programmatic tools, and keep async tools out of parallel tool calls in multi-agent mode unless the host explicitly supports that combination.
- For an offline Batch API, give every request a unique identifier, reconcile each result independently, and treat the job as delayed work. Keep interactive decisions and side effects that need immediate authorization out of it.
- On other hosts, detect the supported capability and result contract before using a mode. Take OpenAI-specific flags and lifecycle semantics only from OpenAI hosts, never from a generic tool name.

## Measure the choice

Run the protocol in `agent-evaluation`: compare sequential direct calls with the selected mode on representative whole-repository tasks, with model, prompt, tools, rate limits, retry policy, and task set frozen. Measure correctness, evidence coverage, turns, calls, critical-path latency, queue and tool wait, tokens, cost, retries, partial failures, and cleanup. Keep the faster mode only when the quality bar holds within budget.

Keep semantic judgment, approval, and final validation visible to the main agent.

## Not for

- A single dependent call chain, where direct calls are already the answer.

## Done when

- The dependency graph is written, each node has a mode, and every serial barrier is named.
- Every call has a recorded status (ok, failed, timed out, cancelled, partial) and no missing result is filled by a guess.
- Changing the graph, concurrency, or tool set invalidates earlier measurements; remeasure.

## If it fails

- Find the failed node, its resource overlap or rate limit, and the host capability it assumed.
- Cut concurrency or move the node to a serial barrier before retrying; keep the quality bar fixed.
- Fall back to direct sequential calls when two adjustments still fail.
