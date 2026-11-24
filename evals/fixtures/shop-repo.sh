#!/usr/bin/env bash
# Builds a small, realistic Git repository in the current directory so routing
# prompts that mention a codebase have something to look at.
set -euo pipefail

git init -q -b main .
git config user.name "Dev"
git config user.email "dev@example.com"

mkdir -p shop/payments shop/web tests docs

cat > README.md <<'EOF'
# shop-api

Order, cart, and payment service for the storefront. Python 3.12, Flask.

    pip install -e . && pytest
EOF

cat > AGENTS.md <<'EOF'
# Agent notes

- Run `pytest` before committing.
- Use conventional commits.
EOF

cat > pyproject.toml <<'EOF'
[project]
name = "shop-api"
version = "1.4.0"
dependencies = ["flask>=3", "requests>=2.32"]
EOF

cat > shop/__init__.py <<'EOF'
EOF

cat > shop/config.py <<'EOF'
import json
from pathlib import Path


def parse_config(path: str) -> dict:
    return json.loads(Path(path).read_text())
EOF

cat > shop/cart.py <<'EOF'
def total(items, discount_code=None, free_shipping=False):
    subtotal = sum(i["price"] * i["qty"] for i in items)
    if discount_code == "SAVE10":
        subtotal *= 0.9
    shipping = 0 if free_shipping else 4.99
    if discount_code and free_shipping:
        shipping = 4.99
    return round(subtotal + shipping, 2)
EOF

cat > shop/text.py <<'EOF'
import re


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower().encode("ascii", "ignore").decode()).strip("-")
EOF

cat > shop/http.py <<'EOF'
import requests

DEFAULT_TIMEOUT = 30


def get(url, **kwargs):
    return requests.get(url, timeout=kwargs.pop("timeout", DEFAULT_TIMEOUT), **kwargs)
EOF

cat > shop/payments/stripe_client.py <<'EOF'
from shop import http


def charge(customer_id, cents):
    return http.get(f"https://api.stripe.example/charge?c={customer_id}&a={cents}")
EOF

cat > shop/webhooks.py <<'EOF'
import time

from shop import http

MAX_RETRIES = 7
MAX_DELAY = 90


def send(url, payload):
    for attempt in range(MAX_RETRIES):
        response = http.get(url, params=payload)
        if response.ok:
            return True
        time.sleep(min(2 ** attempt, MAX_DELAY))
    return False
EOF

cat > shop/web/app.py <<'EOF'
from flask import Flask, request

from shop import cart

app = Flask(__name__)
SECRET_KEY = "dev-secret-123"


@app.post("/cart/total")
def cart_total():
    body = request.get_json()
    return {"total": cart.total(body["items"], body.get("code"), body.get("free_shipping", False))}


@app.get("/orders")
def orders():
    user = request.args["user"]
    query = f"SELECT * FROM orders WHERE user = '{user}'"
    return {"query": query}
EOF

cat > tests/test_cart.py <<'EOF'
from shop.cart import total


def test_total_without_discount():
    assert total([{"price": 10, "qty": 2}]) == 24.99
EOF

cat > docs/architecture.md <<'EOF'
# Architecture

The API (`shop/web`) calls the cart and payment modules. Webhooks notify partners after payment.
EOF

git add -A
git commit -q -m "feat: initial shop api"

cat >> shop/webhooks.py <<'EOF'


def backoff(attempt):
    return min(2 ** attempt, MAX_DELAY)
EOF
git commit -qam "fix(webhooks): cap retry delay at 90s after partner outage (see #212)"

git checkout -q -b feat/webhook-retries
cat > shop/webhooks.py <<'EOF'
import random
import time

from shop import http

MAX_RETRIES = 7
MAX_DELAY = 90


def backoff(attempt):
    return min(2 ** attempt + random.random(), MAX_DELAY)


def send(url, payload, idempotency_key=None):
    for attempt in range(MAX_RETRIES + 1):
        response = http.get(url, params=payload)
        if response.status_code < 500:
            return response.ok
        time.sleep(backoff(attempt))
    return False
EOF
git commit -qam "feat(webhooks): add jitter and idempotency key to retries"
git checkout -q main
git checkout -q feat/webhook-retries
