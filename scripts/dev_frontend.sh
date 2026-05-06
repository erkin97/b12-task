#!/usr/bin/env bash
# Run the Vite dev server on http://localhost:5173.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT/web/frontend"
exec npm run dev
