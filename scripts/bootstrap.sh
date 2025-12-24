#!/usr/bin/env bash
set -euo pipefail

# Bootstrap script for the Local AI Factory repo.
# - Creates data directories
# - Copies .env.example to .env (if missing)

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[bootstrap] Root directory: $ROOT_DIR"

# Create data directories
mkdir -p data/inbox data/logs data/briefs

echo "[bootstrap] Ensured data directories: data/inbox, data/logs, data/briefs"

# Copy .env.example to .env if .env does not exist
if [[ ! -f .env ]]; then
  if [[ -f .env.example ]]; then
    cp .env.example .env
    echo "[bootstrap] Created .env from .env.example"
  else
    echo "[bootstrap] WARNING: .env.example not found; .env was not created" >&2
  fi
else
  echo "[bootstrap] .env already exists; leaving as-is"
fi

echo "[bootstrap] Done."
