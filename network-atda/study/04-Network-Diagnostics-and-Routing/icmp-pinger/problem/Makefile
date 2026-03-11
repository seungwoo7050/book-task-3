# ICMP Pinger — Makefile
#
# Usage:
#   sudo make run-client HOST=google.com
#   sudo make run-solution HOST=google.com
#   make test
#   sudo make test-live HOST=google.com
#   make clean

PYTHON := python3
HOST   := google.com
COUNT  := 4

.PHONY: run-client run-solution test test-live clean help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

run-client: ## Run the skeleton ICMP pinger (requires sudo)
	sudo $(PYTHON) code/icmp_pinger_skeleton.py $(HOST) -c $(COUNT)

run-solution: ## Run the solution ICMP pinger (requires sudo)
	sudo $(PYTHON) ../python/src/icmp_pinger.py $(HOST) -c $(COUNT)

test: ## Run deterministic ICMP tests without raw sockets
	PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 $(PYTHON) -m pytest -q ../python/tests

test-live: ## Run the live raw-socket ICMP check (requires sudo)
	@if [ "$$(id -u)" -ne 0 ]; then \
		echo "[SKIP] ICMP raw-socket test requires root privileges."; \
		echo "       Run: sudo make test-live HOST=$(HOST)"; \
	else \
		bash script/test_icmp.sh $(HOST); \
	fi

clean: ## Remove temporary files
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete 2>/dev/null || true
