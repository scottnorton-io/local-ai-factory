#!/usr/bin/env bash
set -euo pipefail

# Stop the Local AI Factory stack via docker compose.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[dev-down] Stopping Local AI Factory stack..."

docker compose down

echo "[dev-down] Stack stopped."
