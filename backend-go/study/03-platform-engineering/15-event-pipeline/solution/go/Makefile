.PHONY: help up down logs wait-db wait-kafka migrate reset-schema build run-relay run-consumer test test-race e2e smoke repro

COMPOSE := docker compose -p event-pipeline -f docker-compose.yml
DATABASE_URL ?= postgresql://root@localhost:26258/defaultdb?sslmode=disable
KAFKA_BROKER ?= localhost:9093
KAFKA_TOPIC ?= game.purchases

help: ## Show available commands
	@grep -E '^[a-zA-Z0-9_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

up: ## Start CockroachDB and Redpanda
	$(COMPOSE) up -d db kafka
	$(MAKE) wait-db
	$(MAKE) wait-kafka

down: ## Stop containers
	$(COMPOSE) down -v

logs: ## Show service logs
	$(COMPOSE) logs -f db kafka

wait-db: ## Wait until CockroachDB is ready
	@until $(COMPOSE) exec -T db cockroach sql --insecure --host=localhost:26258 -e "select 1" >/dev/null 2>&1; do \
		echo "waiting for db..."; \
		sleep 1; \
	done
	@echo "db is ready"

wait-kafka: ## Wait until Redpanda is ready
	@until $(COMPOSE) exec -T kafka rpk cluster info >/dev/null 2>&1; do \
		echo "waiting for kafka..."; \
		sleep 1; \
	done
	@echo "kafka is ready"

migrate: up ## Apply schema.sql to CockroachDB
	$(COMPOSE) exec -T db sh -lc "cockroach sql --insecure --host=localhost:26258 < /workspace/schema.sql"

reset-schema: up ## Drop and recreate the public schema, then apply schema.sql
	$(COMPOSE) exec -T db cockroach sql --insecure --host=localhost:26258 -e "DROP SCHEMA IF EXISTS public CASCADE; CREATE SCHEMA public;"
	$(COMPOSE) exec -T db sh -lc "cockroach sql --insecure --host=localhost:26258 < /workspace/schema.sql"

build: ## Build relay and consumer binaries
	mkdir -p ./bin
	go build -o ./bin/relay ./cmd/relay
	go build -o ./bin/consumer ./cmd/consumer

run-relay: ## Run the relay against local CockroachDB and Redpanda
	DATABASE_URL="$(DATABASE_URL)" KAFKA_BROKER="$(KAFKA_BROKER)" KAFKA_TOPIC="$(KAFKA_TOPIC)" go run ./cmd/relay

run-consumer: ## Run the consumer against local CockroachDB and Redpanda
	DATABASE_URL="$(DATABASE_URL)" KAFKA_BROKER="$(KAFKA_BROKER)" KAFKA_TOPIC="$(KAFKA_TOPIC)" go run ./cmd/consumer

test: ## Run unit tests
	go test ./... -count=1

test-race: ## Run unit tests with race detector
	go test -race ./... -count=1

e2e: migrate ## Run DB+Kafka end-to-end tests
	RUN_E2E=1 DATABASE_URL="$(DATABASE_URL)" KAFKA_BROKER="$(KAFKA_BROKER)" KAFKA_TOPIC="$(KAFKA_TOPIC)" go test ./e2e -v -count=1

smoke: e2e ## Alias for runtime smoke verification

repro: test-race e2e ## Full reproducibility verification
