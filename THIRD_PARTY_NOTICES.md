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
