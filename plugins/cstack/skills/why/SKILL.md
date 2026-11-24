---
name: why
description: Investigate why code or a design has its current shape - design rationale, tradeoffs, regressions, postmortems, or data-backed thresholds - by querying every available evidence source (git history and PRs, issue tracker, docs, chat, observability, error tracking, analytics) in parallel and returning a cited read that separates facts from inference. Use for "why does X work this way" or "why did we pick Y". Not for what code does at runtime (use `how`) or for what a change would break (use `blast-radius`).
---

# Why

Investigate the motivation and intent behind code. `how` answers what the code does; `why` answers which forces gave it its shape. Read [subagents](../default-mode/references/subagents.md) before the first spawn. Investigators need MCP access, so use a worker type that keeps the session's MCP tools, and tell them not to write anything.

## Operating posture

Be a careful, precise investigator. Be honest about what you know versus what you infer. Read [references/epistemics.md](references/epistemics.md) for the confidence framework and phrasing; the synthesizer must follow it. Never claim an intent the evidence does not support.

## Step 1. Understand the target and the question

The target is usually code, a pattern, a feature, or a named decision. The question is usually a rationale, a tradeoff, a motivating edge case, an external constraint, dead code, or a history sweep. Make your best guess from the conversation (open files, recent edits, what was just discussed) when the target is vague, state it briefly so the user can redirect, and proceed.

## Step 2. Establish the code anchor

Before spawning anything, build the seed context: file paths and line ranges, key symbols, recent commits touching the target, PR numbers from merge subjects (`(#1234)`), and linked ticket IDs. Use `git blame -L <start>,<end> <file>`, `git log --follow -p -- <file>`, `git log --oneline -20 -- <file>`, and `git log -1 --format=%B <commit>`. Pull PR bodies and discussion for substantive commits: `gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews`. The anchor goes to every investigator and to the synthesizer.

## Step 3. Spawn parallel investigators

Default to the full parallel investigation. The goal is a complete coverage map; document a null result rather than skipping the search.

**Discovery.** List the MCP tools available in this session and map each server to one evidence category:

1. Source control history (always available through `git` and `gh`)
2. Issue or ticket tracker (Linear, Jira, GitHub Issues, Shortcut)
3. Long-form documents (Notion, Confluence, Google Docs)
4. Real-time team chat (Slack, Discord, Teams)
5. Infrastructure observability (Datadog, Grafana, Honeycomb)
6. Error or exception tracking (Sentry, Rollbar, Bugsnag)
7. Product analytics warehouse (BigQuery, Snowflake, Databricks)

Classify by server name, instructions, and tool names. Use a two-category server's primary evidence and note the ambiguity in the coverage map.

Start one investigator per category that has a source, all together, each owning exactly one tool or MCP server. Each investigator's prompt is [references/investigator-prompt.md](references/investigator-prompt.md) filled in, plus the category playbook from `references/sources/` adapted from [references/source-playbook.md](references/source-playbook.md), plus `references/sources/incident-postmortem.md` when the target looks defensive (null checks, retries, timeouts, rate limits, feature flags, OOM handlers), plus the anchor and the user's question. A fast model suits investigators.

What each category is best at surfacing: source control, implementation-time rationale from review; tickets, the product or business forcing function; docs, design rationale written before the code; chat, deliberation that never reached a doc; observability, the runtime reality behind timeouts, retries, and limits; error tracking, the exceptions that motivated defensive code; analytics, the data behind flags, experiments, and "where did this number come from".

**When to skip a category**, only with a written reason that goes in Sources Consulted: no source is available for it ("Real-time chat skipped. No matching MCP available, so the conversational record was not searchable."), or the source is provably irrelevant ("Error tracking skipped. Target is a build-time script with no runtime path."). Answer inline, and say so, only for a single-commit target whose PR description already holds the complete answer.

## Step 4. Synthesize

Start one synthesizer on the strongest available model with the investigator findings (including nulls and justified skips), the code anchor, the user's question, [references/epistemics.md](references/epistemics.md), and [references/synthesizer-prompt.md](references/synthesizer-prompt.md).

## Step 5. Present

Present the synthesizer's output. Light edits for clarity are fine; do not rewrite the confidence language.

## Output format

The structure in [references/synthesizer-prompt.md](references/synthesizer-prompt.md): The Question, The Code in Question, What We Found, What We Can Reasonably Infer, Competing Hypotheses, What We Don't Know, Sources Consulted, Confidence Summary. Keep Sources Consulted as one line per category, including empty and skipped ones with the reason.

End with a Preserve / Change / Avoid / Risk constraint set for planning the change when the question precedes a change to this code.

## Common failure modes

- **Recency bias**: treating the latest commit as authoritative. The current shape is often an accretion of earlier decisions; trace back.
- **Single-source answers**: stopping at the first plausible PR when chat or tickets hold the real forcing function.
- **Upgrading inference to fact**: a plausible motive is a hypothesis until a source states it.

## Done when

- The output has all eight sections of the synthesizer format, with one Sources Consulted line per category (searched, null, or skipped with the reason).
- Every claim carries a source (commit SHA, PR number, ticket, or link) and the confidence wording from `references/epistemics.md`; no inference is stated as fact; no file was edited (`git status` clean).

## If it fails

- A source errors or returns nothing: record it as null or skipped with the error, and continue with the other categories; do not fill the gap from memory.
- An investigator returns no evidence for its brief: rerun it once with a narrower anchor (exact path, PR numbers, date range). After the second null, report the gap under What We Don't Know and stop searching that source.
