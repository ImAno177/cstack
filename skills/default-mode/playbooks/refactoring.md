### Refactoring

Change structure while holding behavior constant.

1. Pin the current behavior with the smallest existing observable check; do not add a test only for ceremony.
2. Name the missing structure and target shape before moving code.
3. Delete dead paths and one-use wrappers before adding a new layer.
4. Migrate all callers and delete the legacy path in the same change when the contract permits it.
5. Prove equivalence on the real artifact and report the reader-load improvement. If behavior changes, re-route to feature or bug fix.
