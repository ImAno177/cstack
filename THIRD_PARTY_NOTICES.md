# Third-party skill sources

The root `LICENSE` describes code maintained by cstack. Vendored third-party content may have **different licenses**; it is not relicensed by this file. Retain upstream copyright and license notices and confirm redistribution terms before release.

## pstack

Many core skills and the `default-mode` playbooks are adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan ([@poteto](https://github.com/poteto)), released under the MIT License. Adapted skills: `architect`, `arena`, `benchmark-checklist`, `blast-radius`, `correct`, `create-formal-verification-skill`, `create-verification-skill`, `figure-it-out`, `how`, `in-your-own-words`, `interrogate`, `ketchup`, `ketchup-video`, `maintain-formal-verification-skill`, `maintain-verification-skill`, `principle-*`, `reflect`, `sharpen`, `show-me-your-work`, `statechart`, `swarm`, `tdd`, `teach`, `technical-writing`, `typescript-best-practices`, `unslop`, `why`. cstack replaces Cursor-specific model routing and tools with the host-neutral `default-mode/references/subagents.md`, ports `show-me-your-work/scripts/log.sh` and the `reflect` reviewer prompts, and renames three principles (`principle-exhaust-design-space`, `principle-never-block-on-human`, `principle-subtract-before-add`). `default-mode` is adapted from pstack's `poteto-mode`.

```text
MIT License

Copyright (c) 2026 Lauren Tan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## md-docs

`skills/md-docs` is adapted from [iliaal/ai-skills](https://github.com/iliaal/ai-skills/tree/main/skills/md-docs) under the MIT License. cstack drops its `SPEC.md`, replaces host tool names with host-neutral wording, removes the `paths` activation filter, and requires confirmation and a backup before removing or regenerating existing content.

```text
MIT License

Copyright (c) 2025 Every

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Other adapted skills

These skills are not managed by the upstream sync. Each one started from the source below. The status column records what was checked against the source text in May-November 2026 (similarity is a character-level ratio from `difflib`; 1.0 is identical).

| Local entry | Source | License | Copyright | Status |
| --- | --- | --- | --- | --- |
| `skills/conventional-commit`, `skills/create-pr` | [marcelorodrigo/agent-skills](https://github.com/marcelorodrigo/agent-skills) | MIT | Copyright (c) 2026 Marcelo Rodrigo | Adapted; text differs from source |
| `skills/find-skills` | [vercel-labs/skills](https://github.com/vercel-labs/skills/tree/main/skills/find-skills) | MIT | Copyright (c) 2026 Vercel, Inc. | Adapted; text differs from source |
| `skills/peft-lora-qlora` | [Orchestra-Research/AI-research-SKILLs](https://github.com/Orchestra-Research/AI-research-SKILLs/tree/main/03-fine-tuning/peft) | MIT | Copyright (c) 2025 Claude AI Research Skills Contributors | Adapted; `references/troubleshooting.md` is a near-verbatim copy (similarity 0.99) |
| `skills/bitsandbytes-quantization` | [Orchestra-Research/AI-research-SKILLs](https://github.com/Orchestra-Research/AI-research-SKILLs/tree/main/10-optimization/bitsandbytes) | MIT | Copyright (c) 2025 Claude AI Research Skills Contributors | Adapted; `references/memory-optimization.md` is identical to source |
| `skills/scientific-slides`, `skills/scientific-visualization` | [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) | MIT | Copyright (c) 2025 K-Dense Inc. | Adapted; `scientific-visualization/references/publication_guidelines.md` is identical to source |
| `skills/write-kaggle-benchmarks` | [Kaggle/kaggle-skills](https://github.com/Kaggle/kaggle-skills/tree/main/write-kaggle-benchmarks) | Apache-2.0 | Kaggle (see `licenses/Apache-2.0.txt`) | `references/full-guide.md` is a near-verbatim copy of the upstream SKILL.md (similarity 0.98) |
| `skills/android-testing-setup` | [android/skills](https://github.com/android/skills/tree/main/testing/testing-setup) | Apache-2.0 (`skills/android-testing-setup/LICENSE.txt`) | Google LLC (per the skill's metadata) | Adapted; text differs from source (similarity 0.80) |
| `skills/frontend-design` | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | Apache-2.0 (`skills/frontend-design/LICENSE.txt`) | Anthropic, PBC | Adapted; text differs from source |
| `skills/prompt-audit` | [anthropics/skills, claude-api/shared/prompt-audit.md](https://github.com/anthropics/skills/blob/main/skills/claude-api/shared/prompt-audit.md) | Apache-2.0 | Anthropic, PBC | Rewritten for cstack; the upstream guidance is cited in the skill (similarity 0.05) |

### MIT license text for the adapted MIT skills

The four MIT sources above share one permission notice. Their copyright lines are listed first:

```text
Copyright (c) 2026 Marcelo Rodrigo
Copyright (c) 2026 Vercel, Inc.
Copyright (c) 2025 Claude AI Research Skills Contributors
Copyright (c) 2025 K-Dense Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notices and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Upstream-synced skills

Managed sources from `.cstack/upstreams.json`, copied verbatim by `scripts/sync_upstream_skills.py`:

| Local entry | Upstream repository | Upstream path | License |
| --- | --- | --- | --- |
| `skills/kaggle-cli` | [Kaggle/kaggle-cli](https://github.com/Kaggle/kaggle-cli) | `skills` | Apache-2.0 |
| `skills/colab-operator` | [googlecolab/google-colab-cli](https://github.com/googlecolab/google-colab-cli) | `skills/colab-operator` | Apache-2.0 |
| `skills/hf-cli` | [huggingface/skills](https://github.com/huggingface/skills) | `skills/hf-cli` | Apache-2.0 |
| `skills/trl-training` | [huggingface/skills](https://github.com/huggingface/skills) | `skills/trl-training` | Apache-2.0 |
| `skills/agents-sdk` | [cloudflare/skills](https://github.com/cloudflare/skills) | `skills/agents-sdk` | Apache-2.0 |
| `skills/cf-cli` | [cloudflare/skills](https://github.com/cloudflare/skills) | `skills/cf-cli` | Apache-2.0 |
| `skills/cloudflare` | [cloudflare/skills](https://github.com/cloudflare/skills) | `skills/cloudflare` | Apache-2.0 |
| `skills/cloudflare-email-service` | [cloudflare/skills](https://github.com/cloudflare/skills) | `skills/cloudflare-email-service` | Apache-2.0 |
| `skills/cloudflare-one` | [cloudflare/skills](https://github.com/cloudflare/skills) | `skills/cloudflare-one` | Apache-2.0 |
| `skills/cloudflare-one-migrations` | [cloudflare/skills](https://github.com/cloudflare/skills) | `skills/cloudflare-one-migrations` | Apache-2.0 |
| `skills/durable-objects` | [cloudflare/skills](https://github.com/cloudflare/skills) | `skills/durable-objects` | Apache-2.0 |
| `skills/sandbox-migrate-to-next` | [cloudflare/skills](https://github.com/cloudflare/skills) | `skills/sandbox-migrate-to-next` | Apache-2.0 |
| `skills/sandbox-next` | [cloudflare/skills](https://github.com/cloudflare/skills) | `skills/sandbox-next` | Apache-2.0 |
| `skills/sandbox-stable` | [cloudflare/skills](https://github.com/cloudflare/skills) | `skills/sandbox-stable` | Apache-2.0 |
| `skills/turnstile-spin` | [cloudflare/skills](https://github.com/cloudflare/skills) | `skills/turnstile-spin` | Apache-2.0 |
| `skills/web-perf` | [cloudflare/skills](https://github.com/cloudflare/skills) | `skills/web-perf` | Apache-2.0 |
| `skills/workers-best-practices` | [cloudflare/skills](https://github.com/cloudflare/skills) | `skills/workers-best-practices` | Apache-2.0 |
| `skills/wrangler` | [cloudflare/skills](https://github.com/cloudflare/skills) | `skills/wrangler` | Apache-2.0 |

Each upstream repository is licensed under the Apache License 2.0; a copy is in [`licenses/Apache-2.0.txt`](licenses/Apache-2.0.txt). The synced files are unmodified, so their own notices apply. This inventory is not a blanket license clearance.

`.cstack/upstreams.lock.json` records each managed snapshot's source commit and local content hash. Inspect those changes and retained notices in the automated PR before merging.
