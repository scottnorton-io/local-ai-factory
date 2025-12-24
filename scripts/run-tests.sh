#!/usr/bin/env bash
set -euo pipefail

# Run unit, integration, and evaluation smoke tests for Local AI Factory.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

export PYTHONPATH="$ROOT_DIR:${PYTHONPATH:-}"

echo "[tests] Running unit tests..."
pytest tests/unit

echo "[tests] Running integration tests..."
pytest tests/integration

echo "[tests] Running evaluation smoke tests..."
python tests/evaluation/run_eval.py --suite smoke || {
  echo "[tests] Evaluation suite reported failures" >&2
  exit 1
}

echo "[tests] All test suites completed."
