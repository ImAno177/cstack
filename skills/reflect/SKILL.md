---
name: reflect
description: "Mine a completed or failed agent episode for durable learnings with three parallel reviewers (judgment, tooling, divergent) and a synthesizer, then route each accepted learning to a concrete edit on an existing skill, with rejected and backlog items listed separately. Use when the user says reflect, or after a long task whose recipe should be captured. Not for measuring or promoting learnings across many episodes; use `continual-learning`."
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits. Read [subagents](../default-mode/references/subagents.md) before the first spawn. This skill ends at approved edits for one episode; replay, retention measurement, and retirement belong to `continual-learning`.

## 1. Locate the active transcript

Find this conversation's transcript per [transcripts](../default-mode/references/subagents.md#transcripts); on Claude Code its file is `${CLAUDE_SESSION_ID}.jsonl`. Read only this workspace's history. Take the candidate whose first user message matches this conversation's opening prompt when several exist. Pass a tight digest of the session instead when none is reachable, and say so.

## 2. Spawn three reviewers in parallel

Start three reviewers together. Use a worker type that keeps the session's MCP tools so they can look up the tickets, threads, and traces the transcript references, and tell them not to write anything.

| Lens | Model | Prompt template |
|---|---|---|
| Judgment | strongest available | [references/judgment-reviewer.md](references/judgment-reviewer.md) |
| Tooling | a fast model, another family when available | [references/tooling-reviewer.md](references/tooling-reviewer.md) |
| Divergent | strongest available | [references/divergent-reviewer.md](references/divergent-reviewer.md) |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in their final message.

## 3. Synthesize

Start one synthesizer on the strongest available model with [references/synthesizer.md](references/synthesizer.md) verbatim and each reviewer's full output inlined where marked. It spot-verifies citations and returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, validator, or runtime check would enforce more reliably to Backlog (`principle-encode-lessons-in-structure`).

## 5. Check before applying

For each Accepted edit that changes behavior, name how you will know it helped: replay the triggering task, a representative prior task, and one unrelated protected task, with the evaluator outside the learner's write scope. Hand the edit to `continual-learning` when it must persist across many episodes and needs retention measured.

## 6. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit; skill changes affect every future agent. The user picks the subset and may redirect routings. List Backlog items for the user's tracker without waiting.

Edit the skill's source repository, or a project or user skill copy the user approves; leave installed plugin caches (such as `~/.claude/plugins/`) untouched.

Follow each approved row's routing exactly:

- Trivial existing-skill edit (one bullet, a tightened sentence, a stale fact): apply it directly.
- Substantive existing-skill edit (a new section or pattern table, more than about 10 lines): follow `default-mode`'s `authoring-a-skill.md` playbook, or the host's skill-creator when installed.
- `tune description: <skill path>`: optimize the description so the skill triggers when it should, with the same playbook or skill-creator.
- `new skill via create-skill: <kebab-name>`: create it through that playbook or skill-creator; do not invent the shape ad hoc.

Run the repository's skill validators on every touched skill before declaring done.

## 7. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`, what changed, one line each.
- New skills created: `<skill path>`, one line each (rare).
- Backlog: `<item>`, one line each.
- Dropped: one line per rejected finding and the synthesizer's reason.

## Not for

- Trivial or off-topic conversations, or ones where a skill was followed correctly.
- One-offs and private preferences; they are not global rules.

## Done when

- Every applied edit was approved by the user, and the repository's skill validators pass on each touched skill.
- Editing a skill after validation invalidates the run; revalidate before the summary.

## If it fails

- No transcript or digest: stop and report instead of reviewing from memory.
- A reviewer returns nothing or uncited findings: rerun that reviewer once with the transcript path fixed; synthesize with the remaining two and say so.
- A validator fails: fix the edit, never loosen the validator.

## Example summary

```
- Edits applied: `skills/<skill>/SKILL.md`, added the exact validator command to Done when.
- New skills created: none.
- Backlog: `<lint for stale links>`, a validator can enforce this.
- Dropped: `<one-off path fix>`, durability (breaks when the path moves).
```
