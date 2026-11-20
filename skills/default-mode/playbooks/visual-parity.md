### Visual parity

Prove that a migration or rewrite preserves the reference UI. The baseline is immutable during the comparison.

1. Capture the original UI before edits, across the relevant routes, breakpoints, interaction states, and deterministic fixtures. Record viewport, fonts, device scale, browser, and animations; otherwise image differences are ambiguous.
2. Choose an explicit comparison policy before writing code: exact pixel equality or a documented tolerance for rendering noise. Never adjust the baseline or tolerance after seeing a failure to make the change pass.
3. Change a small set of components at a time, shared primitives first. Separate worktrees if different agents own independent components.
4. Capture the same states after each change and run image diffs plus functional interaction checks. A pass in the visual diff does not replace checking keyboard, navigation, or error behavior.
5. Investigate nonmatching regions. Change the product code or honestly report why equivalence is not proven. Do not hide differences in masks or alter the capture harness to get green.
6. Ship only the verified set and preserve before/after artifacts with the PR.

**Reply:** components and states compared, baseline location, exact comparison command and threshold, failed diffs, and any unverified behavior.
