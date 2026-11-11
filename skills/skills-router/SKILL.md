---
name: skills-router
description: Choose the smallest set of installed skills when a request plausibly matches multiple capabilities or spans domains, artifacts, or connected apps. Do not use when a single skill clearly owns the task.
license: MIT
---

# Skills router

Invoke only when selection is ambiguous or the request spans capabilities. If one skill clearly owns the outcome, use it directly. Never invent an unavailable route. Routes name each host's skill; use only the one the current host has installed. On Claude Code, plugin skills are namespaced, e.g. `cstack:default-mode` or `/cstack:default-mode`.

## Routes

- image generation or raster image editing -> `imagegen`
- DOCX or Word layout, redlining, or comments -> `documents:documents`; on Claude -> `document-skills:docx`
- PDF work or visual PDF verification -> `pdf:pdf`; on Claude -> `document-skills:pdf`
- PowerPoint or presentation work -> `presentations:Presentations`; on Claude -> `document-skills:pptx`
- spreadsheet files -> `spreadsheets:Spreadsheets`, on Claude `document-skills:xlsx`; live Excel -> `spreadsheets:excel-live-control`
- connected Google Drive, Docs, Sheets, or Slides -> the matching `google-drive:*` skill
- ChatGPT Pages or Spaces -> the matching `pages:*` skill
- website creation or management -> `sites:sites`; site remix -> `sites:sites-remix`
- ChatGPT Work pets -> the matching `work-pets:*` skill
- Cloudflare Workers, Wrangler, Durable Objects, Email, Zero Trust, Turnstile, Agents SDK, or sandbox -> the narrowest installed Cloudflare skill; use `cloudflare` only when none is narrower
- generic web performance, Core Web Vitals, Lighthouse -> `web-perf`
- LoRA or QLoRA fine-tuning -> `peft-lora-qlora`
- bitsandbytes quantization -> `bitsandbytes-quantization`
- TRL training -> `trl-training`
- Kaggle CLI -> `kaggle-cli`; Google Colab runtime or CLI -> `colab-operator`; Hugging Face Hub or CLI -> `hf-cli`
- scientific or publication figures -> `scientific-visualization`; research slides -> `scientific-slides`
- native Android testing -> `android-testing-setup`; browser end-to-end testing of a web app -> `webapp-testing`; frontend design -> `frontend-design`
- a repeatable project verification harness -> `create-verification-skill`; keep it current -> `maintain-verification-skill`
- test-first bug fix or regression test -> `tdd`; security review, threat model, or secrets -> `security-audit`
- research papers, related work, or citation checks -> `literature-review`
- building an MCP server -> `example-skills:mcp-builder` when installed
- README, AGENTS.md, CLAUDE.md, or CONTRIBUTING -> `md-docs`; conventional commits -> `conventional-commit`; pull requests -> `create-pr`; architecture boundaries -> `architect`; code walkthroughs -> `how`; Kaggle benchmarks -> `write-kaggle-benchmarks`
- review a change, commit, or PR -> `change-review`; audit the whole repository -> `repo-audit`; assess affected consumers -> `blast-radius`; recurring mistake prevention -> `correct`
- shortcut debt or deferred work -> `shortcut-debt`; architecture rationale or postmortems -> `why`
- extract learning from one episode -> `reflect`; promote learning across episodes and evaluate retention -> `continual-learning`
- agent loops, Pi, model adapters, or harnesses -> `agent-harness`; compare agent outcomes across tasks -> `agent-evaluation`
- parallel delegation with independent ownership -> `multi-agent-workflow`; same-task alternatives -> `arena`; parallel coverage slices -> `swarm`; adversarial review -> `interrogate`
- async or batch tool execution -> `tool-orchestration`; long-run decision trail -> `show-me-your-work`
- verify an agent's actual side effects -> `agent-completion`; context compaction or long-run handoff -> `agent-context`
- stale prompts, conflicting rules, or cruft -> `prompt-audit`; AI-sounding prose -> `unslop`
- create or update a skill -> `skill-creator`; discover skills -> `skill-installer` or `find-skills`; plugin settings -> `plugin-management:plugin-management`
- Codex or OpenAI configuration -> `openai-docs`
- non-trivial engineering with no narrower owner -> `default-mode`; broad multi-phase migration needing an explicit plan -> `figure-it-out`

## Selection rules

1. Pick the most specific skill for the user-visible outcome, not the one with the broadest description.
2. For review, route by **scope**: changed diff -> `change-review`, entire repo -> `repo-audit`, hostile-design challenge -> `interrogate`.
3. For learning, route by **stage**: one episode -> `reflect`, measured reusable change -> `continual-learning`, stale instructions -> `prompt-audit`.
4. For Cloudflare, prefer a narrow named product skill over the umbrella `cloudflare` skill.
5. Add a supporting skill only for a second required output. Read each selected `SKILL.md` before acting; obey the host's installed catalog and policy.
6. Do not auto-add a general workflow, review, or audit skill when the primary skill already owns the task.
