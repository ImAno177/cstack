# Subagents

How cstack skills delegate. A skill that says "spawn", "fan out", a "worker", "runner", "judge", or "reviewer" means a subagent started through the host's delegation tool. Read this file once per session before the first spawn.

## Contents

- Spawning
- Models and diversity
- Read-only and isolated workers
- Briefs and results
- Transcripts
- When the host has no subagents

## Spawning

| Need | Claude Code | Other hosts |
| --- | --- | --- |
| Start a worker | `Agent` tool | The host's subagent or task tool |
| Parallel workers | Several `Agent` calls in one message; they run in the background and notify you when done | Start them together if the host allows it; otherwise run them one after another and say so |
| A worker that writes files | `subagent_type: "general-purpose"` with `isolation: "worktree"` and the branch or commit to check out | A separate git worktree or branch per worker |
| A worker that needs MCP tools | `general-purpose`; it keeps the session's MCP servers | Confirm the worker type keeps MCP access before relying on it |
| Resume a finished worker | Start a new one and paste the earlier result into its brief | Same |

Never ask one worker to own two MCP servers, two slices, or two candidates. Use bounded retries and no nested fan-out unless the skill asks for it.

## Models and diversity

Some skills ask for different models, such as runners from more than one model family, or a judge from a family other than the parent's. Diversity catches blind spots, but only real diversity counts.

- On Claude Code, `Agent` takes `model` (`opus`, `sonnet`, `haiku`, or `fable`) and `effort`. Use the strongest model for judgment, synthesis, and prose, and a faster one for broad mechanical work. Omit `model` to run on the session model.
- A Claude Code session has only Claude models. When a skill asks for another family, use a different Claude model or a fresh context on the same model, and say in the reply that cross-family diversity was not available.
- On a host that offers several families, pick across them as the skill asks. When the host rejects a model, use its default and say so.
- A user rule that names models per role overrides these defaults.

## Read-only and isolated workers

- A read-only worker gets a brief that says "do not edit files". On Claude Code use `subagent_type: "Explore"` when it needs no MCP tools, and check `git status` after it returns either way.
- A worker that writes gets its own worktree, branch, or scratch directory, per `principle-separate-before-serializing-shared-state`. Name the exact SHA it starts from.
- Copy uncommitted changes the worker must see into its worktree; a fresh worktree does not contain them.

## Briefs and results

Every brief stands alone, because the worker sees none of this conversation: the goal, the scope, the exact inputs (paths, SHAs, the user's question), how to verify, the result format, and what not to do. Verify every returned artifact yourself. A worker's summary, a clean exit, or a green check is evidence of execution, not proof of completion.

## Transcripts

Skills that audit a run (`reflect`, `show-me-your-work`) read the current session's transcript. Read only this workspace's history, never another project's.

- Claude Code: `~/.claude/projects/<slug>/<session>.jsonl`, where the slug is the workspace path with every character other than a letter or digit replaced by `-` (`/tmp/my_app` becomes `-tmp-my-app`). `<session>` is the current session id, which Claude Code substitutes for `${CLAUDE_SESSION_ID}` in skill text; prefer it to picking the newest `.jsonl`, which can belong to another session in the same workspace. `<session>/subagents/` holds subagent transcripts.
- Other hosts: the transcript path the system prompt or host docs name.
- When no transcript is reachable, write a tight digest of the session (requests, decisions, commands and results, corrections) and use that instead. Say so.

## When the host has no subagents

Run the roles yourself, one after another, in separate passes with a fresh re-read of the inputs each time. Keep each pass's output in its own scratch file so later passes cannot overwrite it. Say in the reply that the work ran without independent workers, because self-review is weaker than review by another agent.
