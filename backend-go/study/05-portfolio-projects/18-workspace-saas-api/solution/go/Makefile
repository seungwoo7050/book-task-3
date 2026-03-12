.PHONY: help up down wait-postgres wait-redis migrate seed run-api run-worker test test-race e2e smoke demo-capture repro

COMPOSE := docker compose -f docker-compose.yml
DATABASE_URL ?= postgres://postgres:postgres@localhost:54339/workspace_saas?sslmode=disable
REDIS_ADDR ?= localhost:6381
PORT ?= 4080
APP_ENV ?= development
JWT_SECRET ?= workspace-saas-secret
WORKER_POLL_INTERVAL ?= 250ms

help: ## Show available commands
	@grep -E '^[a-zA-Z0-9_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

up: ## Start Postgres and Redis containers
	$(COMPOSE) up -d postgres redis
	$(MAKE) wait-postgres
	$(MAKE) wait-redis

down: ## Stop local infrastructure
	$(COMPOSE) down

wait-postgres: ## Wait until Postgres is ready
	@until $(COMPOSE) exec -T postgres pg_isready -U postgres -d workspace_saas >/dev/null 2>&1; do \
		echo "waiting for postgres..."; \
		sleep 1; \
	done
	@echo "postgres is ready"

wait-redis: ## Wait until Redis is ready
	@until $(COMPOSE) exec -T redis redis-cli ping | grep -q PONG; do \
		echo "waiting for redis..."; \
		sleep 1; \
	done
	@echo "redis is ready"

migrate: up ## Apply SQL migrations
	DATABASE_URL="$(DATABASE_URL)" go run ./cmd/migrate up

seed: up ## Apply idempotent seed SQL
	DATABASE_URL="$(DATABASE_URL)" go run ./cmd/migrate seed

run-api: ## Run the HTTP API against local dependencies
	PORT="$(PORT)" APP_ENV="$(APP_ENV)" DATABASE_URL="$(DATABASE_URL)" REDIS_ADDR="$(REDIS_ADDR)" JWT_SECRET="$(JWT_SECRET)" go run ./cmd/api

run-worker: ## Run the notification worker against local dependencies
	APP_ENV="$(APP_ENV)" DATABASE_URL="$(DATABASE_URL)" REDIS_ADDR="$(REDIS_ADDR)" JWT_SECRET="$(JWT_SECRET)" WORKER_POLL_INTERVAL="$(WORKER_POLL_INTERVAL)" go run ./cmd/worker

test: ## Run unit tests
	go test ./... -count=1

test-race: ## Run race-detector tests
	go test -race ./... -count=1

e2e: migrate seed ## Run database and Redis backed end-to-end tests
	DATABASE_URL="$(DATABASE_URL)" REDIS_ADDR="$(REDIS_ADDR)" JWT_SECRET="$(JWT_SECRET)" go test -tags=e2e ./e2e -v -count=1

smoke: migrate seed ## Run curl-based smoke scenario against local API and worker
	PORT="$(PORT)" DATABASE_URL="$(DATABASE_URL)" REDIS_ADDR="$(REDIS_ADDR)" JWT_SECRET="$(JWT_SECRET)" WORKER_POLL_INTERVAL="$(WORKER_POLL_INTERVAL)" ./scripts/smoke.sh

demo-capture: migrate seed ## Generate presentation capture artifacts from a real demo run
	PORT="$(PORT)" DATABASE_URL="$(DATABASE_URL)" REDIS_ADDR="$(REDIS_ADDR)" JWT_SECRET="$(JWT_SECRET)" WORKER_POLL_INTERVAL="$(WORKER_POLL_INTERVAL)" ./scripts/demo_capture.sh

repro: up ## Full local reproducibility check
	$(MAKE) migrate
	$(MAKE) seed
	$(MAKE) test
	$(MAKE) test-race
	$(MAKE) e2e
	$(MAKE) smoke
