---
name: how
description: Explain how a codebase or subsystem works at the level of a senior engineer onboarding onto it - architecture, runtime flow, where things live, and gotchas. Use for "how does X work", code walkthroughs before changing something, and placement or ownership questions ("where should this live", "which package owns this", "is this the right layer"). Not for motivation or history; use `why`.
---

# How

Answer "how does X work?" with an architectural explanation: enough to build a working mental model, not so much that it reads like annotated source. State only runtime behavior that the code or a command showed.

## 1. Assess complexity

State your interpretation when the scope is ambiguous, then explore; the user can redirect.

- **Simple** (one module, a small utility, a narrow question such as "how does function X work"): no explorers. Explore and explain in one pass using [references/explainer-prompt.md](references/explainer-prompt.md) without the explorer-findings section, either yourself or in one read-only worker. Go to step 4.
- **Complex** (a subsystem spanning files or services, a cross-cutting feature, a full architectural overview): go to step 2.

Take the simple path when unsure.

## 2. Explore (complex only)

Split the question into 2-4 angles, each a distinct slice of the subsystem. Start one read-only explorer per angle together, each with [references/explorer-prompt.md](references/explorer-prompt.md) and its angle filled in. Use a fast model for explorers and the strongest model for the explainer, per [subagents](../default-mode/references/subagents.md).

## 3. Synthesize (complex only)

Start one explainer once every explorer returns, with [references/explainer-prompt.md](references/explainer-prompt.md) and all explorer findings filled in.

## 4. Present

Spot-check one or two claims against the code (open the cited file and line), then present the explainer's output. Light edits for clarity or conversation context are fine; do not substantially rewrite it. Replace any claim the code contradicts.

## Output format

The sections defined in [references/explainer-prompt.md](references/explainer-prompt.md), dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.

## Done when

Every cited path exists, at least one claim was checked against the code, and each applicable section is present.

## If it fails

Re-read the cited code when a spot-check contradicts the explanation, correct the claim, and check two more. Resolve explorer contradictions from the code. Switch to the complex path when the answer needs files you have not traced.
