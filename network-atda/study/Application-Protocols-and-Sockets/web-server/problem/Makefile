# Web Server — Makefile
# Usage:
#   make run-server         Start the web server (skeleton)
#   make run-solution       Start the web server (solution)
#   make test               Run the automated test script
#   make request            Send a test HTTP request with curl
#   make clean              Remove temporary files

PYTHON   := python3
PORT     := 6789
HOST     := localhost
DATA_DIR := data

.PHONY: run-server run-solution test request clean help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

run-server: ## Start the skeleton web server on port $(PORT)
	cd $(DATA_DIR) && $(PYTHON) ../code/server_skeleton.py $(PORT)

run-solution: ## Start the solution web server on port $(PORT)
	cd $(DATA_DIR) && $(PYTHON) ../../python/src/web_server.py $(PORT)

test: ## Run the test script with a temporary solution server
	@(cd $(DATA_DIR) && $(PYTHON) ../../python/src/web_server.py $(PORT) >/tmp/net_web_server.log 2>&1) & \
	server_pid=$$!; \
	trap 'kill $$server_pid >/dev/null 2>&1 || true; wait $$server_pid >/dev/null 2>&1 || true' EXIT INT TERM; \
	sleep 0.5; \
	bash script/test_server.sh $(HOST) $(PORT)

request: ## Send a single test GET request
	curl -v http://$(HOST):$(PORT)/hello.html

clean: ## Remove temporary / generated files
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete 2>/dev/null || true
