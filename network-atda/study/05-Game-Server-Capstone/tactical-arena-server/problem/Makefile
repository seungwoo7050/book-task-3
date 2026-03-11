# Tactical Arena Server — Makefile
#
# Usage:
#   make test
#   make run-server
#   make run-bot-demo
#   make load-test
#   make clean

CMAKE := cmake
PYTHON := python3
CPP_DIR := ../cpp
BUILD_DIR := ../cpp/build
DB_PATH := data/arena.sqlite3
TCP_PORT := 39001
UDP_PORT := 39002
THREADS := 4
MATCH_DURATION_MS := 90000
RESUME_WINDOW_MS := 20000

.PHONY: configure build test run-server run-bot-demo load-test clean help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

configure: ## Configure the CMake build directory
	$(CMAKE) -S $(CPP_DIR) -B $(BUILD_DIR)

build: configure ## Build the project binaries
	$(CMAKE) --build $(BUILD_DIR)

test: build ## Run CTest, integration checks, and load smoke
	ctest --test-dir $(BUILD_DIR) --output-on-failure
	$(PYTHON) script/integration_test.py $(BUILD_DIR)
	$(PYTHON) script/load_smoke_test.py $(BUILD_DIR)

run-server: build ## Run the arena server with default local ports
	$(BUILD_DIR)/arena_server \
		--tcp-port $(TCP_PORT) \
		--udp-port $(UDP_PORT) \
		--db-path $(DB_PATH) \
		--thread-count $(THREADS) \
		--match-duration-ms $(MATCH_DURATION_MS) \
		--resume-window-ms $(RESUME_WINDOW_MS)

run-bot-demo: build ## Launch a short local demo with two bots
	bash script/run_bot_demo.sh $(BUILD_DIR)

load-test: build ## Run the scripted load smoke with local server
	$(PYTHON) script/load_smoke_test.py $(BUILD_DIR)

clean: ## Remove build outputs and temporary sqlite files
	rm -rf $(BUILD_DIR)
	rm -f data/*.sqlite3
