# Web Proxy — Makefile
#
# Usage:
#   make run-proxy          Start the skeleton proxy
#   make run-solution       Start the solution proxy
#   make test               Run the automated test (proxy must be running)
#   make request            Send a test request through the proxy
#   make clean              Remove cache and temporary files

PYTHON := python3
PORT   := 8888
TEST_URL := http://www.example.com/

.PHONY: run-proxy run-solution test request clean help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

run-proxy: ## Start the skeleton proxy on port $(PORT)
	$(PYTHON) code/proxy_skeleton.py $(PORT)

run-solution: ## Start the solution proxy on port $(PORT)
	$(PYTHON) ../python/src/web_proxy.py $(PORT)

test: ## Run the test script with a temporary solution proxy
	@$(PYTHON) ../python/src/web_proxy.py $(PORT) >/tmp/net_web_proxy.log 2>&1 & \
	proxy_pid=$$!; \
	trap 'kill $$proxy_pid >/dev/null 2>&1 || true; wait $$proxy_pid >/dev/null 2>&1 || true' EXIT INT TERM; \
	sleep 0.5; \
	bash script/test_proxy.sh $(PORT)

request: ## Send a test request through the proxy
	curl -v -x http://localhost:$(PORT) $(TEST_URL)

clean: ## Remove cache and temporary files
	rm -rf cache/
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete 2>/dev/null || true
