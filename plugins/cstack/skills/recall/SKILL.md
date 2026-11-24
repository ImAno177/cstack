---
name: recall
description: Reconstruct recent work on a named project or topic from earlier agent sessions and shared repository records, including prior decisions, PRs, reversions, and next steps. Use for "catch me up on X", "what have I been working on", or "where did I leave off" across sessions. For only the current chat use ketchup; for resuming one exact branch or session use the session-pickup playbook.
---

# Recall

Reconstruct the previous state; do not start implementing it. Limit retrieval to evidence that changes the resume decision.

## Scope

1. Pin the workspace, topic, and time range. Default "recent" to the last seven days; if the user says "all", do not silently truncate it. Do not read unrelated workspaces or accounts without scope and permission.
2. Distinguish this from ketchup (current conversation) and default-mode's session-pickup playbook (one known branch, transcript, or checkpoint). A supplied complete checkpoint is the starting point, not a reason to re-mine everything.
3. Inspect only transcript locations documented by the current host, scoped to this workspace. Filter by real modification time, then topic, then relevant message ranges. Never guess a host-specific path or treat a missing transcript as evidence nothing happened.
4. When multiple relevant sessions exist, delegate bounded, read-only slices if the host supports agents; otherwise inspect sequentially. Keep raw transcripts out of the main context. Each slice returns goal, decisions, changed artifacts, open work, and a source pointer.
5. Reconcile the session history with the shared record: current branch and diff, commits, PRs, issues, recent regressions, and reverted fixes relevant to the named topic. The source code and issue history may have changed after the conversation. Treat inaccessible sources as gaps, not as clean reports.
6. Validate claimed merges, commits, and fixes against the live repository or their recorded evidence. Distinguish verified, reported, reverted, in progress, and unknown. Sanitize credentials and private conversations before quoting or sharing.
7. Stop once the next action is clear. Do not modify code, open a PR, or message others from a recall request.

## Handoff

- **Capsule:** at most five short findings on where the work stands.
- **Threads:** one line per active line of work, with its actual status and a PR, commit, branch, or transcript pointer.
- **Problems:** the most important unresolved symptoms, regressions, or disproved approaches.
- **Next move:** one concrete action a new agent can take without repeating completed work.
- **Gaps:** unavailable history or unverified claims.

For an actionable resume, hand the capsule to [session-pickup](../default-mode/playbooks/session-pickup.md). For preserving a new checkpoint, use `agent-context` from the cstack-harness plugin when it is installed.

## Not for

- Summarizing only this chat: use [ketchup](../ketchup/SKILL.md).
- Capturing lessons from a completed episode: use [reflect](../reflect/SKILL.md).
- A request to inspect code without prior-work history: use [how](../how/SKILL.md) or [why](../why/SKILL.md).

## Done when

Every claim about prior work links to an accessible record or is explicitly unverified, and the capsule names the actual next step.
