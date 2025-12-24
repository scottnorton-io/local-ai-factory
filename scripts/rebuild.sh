#!/usr/bin/env bash
set -euo pipefail

# Rebuild all Local AI Factory images and restart the stack.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[rebuild] Stopping stack..."
./scripts/dev-down.sh || true

echo "[rebuild] Rebuilding images (no cache)..."
docker compose build --no-cache

echo "[rebuild] Starting stack..."
./scripts/dev-up.sh

echo "[rebuild] Done."
