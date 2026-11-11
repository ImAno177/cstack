---
name: show-me-your-work
description: Keep a reviewable decision trail for long-running or unattended work - a TSV log with one row per decision (what, why, evidence, result) - then audit it against the transcript and have an independent reviewer flag what needs attention. Local by default; commit it when a reviewer needs the trail to trust the result. Use for autonomous or multi-phase runs, or work a human reviews after stepping away.
---

# Show me your work

Keep one canonical log.

## The format

A single TSV file, one row per decision. Cells stay single-line. Evidence is a pointer, not prose. Copy [references/decision-log-template.tsv](references/decision-log-template.tsv) (the header row) to start. Columns:

- **ts**: ISO 8601 timestamp.
- **phase**: the phase or workstream.
- **decision**: what was chosen or done, one line.
- **why**: the reason in plain words. If a principle drove it, say it plainly, not as a jargon tag.
- **evidence**: a link or path that proves it: commit SHA, PR number, `file:line`, or an artifact, trace, or screenshot path. Never a paragraph.
- **result**: the outcome or predicate state: `tests green`, `reverted`, `pixel-diff 0`, `INCONCLUSIVE`, `open`.

```
ts	phase	decision	why	evidence	result
2026-05-24T09:02:00Z	frame	counted the work first, about 100 components and roughly 75 hours	wanted to know the size before starting a long run	commit 3a9f1c2	found 5 things to sort out before starting
2026-05-24T09:40:00Z	harness	took screenshots of the old version before changing anything	so we can compare old against new and catch any visual change	scripts/snapshot.sh, baseline/	saved 120 reference screenshots
2026-05-24T12:30:00Z	widget	threw out a helper's work because its screenshots were blank	checked the real files instead of trusting its summary	worktree reset	reverted, tightened the instructions for next time
```

## Logging a row

Write each entry the way you would tell a teammate what you did: plain words, concrete actions (`unslop` applies to log text too).

Run `<skill-dir>/scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>`, where `<skill-dir>` is the directory containing this `SKILL.md` (on Claude Code, `${CLAUDE_SKILL_DIR}`). It stamps `ts`, writes the header on first use, strips stray tabs and newlines, and prefixes any cell starting with `=`, `+`, `-`, or `@` with a single quote so the log is safe to open in a spreadsheet. A bare `printf` append works too, but then handle those bytes yourself when cells come from generated or user-supplied text.

Log decision points and checkpoints, not every action: a fork chosen, a unit completed with its verification result, a pivot or revert and its trigger, a blocker surfaced, a gate fixed. For loop runs, one row per iteration.

A run is one agent conversation, including its later turns. A pickup, a replacement agent, or a new chat starts a new run. When a run adds to a log that already has rows, its first row has phase `start`, and so does its first row after another run's `start` row; so a returning run first reads the last rows to see whether another run wrote since. A `start` row names the `ts` range of the rows before it that this run did not write, and its evidence names this run. Use phase `start` for nothing else.

## Where it lives

By default the log is a working artifact: `decisions.tsv` in the work directory, or `.audit/<task-slug>.tsv` when several efforts run at once, kept out of git. Commit it only when the work is ambitious enough that a reviewer needs the trail to trust the result.

## Rules

- Append-only. A wrong call gets a new row that supersedes it. Never edit or delete history.
- Prefer evidence produced by committed scripts over one-off commands (`principle-encode-lessons-in-structure`).

## Audit the log against the transcript

Before handing back, check that the log told the truth. Read this run's transcript (see [transcripts](../default-mode/references/subagents.md#transcripts); never another project's history) and walk this run's rows against what happened:

- every row maps to a real decision or action;
- each row's evidence resolves and shows what the row claims;
- a fork, pivot, or abandoned approach that shaped the work but is not logged is a gap: add it.

Correct the log, not the story: never edit or remove a row, even an invented one. Add a row that supersedes it with what actually happened and a pointer that resolves.

## Independent review of the trail

Before handing back, start a reviewer that did not do the work, on a different model family when the host offers one ([models and diversity](../default-mode/references/subagents.md#models-and-diversity)). Self-review is not a substitute. It reads the trail and the transcript and flags what the user should look at; it does not redo the work:

- decisions logged with weak or missing evidence;
- verification skipped, or claimed without proof in the transcript;
- choices that look risky in hindsight (premature, scope-creeping, papering over a symptom);
- gaps the user would miss on a quick skim.

Every reply for a run that produced a trail ends with an **Attention** section: the reviewer's model on its own line (`reviewed by <model>`), then each flag pointing at specific rows or moments. "No flags" is a valid value; the model name is not optional.

## Reviewing the trail

Read top to bottom, follow the evidence pointers, spot-check. GitHub renders a committed TSV as a table; `column -s$'\t' -t decisions.tsv` renders it in a terminal.

## Composing this skill

Other skills route their audit trail here instead of inventing one. Reference it by name and let it own the format; do not restate the columns.
