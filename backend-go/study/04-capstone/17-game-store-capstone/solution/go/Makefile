.PHONY: help up down logs wait-db migrate reset-schema run test test-race e2e repro

COMPOSE := docker compose -f docker-compose.yml
DATABASE_URL ?= postgresql://postgres:postgres@localhost:54329/game_store?sslmode=disable

help: ## Show available commands
	@grep -E '^[a-zA-Z0-9_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

up: ## Start PostgreSQL container
	$(COMPOSE) up -d db
	$(MAKE) wait-db

down: ## Stop containers
	$(COMPOSE) down

logs: ## Show DB container logs
	$(COMPOSE) logs -f db

wait-db: ## Wait until PostgreSQL is ready
	@until $(COMPOSE) exec -T db pg_isready -U postgres -d game_store >/dev/null 2>&1; do \
		echo "waiting for db..."; \
		sleep 1; \
	done
	@echo "db is ready"

migrate: up ## Apply schema.sql to DB
	$(COMPOSE) exec -T db psql -U postgres -d game_store -f /workspace/schema.sql

reset-schema: up ## Drop/recreate public schema and re-apply schema.sql
	$(COMPOSE) exec -T db psql -U postgres -d game_store -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	$(COMPOSE) exec -T db psql -U postgres -d game_store -f /workspace/schema.sql

run: ## Run API server against local compose DB
	DATABASE_URL="$(DATABASE_URL)" go run ./cmd/api

test: ## Run unit tests
	go test ./... -count=1

test-race: ## Run tests with race detector
	go test -race ./... -count=1

e2e: migrate ## Run reproducible DB-backed end-to-end tests
	DATABASE_URL="$(DATABASE_URL)" go test ./e2e -v -count=1

repro: test-race e2e ## Full reproducibility verification
