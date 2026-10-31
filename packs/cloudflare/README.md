# Optional pack: Cloudflare

These skills are not in the core `skills/` catalog or `.grok-plugin/plugin-index.json`.
Enable them when you need Cloudflare Workers, Wrangler, Durable Objects, Email,
Zero Trust, Turnstile, Agents SDK, the sandbox SDK, or web performance.

## Skills

- `agents-sdk`
- `cloudflare`
- `cloudflare-email-service`
- `cloudflare-one`
- `cloudflare-one-migrations`
- `durable-objects`
- `sandbox-sdk`
- `turnstile-spin`
- `workers-best-practices`
- `wrangler`
- `web-perf`

## Enable

From the repository root, copy or symlink into `skills/`:

```bash
ln -s ../packs/cloudflare/skills/wrangler skills/wrangler
```

Copy every skill in the pack:

```bash
cp -R packs/cloudflare/skills/. skills/
```

Or point the host at `packs/cloudflare/skills` in addition to core `skills/`.

After a copy or symlink into `skills/`, regenerate the Grok index if you want
those skills listed:

```bash
python scripts/generate_grok_plugin_index.py
```
