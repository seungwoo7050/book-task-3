.PHONY: help build test bench run migrate up down logs e2e smoke repro

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

build: ## Build the server binary
	mkdir -p ./bin
	cd ../go && go build -o ../problem/bin/server ./cmd/server

test: ## Run all tests
	cd ../go && go test ./... -v -count=1 -race

bench: ## Run benchmarks
	cd ../go && go test ./... -bench=. -benchmem

run: build ## Build and run the server
	./bin/server

migrate: ## Apply schema (requires running CockroachDB)
	cockroach sql --insecure --host=localhost:26257 < ../go/schema.sql

up: ## Start CockroachDB for runtime verification
	$(MAKE) -C ../go up

down: ## Stop CockroachDB
	$(MAKE) -C ../go down

logs: ## Show CockroachDB logs
	$(MAKE) -C ../go logs

e2e: ## Run DB-backed end-to-end tests
	$(MAKE) -C ../go e2e

smoke: ## Alias for runtime smoke verification
	$(MAKE) -C ../go smoke

repro: ## Run the full reproducibility verification
	$(MAKE) -C ../go repro
