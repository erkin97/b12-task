#!/usr/bin/env bash
# Bootstrap the venv with uv (Python) and install npm deps for the frontend.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

if ! command -v uv >/dev/null 2>&1; then
  echo "[bootstrap] uv not found. Install: https://docs.astral.sh/uv/getting-started/installation/" >&2
  exit 1
fi

echo "[bootstrap] Creating venv at .venv"
uv venv

echo "[bootstrap] Installing Python deps (CLI, dev, backend)"
uv pip install -e ".[dev,backend]"

if command -v npm >/dev/null 2>&1; then
  echo "[bootstrap] Installing npm deps in web/frontend"
  (cd web/frontend && npm install)
else
  echo "[bootstrap] npm not found, skipping frontend install"
fi

echo
echo "[bootstrap] Done."
