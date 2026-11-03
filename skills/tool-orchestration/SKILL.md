---
name: tool-orchestration
description: Choose direct, parallel, programmatic, async, or offline batch tool execution from dependencies, side effects, and latency. Use when optimizing tool calls or designing an agent workflow.
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

- On the OpenAI Responses API, use strict schemas for parallel function calls when supported. Set `parallel_tool_calls` to `false` when ordering, shared state, or a single-call invariant matters. Do not assume hosted built-in tools can join a parallel function-call batch.
- For async function or custom tools, bind a unique task handle to the original call ID and return the result on that original call. Do not use async for hosted built-in or programmatic tools, and do not combine async tools with parallel tool calls in multi-agent mode unless the host explicitly supports that combination.
- For an offline Batch API, give every request a unique identifier, reconcile each result independently, and treat the job as delayed work. Do not use it for interactive decisions or side effects that need immediate authorization.
- On other hosts, detect the supported capability and result contract before using these modes. Never infer OpenAI-specific flags or lifecycle semantics from a generic tool name.

## Measure the choice

Compare sequential direct calls with the selected mode on representative whole-repository tasks. Freeze the model, prompt, tools, rate limits, retry policy, and task set. Measure correctness, evidence coverage, turns, calls, critical-path latency, queue and tool wait, tokens, cost, retries, partial failures, and cleanup. Keep the faster mode only if the quality bar holds within budget.

Do not assume the host supports every mode. Keep semantic judgment, approval, and final validation visible to the main agent.
