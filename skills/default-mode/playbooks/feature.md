### Feature

Own the design and verification; delegate only disjoint work with isolated writes.

1. Map the affected subsystem with `how`.
2. Define the data shape, owner, boundary, and observable success state before implementation.
3. Parallelize only independent work. Serialize shared state and name the reason.
4. Prefer existing interfaces and the smallest complete behavior. Use `arena` only when alternatives have materially different tradeoffs.
5. Apply `principle-boundary-discipline` to every surface that accepts outside input: unguessable identifiers, one error format for every request, deliberate handling of each input class.
6. Verify the matching surface with the hostile-input probes in `principle-prove-it-works`, inspect the diff, and report open decisions and evidence.
