# Third-party skill sources

The root `LICENSE` describes code maintained by cstack. Vendored third-party content may have **different licenses**; it is not relicensed by this file. Retain upstream copyright and license notices and confirm redistribution terms before release.

## pstack

Many core skills and the `default-mode` playbooks are adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan ([@poteto](https://github.com/poteto)), released under the MIT License. Adapted skills: `architect`, `arena`, `benchmark-checklist`, `blast-radius`, `correct`, `create-formal-verification-skill`, `create-verification-skill`, `figure-it-out`, `how`, `in-your-own-words`, `interrogate`, `ketchup`, `ketchup-video`, `maintain-formal-verification-skill`, `maintain-verification-skill`, `principle-*`, `reflect`, `sharpen`, `show-me-your-work`, `statechart`, `swarm`, `tdd`, `teach`, `technical-writing`, `typescript-best-practices`, `unslop`, `why`. cstack shortens several of them, removes Cursor-specific model routing, and renames three principles (`principle-exhaust-design-space`, `principle-never-block-on-human`, `principle-subtract-before-add`). `default-mode` is adapted from pstack's `poteto-mode`.

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

## Upstream-synced skills

Managed sources from `.cstack/upstreams.json`:

| Local entry | Upstream repository | Upstream path |
| --- | --- | --- |
| `skills/kaggle/kaggle-cli` | [Kaggle/kaggle-cli](https://github.com/Kaggle/kaggle-cli) | `skills` |
| `skills/colab/colab-operator` | [googlecolab/google-colab-cli](https://github.com/googlecolab/google-colab-cli) | `skills/colab-operator` |
| `skills/huggingface/hf-cli` | [huggingface/skills](https://github.com/huggingface/skills) | `skills/hf-cli` |
| `skills/huggingface/trl-training` | [huggingface/skills](https://github.com/huggingface/skills) | `skills/trl-training` |

Additional manually maintained or imported platform skill files (including the Cloudflare group) require their own provenance/license review. This inventory is not a blanket license clearance.

`.cstack/upstreams.lock.json` records each managed snapshot's source commit and local content hash. Inspect those changes and retained notices in the automated PR before merging.
