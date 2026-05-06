#!/usr/bin/env bash
# Run the Django dev server on http://localhost:8000.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT/web/backend"
exec uv run python manage.py runserver 0.0.0.0:8000
