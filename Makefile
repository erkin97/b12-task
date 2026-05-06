.PHONY: help setup backend frontend test lint up down

help:
	@echo "Targets:"
	@echo "  setup      Bootstrap the Python venv and install deps"
	@echo "  backend    Run the Django dev server on :8000"
	@echo "  frontend   Run the Vite dev server on :5173"
	@echo "  test       Run pytest"
	@echo "  lint       Run ruff check and format check"
	@echo "  up         docker compose up --build"
	@echo "  down       docker compose down"

setup:
	./scripts/bootstrap.sh

backend:
	./scripts/dev_backend.sh

frontend:
	./scripts/dev_frontend.sh

test:
	uv run pytest

lint:
	uv run ruff check . && uv run ruff format --check .

up:
	docker compose up --build

down:
	docker compose down
