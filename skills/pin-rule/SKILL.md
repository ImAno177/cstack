---
name: pin-rule
description: Pin a rule the user states in chat so it survives context compaction and long sessions. Use when the user says to always or never do something for this project or for all work, or asks to remember a rule. Not for facts or preferences the user did not state as a rule; those belong in memory.
---

# Pin a rule

A rule that lives only in the conversation can be summarized away when the context is compacted, and prohibitions fade as a session grows. cstack's `standing-rules` hook re-injects pinned rules at session start, after every compaction, into each subagent, and every few prompts.

## Steps

1. Restate the rule as one line the agent can act on, with its scope and reason: what to do, where it applies, and why. Prefer the positive form ("ask before deleting files under `data/`") over a bare prohibition, and keep any exception the user gave.
2. Choose the file:
   - this project only: `.claude/pinned-rules.md` at the project root;
   - all projects: `~/.claude/pinned-rules.md`.
3. Read the file if it exists. Do not add a duplicate; replace an older rule the new one supersedes.
4. Append the rule as a single `- ` line. Keep the file under 2,000 characters, because the hook truncates beyond that; if it would grow past that, ask the user which rule to drop.
5. Tell the user the exact line you pinned and the file path.

## Done when

The rule is one line in the chosen file, the file is under 2,000 characters, and the reply quotes the line and path.

## If it fails

If the file cannot be written, give the user the line and the path so they can add it themselves.
