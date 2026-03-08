# Traceroute — Makefile
#
# Usage:
#   make run-client HOST=8.8.8.8   Run the live traceroute implementation (requires sudo)
#   make test                      Run the non-privileged unit checks
#   make clean                     Remove temporary files

PYTHON := python3
HOST := 8.8.8.8
MAX_HOPS := 8
PROBES := 3
TIMEOUT := 1.0

.PHONY: run-client test clean help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

run-client: ## Run the live traceroute implementation (requires sudo on most systems)
	sudo $(PYTHON) ../python/src/traceroute.py $(HOST) --max-hops $(MAX_HOPS) --probes $(PROBES) --timeout $(TIMEOUT)

test: ## Run parser, formatting, and synthetic route integration tests
	PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 $(PYTHON) -m pytest -q ../python/tests

clean: ## Remove temporary files
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete 2>/dev/null || true
