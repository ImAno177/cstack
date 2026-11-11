---
name: how
description: Explain how a codebase or subsystem works at the level of a senior engineer onboarding onto it - architecture, runtime flow, where things live, and gotchas. Use for "how does X work", code walkthroughs before changing something, and placement or ownership questions ("where should this live", "which package owns this", "is this the right layer"). Use why for motivation.
---

# How

Answer "how does X work?" with an architectural explanation: enough to build a working mental model, not so much that it reads like annotated source. Do not invent runtime behavior that the code or a command did not show.

## 1. Assess complexity

If the scope is ambiguous, state your interpretation and explore; the user can redirect.

- **Simple** (one module, a small utility, a narrow question such as "how does function X work"): no explorers. Explore and explain in one pass using [references/explainer-prompt.md](references/explainer-prompt.md) without the explorer-findings section, either yourself or in one read-only worker. Go to step 4.
- **Complex** (a subsystem spanning files or services, a cross-cutting feature, a full architectural overview): go to step 2.

When in doubt, take the simple path.

## 2. Explore (complex only)

Split the question into 2-4 angles, each a distinct slice of the subsystem. Start one read-only explorer per angle together, each with [references/explorer-prompt.md](references/explorer-prompt.md) and its angle filled in. Use a fast model for explorers and the strongest model for the explainer, per [subagents](../default-mode/references/subagents.md).

## 3. Synthesize (complex only)

Once every explorer returns, start one explainer with [references/explainer-prompt.md](references/explainer-prompt.md) and all explorer findings filled in.

## 4. Present

Present the explainer's output. Light edits for clarity or conversation context are fine; do not substantially rewrite it. Spot-check one or two claims against the code before presenting.

## Output format

The sections defined in [references/explainer-prompt.md](references/explainer-prompt.md), dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.
