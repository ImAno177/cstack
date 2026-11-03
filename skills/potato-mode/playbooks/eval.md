### Agent evaluation

Evaluate a model and its harness together.

1. Freeze the task set, environment, tools, model configuration, grader, and stopping rule before running candidates.
2. Use clean isolated workspaces and organic prompts. Do not leak the rubric or variant names.
3. Grade the final artifact and the trajectory separately, then classify model, harness, tool, environment, and evaluator failures.
4. Repeat representative cases, report variance and cost, and promote only a change that improves the target without unacceptable regressions.
