### Feature

Own the design and verification; delegate only disjoint work with isolated writes.

1. Map the affected subsystem with `how`.
2. Define the data shape, owner, boundary, and observable success state before implementation.
3. Parallelize only independent work. Serialize shared state and name the reason.
4. Prefer existing interfaces and the smallest complete behavior. Use `arena` only when alternatives have materially different tradeoffs.
5. Verify the matching surface, inspect the diff, and report open decisions and evidence.
