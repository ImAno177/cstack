# Third-party skill sources

The root `LICENSE` describes code maintained by cstack. Adapted third-party content keeps its upstream license notice below or in the skill folder (for example `plugins/cstack/skills/frontend-design/LICENSE.txt`).

## pstack

Many core skills and the `default-mode` playbooks are adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan ([@poteto](https://github.com/poteto)), released under the MIT License. Adapted skills: `architect`, `arena`, `benchmark-checklist`, `blast-radius`, `correct`, `create-formal-verification-skill`, `create-verification-skill`, `figure-it-out`, `how`, `in-your-own-words`, `interrogate`, `ketchup`, `ketchup-video`, `maintain-formal-verification-skill`, `maintain-verification-skill`, `principle-*`, `recall`, `reflect`, `reframe`, `sharpen`, `show-me-your-work`, `statechart`, `swarm`, `tdd`, `teach`, `technical-writing`, `typescript-best-practices`, `unslop`, `why`. cstack replaces Cursor-specific model routing and tools with the host-neutral `default-mode/references/subagents.md`, ports `show-me-your-work/scripts/log.sh` and the `reflect` reviewer prompts, and renames three principles (`principle-exhaust-design-space`, `principle-never-block-on-human`, `principle-subtract-before-add`). `default-mode` is adapted from pstack's `poteto-mode`. Its additional `session-pickup`, `pause-safely`, `hillclimb`, `runtime-forensics`, `trace-forensics`, `visual-parity`, and `autonomous-run` playbooks are host-neutral adaptations of the corresponding pstack workflows.

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

`plugins/cstack/skills/md-docs` is adapted from [iliaal/ai-skills](https://github.com/iliaal/ai-skills/tree/main/skills/md-docs) under the MIT License. cstack drops its `SPEC.md`, replaces host tool names with host-neutral wording, removes the `paths` activation filter, and requires confirmation and a backup before removing or regenerating existing content.

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
