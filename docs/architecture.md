# cstack architecture

The repository root is the installable plugin. A skill is a portable capability; a playbook is a task-shaped operating mode selected by `potato-mode`.

## What was adopted from pstack

- A front door routes work through a small set of playbooks instead of making every workflow a top-level skill.
- Conditional detail lives beside the entrypoint in `playbooks/` or `references/`, so normal work does not load every mode.
- Documentation separates setup, routing, design, verification, and customization concerns.
- Runtime behavior belongs to hooks or extensions; prose skills do not pretend to enforce lifecycle events.

## What stays out of cstack

- `assets/logo.png` in pstack is branding, not instruction or runtime input, so cstack does not carry it.
- pstack `agents/`, Cursor automations, Bugbot helpers, and Claude harness adapters are host-specific. cstack keeps portable delegation and completion behavior in skills and hooks.
- pstack's PR watcher and statechart fixture corpus are executable tooling or test data, not portable skill content. They are not copied without a cstack-owned host adapter.

## Source ownership

- Core skills under `skills/` are maintained in this repository.
- Platform skills under `skills/kaggle/`, `skills/colab/`, `skills/huggingface/`, and `skills/cloudflare/` retain their upstream organization. Managed entries are declared in `.cstack/upstreams.json` and refreshed by `scripts/sync_upstream_skills.py`.
- `hooks/`, `scripts/`, manifests, and generated indexes are packaging or runtime surfaces. Changes to them require the repository validators and an artifact check.

## Harness rule

For local model and Pi work, keep model adaptation, tool registry, loop control, state, and evaluation separate. Use `skills/agent-harness/references/lfm3-pi.md` for the LFM3-specific constraints. Do not use a one-off PowerShell helper or a final model sentence as the proof that a harness worked.

## Design sources

- [pstack](https://github.com/cursor/plugins/tree/main/pstack) for the front-door plus playbook organization.
- [Matt Pocock's skills](https://github.com/mattpocock/skills) for small, composable, phase-specific skills and agent-readable repository guidance.
- [OpenAI skill authoring guidance](https://developers.openai.com/plugins/build/skills) and [Authoring Agent Skills](https://arxiv.org/abs/2607.25032) for staged loading, narrow interfaces, references, scripts, and behavioral evaluation.
- [Pi](https://github.com/badlogic/pi-mono) and the [LFM3 model card](https://huggingface.co/LiquidAI/LFM3-1.7B) for the harness/resource split and local-model tool-loop constraints.
- [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) for plugin seams, service ownership, and inspectable session writes; [Prime Agent](https://github.com/PrimeIntellect-ai/prime-agent) for resumable long-running state and evidence-backed refinement.
- [Harness Engineering](https://arxiv.org/abs/2609.00006) for the seven-subsystem comparison and the recommendation to start with a small linear loop, deterministic code retrieval, deferred loading, explicit policies, and measured delegation.
