.DEFAULT_GOAL := help

.PHONY: help install dev lint format \
        test test-cov test-int test-all \
        test-db-up test-db-down test-db-logs \
        db-up db-down db-down-v db-logs db-migrate db-info \
        api-build api-up api-down api-logs \
        stack-up stack-down stack-logs \
        load-test

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

# ── Local dev ──────────────────────────────────────────────────────────────
install: ## Install all dependencies via Poetry
	poetry install

dev: ## Start dev server with hot reload (requires DB running)
	poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

lint: ## Run ruff linter and format checks
	poetry run ruff check .
	poetry run ruff format --check .

format: ## Auto-fix lint and format issues
	poetry run ruff check --fix .
	poetry run ruff format .

# ── Tests ──────────────────────────────────────────────────────────────────
test: ## Run unit tests (no DB required)
	poetry run pytest tests/unit -v

test-cov: ## Run unit tests with coverage report
	poetry run pytest tests/unit --cov=app --cov-report=term-missing -v

test-int: ## Run integration tests (requires test DB — run make test-db-up first)
	poetry run pytest tests/integration -v

test-all: ## Run unit + integration tests
	poetry run pytest tests/ -v

# ── Test database (docker-compose.test.yml) ────────────────────────────────
test-db-up: ## Start test DB on port 5433 and run migrations
	docker compose -f docker-compose.test.yml up -d

test-db-down: ## Stop test DB
	docker compose -f docker-compose.test.yml down

test-db-logs: ## Tail test DB logs
	docker compose -f docker-compose.test.yml logs -f

# ── Database + migrations (docker-compose.db.yml) ─────────────────────────
db-up: ## Start Postgres and run Flyway migrations
	docker compose -f docker-compose.db.yml up -d

db-down: ## Stop DB services
	docker compose -f docker-compose.db.yml down

db-down-v: ## Stop DB services and remove volumes
	docker compose -f docker-compose.db.yml down -v

db-logs: ## Tail DB and Flyway logs
	docker compose -f docker-compose.db.yml logs -f

db-migrate: ## Run Flyway migrate manually
	docker compose -f docker-compose.db.yml run --rm flyway migrate

db-info: ## Show Flyway migration status
	docker compose -f docker-compose.db.yml run --rm flyway info

# ── API (docker-compose.api.yml) ──────────────────────────────────────────
api-build: ## Build the API Docker image
	docker compose -f docker-compose.api.yml build

api-up: ## Start the API container
	docker compose -f docker-compose.api.yml up -d

api-down: ## Stop the API container
	docker compose -f docker-compose.api.yml down

api-logs: ## Tail API container logs
	docker compose -f docker-compose.api.yml logs -f api

# ── Full stack (Docker only — no local Python/Poetry needed) ───────────────
stack-up: ## Build and start the full stack (DB + API) using Docker
	docker compose -f docker-compose.db.yml up -d
	docker compose -f docker-compose.api.yml build
	docker compose -f docker-compose.api.yml up -d

stack-down: ## Stop the full stack
	docker compose -f docker-compose.api.yml down
	docker compose -f docker-compose.db.yml down

stack-logs: ## Tail logs from all services
	docker compose -f docker-compose.db.yml logs -f &
	docker compose -f docker-compose.api.yml logs -f

# ── Load test ──────────────────────────────────────────────────────────────
load-test: ## Run k6 load test (API on host: make load-test, Docker stack: BASE_URL=http://api:8000 make load-test)
	docker compose -f docker-compose.k6.yml run --rm k6
