---
name: md-docs
class: workflow
description: >-
  Manages project documentation: CLAUDE.md, AGENTS.md, README.md, CONTRIBUTING.md, DOCS.md.
  Use when asked to update, create, or init these context files. Not for general
  markdown editing or sentence-level prose style; use `technical-writing`.
---

# Markdown Documentation

Manage project documentation by verifying against actual codebase state: analyze structure, files, and patterns before writing; never generate blind.

## Not for

- Writing or reviewing prose style, Diátaxis mode, or sentence rules; use `technical-writing`. This skill decides which file holds a fact and verifies it against the repo. Load both for a documentation task.
- Changelogs, release notes, and generic markdown editing.

## Working rules

- Read existing documentation and verify its claims against actual code and commands before editing.
- Preserve request authority, external-action boundaries, proof standards, and failure-attribution rules when condensing context.
- Do not create CONTRIBUTING.md or DOCS.md as a side effect; apply the specific workflow's creation limits.
- Keep cross-cutting conventions discoverable in the main context file and avoid duplicated volatile facts.
- Report actual edits and checks; do not claim snippets or external identifiers verified without checking them.

## Portability

AGENTS.md is the universal context file (works with Claude Code, Codex, Kilocode). Run `mv CLAUDE.md AGENTS.md` only inside the Initialize Context or Update Context Files workflows, only when CLAUDE.md exists without AGENTS.md, and only after the user confirms (use the host's question tool if it has one; otherwise numbered options in chat). Never migrate as a side effect of another task.

The CLAUDE.md symlink is optional compatibility, not a required step. Claude Code v2.1.277 and later reads AGENTS.md natively when no `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` exists in the working directory or above it; any of those three found there silently stops that loading, so flag it. For harnesses or sessions that read only CLAUDE.md, offer a CLAUDE.md containing `@AGENTS.md`; offer `ln -s AGENTS.md CLAUDE.md` only when no contributor uses Windows (a clone without `core.symlinks` gets a one-line text file); Edit/Write refuse to write through the link. Keep an existing symlink unless the user asks to remove it. Details and fixes: [init-agents.md](./references/init-agents.md), section "Claude Code compatibility".

When this skill references "context files", it means AGENTS.md (and CLAUDE.md if present, as a symlink or an `@AGENTS.md` import).


## Monorepos

Read [monorepo.md](./references/monorepo.md) before any `update-*`/`init-*` sweep of a multi-package repo (discovery commands, per-file scoping, context-loading rules). Enumerate targets. Stop and confirm before writing when the sweep would create or rewrite more than 3 files: list the planned targets first (same ask mechanism as in Portability above).


## Arguments

Treat these as user-request modifiers: apply when the request contains the flag or equivalent phrasing. All workflows support:

- `--dry-run`: preview changes as a diff, write nothing
- `--preserve`: keep existing structure, fix inaccuracies only
- `--minimal`: quick pass, high-level structure only
- `--thorough`: deep analysis of all files


## Backup Handling

Before overwriting, create a unique adjacent backup path with exclusive creation (for example, `mktemp FILE.backup.XXXXXX`). Copy the source bytes into that new path. Report the backup path. If creation or copying fails, stop before overwriting the source. Never replace or auto-delete an existing backup.


## Done when

- Every factual claim, command, and path in the edited docs was checked against the current repo, and the Report lists what was inspected and what stayed unexecuted.
- No stale file path or component name remains: run `grep -n` for each path you touched.
- The edited file renders in a markdown preview, and any overwritten file has a reported backup path.

## If it fails

Fix the doc, not the check. Stop and report when a command or path cannot be verified, and mark the claim unverified instead of deleting the check. Rerun every check after changing a file. Stop at a CLAUDE.md migration question without an answer; do not migrate.

## Task-specific references

Read the relevant reference before implementing or reviewing the matching behavior:

- For updating or initializing a context file, README, CONTRIBUTING, or API documentation: [documentation-workflows.md](./references/documentation-workflows.md).
- For selecting durable context, organizing documentation, or editing context-file prose: [context-content-and-writing.md](./references/context-content-and-writing.md). Sentence-level style beyond that belongs to `technical-writing`.

Existing specialized references, when the corresponding topic applies:

- [update-agents.md](./references/update-agents.md).
- [update-readme.md](./references/update-readme.md).
- [update-contributing.md](./references/update-contributing.md).
- [init-agents.md](./references/init-agents.md).

## Report Format

After every operation, display a summary:

```
[OK] Updated AGENTS.md
  - Fixed build command (verified: ran `npm run build`)
  - Added new directory to structure
  - Backup: AGENTS.md.backup.k3Xa9Q

[OK] Updated README.md
  - Added installation section (install command inspected, not run)

[--] CONTRIBUTING.md not found (skipped)
```
