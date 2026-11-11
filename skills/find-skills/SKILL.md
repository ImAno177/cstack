---
name: find-skills
description: Discovers and installs agent skills from the open skills ecosystem with the `npx skills` CLI. Use when the user asks "how do I do X", "find a skill for X", "is there a skill that can...", or wants to extend agent capabilities in a specialized domain. Not for skills already in this pack; read them directly.
---

# Find Skills

Search the open agent skills ecosystem with the Skills CLI (`npx skills`), verify quality, and present options. Install only after the user confirms.

## Commands

- `npx skills find [query] [--owner <owner>]` searches by keyword, optionally scoped to a GitHub owner.
- `npx skills add <package>` installs a skill from GitHub or another source.
- `npx skills update` updates all installed skills.
- `npx skills init <name>` scaffolds a new skill.

Readiness check: run `npx skills find react` once. If `npx` or the network is unavailable, tell the user and browse https://skills.sh/ instead.

## Not for

- Skills already installed or listed in this pack: read them directly.
- Tasks you can do directly with no specialized skill.

## Workflow

1. Name the domain (React, testing, deployment) and the specific task (write tests, review PRs).
2. Check the [skills.sh leaderboard](https://skills.sh/) for a well-known skill in the domain. It ranks by installs; `vercel-labs/agent-skills` (React, Next.js, web design) and `anthropics/skills` (frontend design, documents) are common sources.
3. Run `npx skills find <specific keywords>`, for example `npx skills find react performance`, `npx skills find pr review`, `npx skills find changelog`. Use specific keywords ("react testing", not "testing") and retry with alternates ("deployment", "ci-cd") when results are thin.
4. Verify each candidate before recommending it. Search results alone are not enough:
   - Install count: prefer 1K+; treat under 100 with caution.
   - Source: official owners (`vercel-labs`, `anthropics`, `microsoft`) over unknown authors.
   - Repository: treat under 100 GitHub stars with skepticism.
5. Present the skill name and what it does, install count and source, the install command, and the skills.sh link.
6. Show the user the source repository, the skill's SKILL.md and any scripts, and whether the install is project-level or global. A skill is third-party code and instructions that future sessions follow. Run `npx skills add <owner/repo@skill>` only after they confirm. Add `-g` only when the user asks for a user-level install. Never pass `-y`; let the CLI's own confirmation run.

## No match

Say no existing skill was found, offer to do the task directly, and mention `npx skills init <name>` for building one.

## Done when

- The reply lists each recommended skill with install count, source, and install command, or says no match was found.
- A skill is installed only after explicit user confirmation, and `npx skills add` output is quoted when it ran.

## If it fails

A search that returns nothing: change the keywords (synonyms, the `--owner` filter) before retrying. After three different queries, report no match and offer to do the task directly. Do not lower the quality thresholds in step 4 to produce a recommendation.

## Example reply

```
I found a skill that might help. "react-best-practices" gives React and Next.js
performance guidelines from Vercel Engineering (<install count> installs,
source: vercel-labs/agent-skills).

Install it with:
npx skills add vercel-labs/agent-skills@react-best-practices

Learn more: https://skills.sh/vercel-labs/agent-skills/react-best-practices
Next step: I show you the repository and its SKILL.md, then install at project level once you confirm.
```
