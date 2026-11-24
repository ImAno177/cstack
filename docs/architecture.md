# cstack architecture

cstack is a marketplace: one repository, several plugins, each installed on its own. A skill is one capability in `plugins/<plugin>/skills/<name>/`. A playbook is a task-shaped operating mode inside `default-mode`. A plugin is the unit a user installs and a host loads.

## Why this layout

The layout follows what the agent-skill research and the hosts' own documentation say. Each point below names the decision and its evidence.

### Few listed skills per plugin

The model sees the name and description of every listed skill on every turn and picks among them. Selection gets worse as that list grows, and similar skills are the main cause.

- In a controlled sweep of 5 to 200 skills, selection accuracy stayed above 90% up to 20 skills, fell steadily after 30, and reached about 20% at 200. Adding one look-alike competitor per skill cut accuracy by 7 to 30%, and two competitors by 17 to 63%. Grouping skills into categories and choosing in two steps recovered 37 to 40 points for GPT-4o-mini and 9 to 10 for GPT-4o at 120 skills ([Li 2026, arXiv 2601.04748](https://arxiv.org/abs/2601.04748)).
- In NVIDIA's paired live evaluation, skill lift held for 1 to 20 visible skills while wall time rose from 258 s to 451 s; at 50 visible skills the with-skill pass rate fell from 0.725 to 0.55 and wall time reached 1,290 s ([ACES, arXiv 2608.20614](https://arxiv.org/abs/2608.20614)).
- Claude Code gives the skill listing about 1% of the context window and drops descriptions of the least-used skills when it overflows ([Claude Code skills](https://code.claude.com/docs/en/skills)). Every enabled plugin's listed skills and agents cost context on every turn ([Claude Code plugins](https://code.claude.com/docs/en/plugins)).

cstack 0.8 shipped 103 skills in one plugin, 76 of them listed. 0.9 splits them by audience into three plugins and lists 42 in total; a user who installs only `cstack` sees 27. `validate_skill_stack.py` fails when a plugin lists more than `max_listed_skills_per_plugin` (30) in `.cstack/skill-policy.json`.

### A two-level route instead of a flat list

Workflows a user starts on purpose (`arena`, `swarm`, `interrogate`, `figure-it-out`, `show-me-your-work`, `correct`, `reflect`, `teach`, the verification skills, and the 23 principles) set `disable-model-invocation: true`. They stay out of the listing. `default-mode` is the first-level choice and links to them by relative path, which is the hierarchical routing the study above found effective. The user can still type any of them as `/cstack:<name>`. pstack takes the same approach, reaching its workflows through `poteto-mode`.

When two listed skills overlap, each description names the other and says when to use it instead. `overlap_groups` in the policy file enforces this.

### Plugins split by audience

The three plugins match three kinds of users: anyone writing code (`cstack`), people building agents and harnesses (`cstack-harness`), and people doing research or ML work (`cstack-research`). Claude Code marketplaces hold any number of plugins, each with a relative `source` path, and users install them by name ([plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)). Anthropic's own marketplaces split the same way: `anthropics/skills` ships five plugins and `claude-plugins-official` keeps each plugin in `plugins/<name>/`.

A skill links only inside its own plugin, because a host installs one plugin folder and a link to a sibling plugin breaks. Mentions of a skill in another plugin use its name and the plugin it ships in. `validate_skill_stack.py` rejects links that leave their plugin.

### Components live inside the plugin

A Claude Code plugin is a folder with `skills/`, `agents/`, `hooks/hooks.json`, and other component folders at its root ([plugins reference](https://code.claude.com/docs/en/plugins-reference)). `agents/` holds subagents, which register under the plugin's name (`cstack:verifier`). Until 0.8 the repository root was the plugin, so these folders sat next to the repository's own docs and scripts. Now they sit in `plugins/cstack/`, and the root holds only repository tooling and the marketplace files.

### Generated manifests

Each host wants its own manifest: `.claude-plugin/`, `.codex-plugin/`, `.grok-plugin/`, `.cursor-plugin/`, plus a marketplace file for each and `skills.sh.json` for `npx skills`. Hand-editing thirteen version strings drifts. `scripts/build_manifests.py` writes all of them from `.cstack/catalog.json`, and CI runs it with `--check`. superpowers, Cloudflare, and Hugging Face keep their multi-host manifests the same way, from one source.

### No vendored third-party skills

cstack 0.8 copied 18 skills from Cloudflare, Hugging Face, Kaggle, and Colab, with a sync workflow and lockfile to keep them current. Those owners publish the skills and their own marketplaces, so the copies only added listed skills and maintenance. A large-scale scan found vulnerabilities in 26.1% of 31,132 community skills, and skills that bundle scripts were 2.12 times as likely to contain one ([Liu et al. 2026, arXiv 2601.10338](https://arxiv.org/abs/2601.10338), as summarized in [Xu and Yan 2026, arXiv 2602.12430](https://arxiv.org/abs/2602.12430)). Installing from the owner keeps provenance with the owner. The README lists the install commands.

### Skill format

Each `SKILL.md` follows the Agent Skills format and Anthropic's authoring guidance ([best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)):

- `name` is lowercase kebab-case, at most 64 characters, and matches its folder.
- `description` is at most 1,024 characters and says what the skill does and when to use it, and when not to.
- The entrypoint stays short (`max_entry_lines`, 160 here; Anthropic's ceiling is 500). Detail goes in `references/` one level deep, and deterministic steps go in `scripts/`.

`validate_plugin.py` checks the name, description, and folder rules.

### Proof comes from runs, not from scans

Static checks catch authoring mistakes but do not predict whether a skill helps. In ACES, neither structural scores nor LLM-judge scores had a detectable correlation with live skill lift (Spearman ρ = −0.02 and −0.03, both indistinguishable from zero; [arXiv 2608.20614](https://arxiv.org/abs/2608.20614)). The validators here are a floor. Claims that a change improves agents need the paired runs in [skill-effect-benchmark.md](skill-effect-benchmark.md) and the routing runs in [routing-benchmark.md](routing-benchmark.md).

## What was adopted from pstack

- A `default-mode` front door routes work through a small set of playbooks instead of making every workflow a top-level skill.
- Conditional detail lives beside the entrypoint in `playbooks/` or `references/`, so normal work does not load every mode.
- Runtime behavior belongs to explicit host integrations. `plugins/cstack/hooks/` is that integration: deterministic Node.js scripts that inject the model's skill and pinned rules, re-inject rules after compaction, and gate stopping and merging. Every block message names the step that clears it.
- `agents/verifier.md` gives the pre-merge verdict the way pstack's shipping playbook does: an agent that did not write the change runs it as a user would and returns `PASS`, `PASS+NOTES`, or `FAIL`.

## Divergence from pstack

- Delegation-heavy skills keep pstack's phases. Cursor model slugs, Task fields, and transcript paths are replaced by one host-neutral reference, `plugins/cstack/skills/default-mode/references/subagents.md`.
- pstack has no planning skill, and neither does cstack: `figure-it-out` and `multi-phase-plan.md` cover plans when the work needs one.
- Shipping stays in playbooks (`opening-a-pr.md`, `babysit.md`, `shipping.md`), condensed and forge-neutral.
- Not ported: `poteto-help`, `setup-pstack`, `automate-me`, `bro`, `no-comments`, `make-bot-ui`, and the Cursor-specific playbooks. See [pstack-audit-2026-11-21.md](pstack-audit-2026-11-21.md).
- cstack adds research (`literature-review`), security (`security-audit`), browser QA (`webapp-testing`), the harness plugin, and the model-specific skills.

## Harness rule

For local model and Pi work, keep model adaptation, tool registry, loop control, state, and evaluation separate. Use `plugins/cstack-harness/skills/agent-harness/references/lfm3-pi.md` for the LFM3-specific constraints. A final model sentence is not proof that a harness worked.

## Other design sources

- [pstack](https://github.com/cursor/plugins/tree/main/pstack) for the front door plus playbooks.
- [Matt Pocock's skills](https://github.com/mattpocock/skills) for small, composable skills and the split between user-invoked and model-invoked skills.
- [Authoring Agent Skills](https://arxiv.org/abs/2607.25032) for staged loading, narrow interfaces, and behavioral evaluation.
- [Harness Engineering](https://arxiv.org/abs/2609.00006) for starting with a small linear loop, deferred loading, explicit policies, and measured delegation.
