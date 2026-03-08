.PHONY: run build test clean healthcheck lint

# ─── Variables ──────────────────────────────────────────────
APP_NAME    := api
SRC_DIR     := ../go
CMD_DIR     := $(SRC_DIR)/cmd/api
BINARY      := ./bin/$(APP_NAME)
PORT        ?= 4000

# ─── Build & Run ────────────────────────────────────────────
build:
	@echo "Building $(APP_NAME)..."
	mkdir -p ./bin
	cd $(SRC_DIR) && go build -o ../problem/bin/$(APP_NAME) ./cmd/api

run:
	@echo "Starting $(APP_NAME) on port $(PORT)..."
	cd $(SRC_DIR) && PORT=$(PORT) ENV=development go run ./cmd/api

# ─── Test ───────────────────────────────────────────────────
test:
	@echo "Running tests..."
	cd $(SRC_DIR) && go test -v -race -count=1 ./...

test-cover:
	@echo "Running tests with coverage..."
	cd $(SRC_DIR) && go test -v -race -coverprofile=coverage.out ./...
	cd $(SRC_DIR) && go tool cover -html=coverage.out -o coverage.html

# ─── Helpers ────────────────────────────────────────────────
healthcheck:
	@curl -s http://localhost:$(PORT)/v1/healthcheck | python3 -m json.tool

lint:
	@cd $(SRC_DIR) && go vet ./...

clean:
	@rm -rf bin/
	@rm -f $(SRC_DIR)/coverage.out $(SRC_DIR)/coverage.html
