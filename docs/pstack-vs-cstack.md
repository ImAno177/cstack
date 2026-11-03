# pstack and cstack

This comparison keeps the useful structure from Cursor's pstack while documenting the boundaries that make cstack portable across ChatGPT, Codex, Grok Build, and Grok Bot.

| Concern | pstack | cstack decision |
| --- | --- | --- |
| Host boundary | A Cursor plugin with Cursor-oriented agents, automations, and model/tool assumptions | The repository root is the installable plugin; portable skills do not depend on a Cursor path or model name |
| Default entrypoint | `poteto-mode` selects a task-shaped playbook | `default-mode` is the single canonical entrypoint; the old name has no compatibility alias |
| Workflow organization | A front door plus playbooks keeps task modes out of the top-level catalog | Adopted as `skills/default-mode/playbooks/`; keep playbooks short and load only the selected one |
| Runtime behavior | Host-specific agents, automations, hooks, and harness adapters live beside the skills | Keep lifecycle enforcement in `hooks/` or a host extension; keep procedural guidance in skills and declare host limits |
| Extensibility | pstack contains useful host integrations and executable helpers for its target host | cstack uses owned seams: skills for procedures, hooks for lifecycle, plugins for replaceable services, and adapters for external systems |
| Upstream platform content | Target-host organization is the source of truth | Preserve upstream groups such as `skills/kaggle/`, `skills/colab/`, `skills/huggingface/`, and `skills/cloudflare/`; refresh them through `.cstack/upstreams.json` and CI |
| Verification | pstack provides a strong workflow vocabulary and harness guidance | Add stack validators, generated plugin indexes, artifact receipts, incident-driven guards, and representative evaluation cases |
| What is intentionally omitted | Branding assets, Cursor-only agents/automations, and target-host watchers | Omitted unless a cstack-owned adapter proves a portable contract; this avoids shipping dead host instructions |

## What cstack learned from pstack

- Put one default workflow at the front door instead of asking every agent to invent its own sequence.
- Keep task-specific detail in playbooks and deeper references so the default context stays small.
- Separate procedural skills from lifecycle/runtime behavior.
- Treat host-specific integrations as adapters, not as universal instructions.

## What cstack adds

- A root plugin layout and manifests for multiple hosts.
- Provenance and scheduled synchronization for large platform skills.
- A runtime-oriented `agent-harness` skill with explicit loop, tool, context, policy, orchestration, and extensibility decisions.
- Incident-driven guards for non-vacuous verification, resource cleanup, bounded delegation, compaction handoffs, stable tool catalogs, safe batching, and skill retirement.

The primary pstack references are its [README](https://github.com/cursor/plugins/blob/main/pstack/README.md) and [poteto-mode skill](https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/poteto-mode/SKILL.md). The name is intentionally normalized to `default-mode` in cstack because this is the workflow's function, not a host-specific brand.
