# Release and upstream update process

## Updating managed upstream skills

- The weekly `sync-upstream-skills` workflow checks out upstream repositories and copies **only** destinations listed in `.cstack/upstreams.json`.
- The updater rejects path traversal, overlapping destinations, and symlinks. Each replacement stages content first and retains the old tree for rollback.
- A successful sync writes `.cstack/upstreams.lock.json`, recording each upstream's commit SHA, source coordinates, and SHA-256 digest of the vendored tree. The first successful run bootstraps the lockfile.
- Run `python scripts/sync_upstream_skills.py --check` to compare vendored content with the lock **without network access** after the lock exists; before it exists, the command compares with live upstream branches.
- The workflow creates a new `automation/upstream-sync-<run-id>` branch and a PR. It will not force-push or update `main`. If an earlier automation PR is open, the workflow skips creating another; review/close the previous PR before running again.
- Review the diff, source SHA changes, and any new executable instructions or third-party licensing. Merge only after validation and independent review.

**Required GitHub setting:** The repository's Actions permissions must allow the workflow token to create pull requests. If GitHub returns `Resource not accessible by integration`, enable the applicable repository/organization Actions PR permission, or provide an appropriately scoped bot token. Do not work around this by enabling direct pushes to `main`.

## Release checklist

1. Update the version consistently in `plugin.json`, `.codex-plugin/plugin.json`, `.grok-plugin/plugin.json`, and `.claude-plugin/marketplace.json`.
2. Check `LICENSE`, [third-party notices](../THIRD_PARTY_NOTICES.md), and changes to all upstream-vendored files. The root MIT license does not override upstream licenses.
3. Run:

   ```sh
   python scripts/validate_plugin.py --root .
   python scripts/validate_skill_stack.py --source-root . --plugin-root . --policy .cstack/skill-policy.json
   python scripts/generate_grok_plugin_index.py --check
   ```

4. Update `CHANGELOG.md` and release notes. Verify marketplace install instructions on the target host before claiming platform compatibility; declared support alone does not prove installation or hook execution.
5. Open a PR with the version and index changes, review CI and the diff, then tag/release only the reviewed commit.

## Plugin entrypoints

- Codex: `.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json`
- Grok: `.grok-plugin/plugin.json`, `.grok-plugin/marketplace.json`, generated `.grok-plugin/plugin-index.json`
- Claude Code: `.claude-plugin/marketplace.json`
- Shared hooks: `hooks/hooks.json` (requires Node.js on the executing host)

The router normally injects a short session bootstrap; set `CSTACK_ROUTER_MODE=full` to compare with the older behavior. See [routing benchmark](routing-benchmark.md). Host installation and lifecycle behavior remain to be verified by maintainers on real clients; this change intentionally does not introduce the separate compatibility test PR.
