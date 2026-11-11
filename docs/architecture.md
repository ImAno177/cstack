# cstack architecture

The repository root is the installable plugin. A skill is a portable capability; a playbook is a task-shaped operating mode selected by `default-mode`.

## What was adopted from pstack

- A `default-mode` front door routes work through a small set of playbooks instead of making every workflow a top-level skill.
- Conditional detail lives beside the entrypoint in `playbooks/` or `references/`, so normal work does not load every mode.
- Documentation separates setup, routing, design, verification, and customization concerns.
- Runtime behavior, if needed later, belongs to explicit host integrations; prose skills do not pretend to enforce lifecycle events.

## What stays out of cstack

- `assets/logo.png` in pstack is branding, not instruction or runtime input, so cstack does not carry it.
- pstack `agents/` (poteto-agent, Comment Sicko), Cursor automations, Bugbot helpers, and Claude harness adapters are host-specific. cstack keeps portable delegation and completion guidance in skills without startup hooks. The one exception is `agents/pr-reviewer.md`, a Claude Code subagent for the pre-merge review that other hosts ignore; skills name it only as "on Claude Code".
- pstack's PR watcher and statechart fixture corpus are executable tooling or test data, not portable skill content. They are not copied without a cstack-owned host adapter.

## Divergence from pstack

- Delegation-heavy skills (`architect`, `arena`, `swarm`, `interrogate`, `how`, `why`, `reflect`, `show-me-your-work`, `figure-it-out`) keep pstack's phases and references. Cursor model slugs, `pstack-models.mdc`, Task fields, and transcript paths are replaced by one host-neutral reference, `skills/default-mode/references/subagents.md`, which maps them for Claude Code and other hosts.
- pstack makes nearly every skill `disable-model-invocation` and reaches them through `poteto-mode`. cstack keeps skills model-invocable so hosts without a mode skill can discover them, and opts out only slash-only skills.
- pstack's planning stance holds: there is no planning skill. `figure-it-out` and `multi-phase-plan.md` cover plans when the work needs one.
- Shipping work stays in playbooks (`opening-a-pr.md`, `babysit.md`, `shipping.md`), condensed and forge-neutral, instead of skills.
- Not ported: `poteto-help`, `setup-pstack`, `automate-me`, `recall`, `bro`, `no-comments`, `make-bot-ui`, and the Cursor-specific playbooks (autopilot, orchestrate, worktree and simulator cleanup). `AGENTS.md` carries the no-comments rule.
- cstack adds skills pstack does not have: research (`literature-review`), security (`security-audit`), browser QA (`webapp-testing`), platform groups, and agent-runtime skills.

## Source ownership

- Core skills under `skills/` are maintained in this repository.
- Third-party skills (Cloudflare, Kaggle, Colab, Hugging Face) live at `skills/<name>/` like every other skill and are copied verbatim from upstream by `.cstack/upstreams.json` and `scripts/sync_upstream_skills.py`. A one-level layout is the only one every host scans, so there are no group folders.
- `scripts/`, manifests, and generated indexes are packaging or runtime surfaces. Changes to them require the repository validators and an artifact check.

## Harness rule

For local model and Pi work, keep model adaptation, tool registry, loop control, state, and evaluation separate. Use `skills/agent-harness/references/lfm3-pi.md` for the LFM3-specific constraints. Do not use a one-off PowerShell helper or a final model sentence as the proof that a harness worked.

## Design sources

- [pstack](https://github.com/cursor/plugins/tree/main/pstack) for the front-door plus playbook organization.
- [Matt Pocock's skills](https://github.com/mattpocock/skills) for small, composable, phase-specific skills and agent-readable repository guidance.
- [OpenAI skill authoring guidance](https://developers.openai.com/plugins/build/skills) and [Authoring Agent Skills](https://arxiv.org/abs/2607.25032) for staged loading, narrow interfaces, references, scripts, and behavioral evaluation.
- [Pi](https://github.com/badlogic/pi-mono) and the [LFM3 model card](https://huggingface.co/LiquidAI/LFM3-1.7B) for the harness/resource split and local-model tool-loop constraints.
- [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) for plugin seams, service ownership, and inspectable session writes; [Prime Agent](https://github.com/PrimeIntellect-ai/prime-agent) for resumable long-running state and evidence-backed refinement.
- [Harness Engineering](https://arxiv.org/abs/2609.00006) for the seven-subsystem comparison and the recommendation to start with a small linear loop, deterministic code retrieval, deferred loading, explicit policies, and measured delegation.
