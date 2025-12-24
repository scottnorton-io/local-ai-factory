#!/usr/bin/env bash
set -euo pipefail

# Run tests inside the Docker "tests" service container.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[tests] Building tests image..."
docker compose build tests

echo "[tests] Running tests in container..."
docker compose run --rm tests

echo "[tests] Done."
