---
name: reflect
description: "Mine a completed or failed agent episode for durable learnings with three parallel reviewers (judgment, tooling, divergent) and a synthesizer, then route each accepted learning to a concrete edit on an existing skill, with rejected and backlog items listed separately. Use when the user says reflect, or after a long task whose recipe should be captured. To measure and promote learnings across many episodes use continual-learning."
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits. Skip when the conversation is trivial, off-topic, or already covered by a skill that was followed correctly. One-offs and private preferences are not global rules. Read [subagents](../default-mode/references/subagents.md) before the first spawn.

## 1. Locate the active transcript

Find this conversation's transcript per [transcripts](../default-mode/references/subagents.md#transcripts); on Claude Code its file is `${CLAUDE_SESSION_ID}.jsonl`. Read only this workspace's history. When several candidates exist, take the one whose first user message matches this conversation's opening prompt. If none is reachable, pass a tight digest of the session instead, and say so.

## 2. Spawn three reviewers in parallel

Start three reviewers together. They need MCP access to look up the tickets, threads, and traces the transcript references, so use a worker type that keeps the session's MCP tools, and tell them not to write anything.

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

For each Accepted edit that changes behavior, name how you will know it helped: replay the triggering task, a representative prior task, and one unrelated protected task, with the evaluator outside the learner's write scope. Use `continual-learning` when the change is meant to persist across many episodes and needs retention measured.

## 6. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect every future agent; do not auto-apply. List Backlog items for the user's tracker without waiting.

Never edit an installed plugin cache (such as `~/.claude/plugins/` or another host's plugin directory). Edit the skill's source repository, or a project or user skill copy the user approves.

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
