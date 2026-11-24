# Release process

All plugins share one version, set in `.cstack/catalog.json`. Claude Code pins installed users to the version in each plugin's `.claude-plugin/plugin.json`, so users receive skill changes only after the version changes.

## Checklist

1. Set the new `version` in `.cstack/catalog.json` and run `python scripts/build_manifests.py`. It rewrites every host manifest, the marketplaces, `skills.sh.json`, the Grok skill index, and each plugin's `LICENSE` copy.
2. Check `LICENSE` and [third-party notices](../THIRD_PARTY_NOTICES.md) for any skill adapted from another project.
3. Run the gate:

   ```sh
   python scripts/build_manifests.py --check
   python scripts/validate_plugin.py
   python scripts/validate_skill_stack.py
   python -m unittest discover -s tests -p 'test_*.py'
   ```

   Run `claude plugin validate plugins/<plugin>` for each plugin when Claude Code is installed; it checks the Claude manifests and component files more strictly than the Python validators.
4. Update `CHANGELOG.md`. Verify the install commands on each host you claim before you report it as supported.
5. Open a PR with the version change, review CI and the diff, then tag only the reviewed commit.

## Generated files

`scripts/build_manifests.py` owns these files; edit `.cstack/catalog.json` or the skills instead:

- Marketplaces: `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json` (Codex), `.grok-plugin/marketplace.json`, `.cursor-plugin/marketplace.json`, `skills.sh.json`
- Per plugin: `plugins/<plugin>/.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.grok-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `LICENSE`
- `.grok-plugin/plugin-index.json`, listing every skill and hook event

## Hooks

The hooks in `plugins/cstack/hooks/` enforce rules and inject the model's skill; none of them routes requests to skills. Run `python -m unittest tests.test_hooks` after changing a hook. Codex users must re-review changed hook scripts after an update.
