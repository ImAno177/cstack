# cstack

`cstack` packages the installed local skills together with upstream `pstack` and Ponytail skills for ChatGPT, Codex, and compatible agent hosts.

## Data flow

`~/.agents/skills` is an optional local input. `source/local/skills` stores its synchronized snapshot. `source/upstream` stores the two upstream snapshots. `plugins/cstack/skills` is generated from both and is the installable plugin payload.

The generated plugin is rebuilt by GitHub Actions. The build workflow runs on pushes, pull requests, manual dispatches, and the `build-plugin` repository dispatch event. The upstream workflow runs daily, on manual dispatch, and on the `sync-upstream` repository dispatch event. It imports `cursor/plugins/pstack/skills` and `DietrichGebert/ponytail/skills` before rebuilding the plugin.

Test suites and test fixtures are excluded from synchronized sources and generated plugin payloads. Testing guidance documents remain available inside the relevant skills.

## Local synchronization

Run a one-time sync from the current Codex skills directory.

```powershell
python scripts/sync_skills.py --source "$env:USERPROFILE\.agents\skills" --destination source/local/skills
python scripts/build_plugin.py --source-root source --destination plugins/cstack/skills
python scripts/validate_plugin.py --root plugins/cstack
```

To watch local changes and push them automatically, run this from a trusted clone.

```powershell
pwsh -File scripts/watch-local-skills.ps1
```

The watcher only stages `source/local` and the generated plugin. It does not stage unrelated files.

## ChatGPT and Codex

Add the repository as a Git-backed marketplace, then install `cstack` from the plugin directory.

```powershell
codex plugin marketplace add ImAno177/cstack --ref main
codex plugin marketplace upgrade cstack
```

The ChatGPT desktop app and Codex use the portable `plugin.json` and `skills/` package. A refresh is still required after a new commit because the host controls plugin installation and trust.

## Grok Build and Grok Bot

This repository is a Grok marketplace. Its `.grok-plugin/marketplace.json` points to the installable `plugins/cstack` plugin, which contains the generated `skills/` payload and the Grok-specific manifest.

Install it with Grok Build:

```powershell
grok plugin marketplace add ImAno177/cstack
grok plugin install cstack --trust
```

Grok Bot uses the same installed plugin on its bot computer. Refresh the plugin from the Grok plugins/marketplace UI after a new release.

## Repository dispatch triggers

Send `repository_dispatch` with event type `sync-upstream` to import both upstream sources. Send `build-plugin` to rebuild without importing upstream sources. GitHub's `push` event remains the normal trigger for source changes.

## Other platforms

The canonical skill payload is the portable `plugins/cstack/skills` directory. Platform-specific marketplace files can point at that directory without changing the skills themselves. New adapters should live under `platforms/` and must not write into the generated plugin directly.
