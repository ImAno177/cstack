### Hillclimb

Improve one measurable outcome through repeated, controlled attempts. This is not a one-off bug fix or a benchmark of two finished implementations.

1. Choose a realistic workload that reproduces the limitation. State one primary metric, its improvement direction, a quality or correctness guardrail, a measurable target, and a bounded attempt or time budget. A target cannot be invented from one noisy sample.
2. Build or reuse a repeatable measurement command. Prove it distinguishes a bad workload from an easy one. Vet the harness with benchmark-checklist, freeze inputs and settings, and record baseline, spread, and regression checks.
3. Start a decision trail via show-me-your-work. Every attempt records hypothesis, changed paths, before/after measurements, number of samples, guardrail result, and keep/revert decision.
4. Test one causal hypothesis at a time. For parallel experiments, give each worker an isolated worktree and the same frozen harness; never compare runs polluted by shared writes.
5. Keep a change only when its effect clears the measured noise and the regression check passes. Otherwise revert only that experiment's changes and record the rejection. Do not stack unmeasured tweaks.
6. When progress stalls, revisit the limiter, measurement setup, or hypothesis class. Do not lower the target to claim success. Stop at the bounded budget or on a real dead end and report the best verified result.
7. Verify accepted changes again together through the real interface. If implementation was authorized, continue with opening-a-pr.

**Reply:** workload, baseline and final metric with sample count and spread, target state, accepted and rejected attempts, verification, and next hypothesis.
