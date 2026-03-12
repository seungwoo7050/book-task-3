.PHONY: help up down logs wait-db migrate reset-schema build run test test-race e2e smoke repro

COMPOSE := docker compose -p cockroach-tx -f docker-compose.yml
DATABASE_URL ?= postgresql://root@localhost:26257/defaultdb?sslmode=disable
ADDR ?= :8080

help: ## Show available commands
	@grep -E '^[a-zA-Z0-9_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

up: ## Start CockroachDB
	$(COMPOSE) up -d db
	$(MAKE) wait-db

down: ## Stop containers
	$(COMPOSE) down -v

logs: ## Show CockroachDB logs
	$(COMPOSE) logs -f db

wait-db: ## Wait until CockroachDB is ready
	@until $(COMPOSE) exec -T db cockroach sql --insecure --host=localhost:26258 -e "select 1" >/dev/null 2>&1; do \
		echo "waiting for db..."; \
		sleep 1; \
	done
	@echo "db is ready"

migrate: up ## Apply schema.sql to CockroachDB
	$(COMPOSE) exec -T db sh -lc "cockroach sql --insecure --host=localhost:26258 < /workspace/schema.sql"

reset-schema: up ## Drop and recreate the public schema, then apply schema.sql
	$(COMPOSE) exec -T db cockroach sql --insecure --host=localhost:26258 -e "DROP SCHEMA IF EXISTS public CASCADE; CREATE SCHEMA public;"
	$(COMPOSE) exec -T db sh -lc "cockroach sql --insecure --host=localhost:26258 < /workspace/schema.sql"

build: ## Build the server binary
	mkdir -p ./bin
	go build -o ./bin/server ./cmd/server

run: ## Run the HTTP server against local CockroachDB
	DATABASE_URL="$(DATABASE_URL)" ADDR="$(ADDR)" go run ./cmd/server

test: ## Run unit tests
	go test ./... -count=1

test-race: ## Run unit tests with race detector
	go test -race ./... -count=1

e2e: migrate ## Run DB-backed end-to-end tests
	RUN_E2E=1 DATABASE_URL="$(DATABASE_URL)" go test ./e2e -v -count=1

smoke: e2e ## Alias for runtime smoke verification

repro: test-race e2e ## Full reproducibility verification
