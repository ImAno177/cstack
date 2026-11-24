# LFM3 and Pi integration notes

These notes describe a bounded integration strategy. They do not replace current provider or Pi documentation.

## Model constraints

The [LFM3-1.7B model card](https://huggingface.co/LiquidAI/LFM3-1.7B) describes a 1.73B text model with a 256K-token context window, structured tool calling, and deferred tool support. It also says the model is not recommended for agentic coding or complex multi-step reasoning. Treat that as a role constraint, not as a prompt problem to paper over.

Good initial roles:

- bounded tool worker with a small, stable tool set;
- router or classifier whose choice is checked by the harness;
- local summarizer or recovery assistant after the primary agent has produced evidence.

Do not make LFM3 the only judge of a code change or the sole planner for an unbounded repository task without a comparative evaluation.

## Tool-history contract

When using the Transformers or compatible chat-template path:

1. Pass the tool schemas on each request.
2. Parse the generated tool call into a mapping before execution.
3. Append the assistant tool call and the tool result with the same call identity.
4. Preserve the current tool-use turn's assistant content and reasoning when the provider requires it.
5. For deferred tools, keep the full tool list and return the provider's tool-reference message before invoking the selected tool.

The adapter owns provider-specific XML or chat-template details. The loop consumes a normalized internal event such as `tool_call`, `assistant_text`, `tool_result`, `error`, or `stop`.

## Pi boundary

Pi is an extensible terminal harness. Its documented resource split is useful here:

- skills hold on-demand procedural instructions;
- extensions hold runtime tools, commands, events, permission gates, and UI;
- prompt templates hold reusable prompts;
- packages bundle these resources for installation and update.

Keep deterministic lifecycle behavior in an extension or host hook. Do not ask a skill to simulate cancellation, enforce a turn limit, or verify a filesystem side effect.

## Minimum evaluation matrix

Run the same cases through the production-shaped Pi loop and a small reference loop:

- answer without a tool;
- choose one tool with valid arguments;
- reject or repair malformed arguments;
- call two independent tools and reconcile both results;
- discover a deferred tool;
- receive a steering interruption while a tool is running;
- resume with a follow-up after completion;
- recover from a tool error without duplicating a write;
- stop only after the expected artifact or state exists.

Record final outcome, tool-call success rate, invalid-call rate, turns, latency, token use, retries, and cleanup. A final text claim without the expected artifact is a failure.
