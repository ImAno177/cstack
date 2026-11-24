---
name: scientific-visualization
description: 'Use whenever you make or fix figures for a paper, thesis, or report in Matplotlib, Seaborn, or Plotly: multi-panel layouts, error bars and uncertainty, missing data, colorblind-safe color and contrast, misleading axes, and journal export. Use it even if the user only says the plots look amateur.'
license: MIT
compatibility: Requires Python 3.11+ and uv for pinned examples. Bundled CLIs are network-free and load Matplotlib, Pillow,
  or pypdf only when needed. Plotly static export with Kaleido v1 requires a compatible Chrome/Chromium installation.
allowed-tools: Read Write Edit Bash Glob Grep
metadata:
  version: '1.4'
  last-reviewed: '2026-10-01'
  skill-author: K-Dense Inc.
---

# scientific-visualization

`<skill-dir>` is the directory containing this `SKILL.md` (on Claude Code, `${CLAUDE_SKILL_DIR}`); its scripts run from any working directory.

Read [the full guide](references/full-guide.md) before building or auditing any figure. It holds the guardrails, workflow, and script invocations. Read `references/publication_guidelines.md` for integrity checks, and `references/journal_requirements.md` only after the exact journal and submission phase are known.

## Not for

- Dashboards, business charts, or slide decks: this skill targets scientific figures.

## Done when

- The delivered figure file was opened and inspected at its final size, not only the plotting code.
- Source data paths, transformations, and uncertainty definition are recorded beside the figure.
- Publisher requirements are marked verified (with the live source) or pending; none are assumed.

## If it fails

A script check that fails (`<skill-dir>/scripts/palette_audit.py`, `image_metadata.py`, `export_plan.py`) means fix the figure or its export settings and rerun the same check. Do not relax a threshold or edit the data to pass. Report the check output and the blocker after two failed repairs.
