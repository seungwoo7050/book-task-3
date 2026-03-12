.PHONY: help build test bench run migrate up down logs e2e smoke repro

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

build: ## Build the server binary
	mkdir -p ./bin
	cd ../solution/go && go build -o ../problem/bin/server ./cmd/server

test: ## Run all tests
	cd ../solution/go && go test ./... -v -count=1 -race

bench: ## Run benchmarks
	cd ../solution/go && go test ./... -bench=. -benchmem

run: build ## Build and run the server
	./bin/server

migrate: ## Apply schema (requires running CockroachDB)
	cockroach sql --insecure --host=localhost:26257 < ../solution/go/schema.sql

up: ## Start CockroachDB for runtime verification
	$(MAKE) -C ../solution/go up

down: ## Stop CockroachDB
	$(MAKE) -C ../solution/go down

logs: ## Show CockroachDB logs
	$(MAKE) -C ../solution/go logs

e2e: ## Run DB-backed end-to-end tests
	$(MAKE) -C ../solution/go e2e

smoke: ## Alias for runtime smoke verification
	$(MAKE) -C ../solution/go smoke

repro: ## Run the full reproducibility verification
	$(MAKE) -C ../solution/go repro
