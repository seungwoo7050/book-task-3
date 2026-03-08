# UDP Pinger — Makefile
#
# Usage:
#   make run-server         Start the UDP ping server
#   make run-client         Run the skeleton ping client
#   make run-solution       Run the solution ping client
#   make test               Run the automated test
#   make clean              Remove temporary files

PYTHON := python3
HOST   := 127.0.0.1
PORT   := 12000

.PHONY: run-server run-client run-solution test clean help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

run-server: ## Start the UDP ping server on port $(PORT)
	$(PYTHON) code/udp_pinger_server.py $(PORT)

run-client: ## Run the skeleton ping client
	$(PYTHON) code/udp_pinger_client_skeleton.py $(HOST) $(PORT)

run-solution: ## Run the solution ping client
	$(PYTHON) ../python/src/udp_pinger_client.py $(HOST) $(PORT)

test: ## Run the test script with a temporary UDP server
	@$(PYTHON) code/udp_pinger_server.py $(PORT) >/tmp/net_udp_server.log 2>&1 & \
	server_pid=$$!; \
	trap 'kill $$server_pid >/dev/null 2>&1 || true; wait $$server_pid >/dev/null 2>&1 || true' EXIT INT TERM; \
	sleep 0.5; \
	bash script/test_pinger.sh $(HOST) $(PORT)

clean: ## Remove temporary files
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete 2>/dev/null || true
