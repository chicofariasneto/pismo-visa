# Pismo Visa API

REST API for account and transaction management built with FastAPI and PostgreSQL.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check (validates DB connection) |
| `POST` | `/api/v1/accounts/` | Create an account |
| `GET` | `/api/v1/accounts/{account_id}` | Get account by ID |
| `POST` | `/api/v1/transactions/` | Create a transaction |

Interactive docs available at `http://localhost:8000/docs` when running.

## Running the API

The only requirement is **Docker**.

```bash
cp .env.example .env
make stack-up
```

This builds the image, starts Postgres, runs database migrations, and starts the API on port `8000`.

```bash
make stack-down   # stop everything
```

## Development

Requires Python 3.12+ and [Poetry](https://python-poetry.org).

```bash
cp .env.example .env
make install      # install dependencies
make db-up        # start Postgres + run migrations
make dev          # start API with hot reload on :8000
```

## Commands

```
make                # show all available commands
make test           # unit tests (no DB needed)
make test-db-up     # start test DB on port 5433
make test-int       # integration tests
make test-all       # unit + integration
make load-test      # k6 load test (requires stack-up first)
make lint           # ruff checks
make format         # auto-fix lint/format
make db-info        # show Flyway migration status
```

## Environment variables

Copy `.env.example` to `.env` and adjust as needed.

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_USER` | `postgres` | Database user |
| `POSTGRES_PASSWORD` | `postgres` | Database password |
| `POSTGRES_HOST` | `localhost` | Database host |
| `POSTGRES_PORT` | `5432` | Database port |
| `POSTGRES_DB` | `pismo_visa` | Database name |
| `DEBUG` | `false` | Enable SQLAlchemy query logging |
