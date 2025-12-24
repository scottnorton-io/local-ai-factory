#!/usr/bin/env bash
set -euo pipefail

# Start the Local AI Factory stack via docker compose.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[dev-up] Starting Local AI Factory stack..."

docker compose up -d

echo "[dev-up] Stack is starting. Use 'docker compose ps' to see status."
