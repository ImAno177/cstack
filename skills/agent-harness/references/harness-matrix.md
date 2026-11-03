# Harness comparison and distilled rules

This matrix is a design reference, not a promise that every host exposes the same API. Verify the host version before implementing an adapter.

## Source systems

| Harness | What it makes explicit | What cstack should borrow | What cstack should not assume |
| --- | --- | --- | --- |
| Codex | Core loop, thread lifecycle, persistence, streaming events, sandbox and approval policy, skills and MCP under one policy surface | Treat a thread as durable state; expose typed lifecycle events; verify policy and artifact effects separately | A client protocol or OS sandbox exists on every host |
| Claude Code | Hooks at lifecycle boundaries, deferred tools, concurrency-safe tool batching, subagents with separate windows, compaction and path-aware activation | Keep hooks deterministic; default tool calls to serial; load context and tools just in time; isolate delegated work | A hook can see every file reference or can repair a tool after it already ran |
| DSH | Everything is a plugin; service registry and dependency injection; swappable context, tools, storage, loop and sandbox; visible service/tool/session writes | Give each capability one owned seam; make implementations replaceable; expose inspectable runtime events | Plugin APIs are stable; DSH is still a developer preview |
| Pi | Minimal terminal harness; skills, extensions, prompts and themes are separate resources; sessions are append-oriented and forkable | Keep the core loop small; put runtime behavior in extensions and procedural guidance in skills; preserve session lineage | Project instructions or extensions are a security sandbox |
| Prime Agent | Persistent REPL, programmatic context, recursive subagents, daemon sessions, goals, heartbeats, refinement and reusable skills | Make long-running state resumable; keep refinement evidence-backed and rollbackable; account for time, tokens and resources | Persistence, worker isolation or a daemon makes untrusted execution safe |

The source comparison is grounded in [Codex harness architecture](https://openai.com/index/unlocking-the-codex-harness/), [Claude Code hook semantics](https://code.claude.com/docs/en/hooks), [DSH](https://github.com/deepseek-ai/deepseek-harness), [Pi](https://github.com/badlogic/pi-mono), and [Prime Agent](https://github.com/PrimeIntellect-ai/prime-agent).

## Hook semantics that must not be blurred

Claude Code is a useful concrete example, not a cross-host contract. Its `PreToolUse` hook runs only after a tool call has been formed and before execution; a file mentioned directly in a prompt can bypass that hook. Its `PostToolUse` hook observes after the action and cannot block the write. Blocking, structured JSON output, timeout, and asynchronous delivery have different semantics. Therefore every cstack hook design must state its event coverage, point of no return, output protocol, timeout behavior, and fail-open or fail-closed rule instead of assuming that “a hook ran” means “the action was controlled.”

## The seven subsystem decisions

Before adding a feature, write one sentence for each subsystem:

1. **Loop.** What alternates model inference and actions, and which explicit states can stop, retry, interrupt, or recover?
2. **Model integration.** Which provider protocol, streaming events, structured output, tool-call identity, caching, and model-specific quirks are normalized?
3. **Tools and actions.** What can the model do, how are arguments validated, how are writes made idempotent, and how is output bounded?
4. **Context and memory.** What is loaded eagerly, what is discovered just in time, when does compaction happen, and what history remains replayable?
5. **Safety and permissions.** Which actions are allowed, asked, denied, or sandboxed in each mode, and where is the policy data stored?
6. **Orchestration.** Why is one agent insufficient, what state is isolated, how do workers return typed evidence, and who owns shared writes?
7. **Extensibility.** Is this behavior a skill, hook, extension, plugin, or external integration, and what is the version/provenance boundary?

## Rules distilled for implementation

- Start with a linear loop. Move turn limits, cost limits, compaction, read-only mode, and other orthogonal checks into middleware only when they are independently testable.
- Keep a typed append-only event or receipt trail. The final assistant message is a UI result, not proof of the filesystem or external side effect.
- Start with a small tool surface. Add tools only for a demonstrated failure mode. Above roughly fifteen tools, use deferred discovery rather than injecting every schema.
- Prefer exact unique-substring edits for a capable model and a controlled fallback for weaker models. Never use line numbers as the write contract.
- Discover hierarchical context deterministically. Use ripgrep, glob, symbol extraction, or filesystem traversal for code; require evidence before adding semantic retrieval.
- Compact below the effective context limit, preserve the system contract and a verbatim recent tail, and merge the previous summary instead of summarizing from scratch. Make compaction replayable or checkpointed.
- Separate plan, default, and automatic modes with policy data. A fast mode may reduce prompts or approvals, but it must not remove the minimum write and sandbox boundary.
- Keep subagents single-hop and in-process until a measured breadth-first task needs isolated parallel context. Never parallelize overlapping writes. Return artifacts and evidence, not prose-only claims.
- Use skills for procedures and domain guidance, hooks for deterministic lifecycle checks, extensions for runtime mechanics, plugins for replaceable services, and MCP or external adapters for remote systems.
- Put runtime checks and regression cases around failures: malformed arguments, duplicate writes, tool timeouts, interruption, compaction, stale context, missing tools, partial completion, and false completion claims.

These rules follow the cross-harness source study [Harness Engineering](https://arxiv.org/abs/2609.00006), but each recommendation remains a hypothesis until the target harness proves it on its own workload.
