.PHONY: help build test run run-relay run-consumer up down logs e2e smoke repro

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

build: ## Build all binaries
	mkdir -p ./bin
	cd ../go && go build -o ../problem/bin/relay ./cmd/relay
	cd ../go && go build -o ../problem/bin/consumer ./cmd/consumer

test: ## Run all tests
	cd ../go && go test ./... -v -count=1 -race

run-relay: build ## Run the outbox relay
	./bin/relay

run-consumer: build ## Run the Kafka consumer
	./bin/consumer

up: ## Start CockroachDB and Redpanda
	$(MAKE) -C ../go up

down: ## Stop local runtime dependencies
	$(MAKE) -C ../go down

logs: ## Show CockroachDB and Redpanda logs
	$(MAKE) -C ../go logs

e2e: ## Run DB+Kafka end-to-end tests
	$(MAKE) -C ../go e2e

smoke: ## Alias for runtime smoke verification
	$(MAKE) -C ../go smoke

repro: ## Run the full reproducibility verification
	$(MAKE) -C ../go repro
