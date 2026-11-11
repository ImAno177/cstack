# Third-party skill sources

The root `LICENSE` describes code maintained by cstack. Vendored third-party content may have **different licenses**; it is not relicensed by this file. Retain upstream copyright and license notices and confirm redistribution terms before release.

Managed sources from `.cstack/upstreams.json`:

| Local entry | Upstream repository | Upstream path |
| --- | --- | --- |
| `skills/kaggle/kaggle-cli` | [Kaggle/kaggle-cli](https://github.com/Kaggle/kaggle-cli) | `skills` |
| `skills/colab/colab-operator` | [googlecolab/google-colab-cli](https://github.com/googlecolab/google-colab-cli) | `skills/colab-operator` |
| `skills/huggingface/hf-cli` | [huggingface/skills](https://github.com/huggingface/skills) | `skills/hf-cli` |
| `skills/huggingface/trl-training` | [huggingface/skills](https://github.com/huggingface/skills) | `skills/trl-training` |

Additional manually maintained or imported platform skill files (including the Cloudflare group) require their own provenance/license review. This inventory is not a blanket license clearance.

`.cstack/upstreams.lock.json` records each managed snapshot's source commit and local content hash. Inspect those changes and retained notices in the automated PR before merging.
