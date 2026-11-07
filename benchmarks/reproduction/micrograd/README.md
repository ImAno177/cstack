# Micrograd reproduction: two-agent A/B benchmark

Reference: [karpathy/micrograd](https://github.com/karpathy/micrograd), pinned at
\`7bc720e951fe422b8f8814aa5aa1b64121d26b4c\` (2026-08-03).
Its engine and neural-network layer are about 150 lines in total.

**Goal:** Evaluate whether cstack skills improve implementation correctness, effort,
and completion reliability, not merely skill-router classification.

## Two conditions

- **A / baseline:** Codex CLI without cstack skill files in the trial workspace.
- **B / skills:** The same Codex CLI/model, with cstack's current skills copied into
  the trial workspace under \`.agents/skills/\`. Nested platform groups are flattened
  to top-level skill directories to support automatic discovery.

Both receive precisely the same task in [TASK.md](TASK.md), workspace permissions,
and per-run timeout. Run the pair concurrently in separate directories. Repeat
each pair at least three times. There is no tool here to launch Codex agents in
this chat environment; the runner is designed to execute on a Codex-enabled host.

Run from the cstack root on a host with an authenticated Codex CLI:

\`\`\`sh
python benchmarks/reproduction/run_codex_ab.py \
  --cstack . --model YOUR_PINNED_MODEL --runs 3 \
  --output /tmp/cstack-micrograd-2026-11-07
\`\`\`

The runner starts **two** independent \`codex exec\` processes per repetition.
It saves one JSON event log, stderr log and isolated workspace for each process.
The grader is called after each agent stops, never inside its workspace.

## Fairness rules

1. Pin **model and cstack Git commit**, CLI version, task hash and tool policy.
2. Disable globally installed cstack skills for the baseline. Check that
   startup logs actually show zero cstack skills for A and enabled skills for B.
3. No network access or access to reference source, the hidden grader or other
   trial workspaces. The CLI sandbox is not a substitute for an OS-level
   containment boundary. For a trustworthy benchmark, run each agent in an
   isolated VM/container with no mount of the grading directory.
4. Log selected skills (from the agent's event stream), retries, failures,
   tokens, wall time and real output files. The runner reports token usage
   only when Codex events explicitly expose it; otherwise \`null\`.
5. Reject contaminated trials. Agent B having skills copied into a directory
   does **not** prove it discovered or activated any of them; inspect events.
6. Keep the grader and reference solution out of prompts and agent-visible files.

## Grading

[grade.py](grade.py) contains nine black-box tests: arithmetic, reverse-mode
gradients, shared-node handling, reflected operators, ReLU boundaries,
finite-difference checks, neuron and layer APIs, parameter counts and SGD.
Scores are \`passed/9\`. Record test failures plus time and token usage.
Compare pass rates and costs on matched runs rather than claim significance
from only three runs.

## Limitations

The task is small enough that a strong model may pass 9/9 under both conditions.
In that case, run separate **repo maintenance** cases (bug fix, test creation,
code review, performance profiling) rather than making the task artificially hard
or claiming skills are useless. This is one benchmark, not a whole-skill evaluation.
