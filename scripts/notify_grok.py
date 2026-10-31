from __future__ import annotations

import argparse
import json
import os
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--sha", required=True)
    parser.add_argument("--release-url", required=True)
    args = parser.parse_args()
    url = os.environ["GROK_BOT_WEBHOOK_URL"]
    key = os.environ["GROK_BOT_WEBHOOK_KEY"]
    body = json.dumps({
        "event": args.event,
        "repository": args.repository,
        "commit": args.sha,
        "release_url": args.release_url,
    }).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
            "X-Automation-Key": key,
        },
    )
    with urllib.request.urlopen(request, timeout=8) as response:
        if response.status < 200 or response.status >= 300:
            raise RuntimeError(f"Grok webhook returned {response.status}")
    print("Grok Bot notified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
