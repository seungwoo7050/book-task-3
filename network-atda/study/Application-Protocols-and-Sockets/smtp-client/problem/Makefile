# SMTP Client — Makefile
#
# Usage:
#   make run-debug-server   Start a local SMTP debugging server
#   make run-client         Run the skeleton SMTP client
#   make run-solution       Run the solution SMTP client
#   make test               Run the automated test
#   make clean              Remove temporary files

PYTHON  := python3
HOST    := localhost
PORT    := 1025
SENDER  := alice@example.com
RCPT    := bob@example.com

.PHONY: run-debug-server run-client run-solution test clean help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

run-debug-server: ## Start a local SMTP debug server on port $(PORT)
	$(PYTHON) -m smtpd -n -c DebuggingServer $(HOST):$(PORT)

run-client: ## Run the skeleton SMTP client
	$(PYTHON) code/smtp_client_skeleton.py $(HOST) $(PORT) $(SENDER) $(RCPT)

run-solution: ## Run the solution SMTP client
	$(PYTHON) ../python/src/smtp_client.py $(HOST) $(PORT) $(SENDER) $(RCPT)

test: ## Run the test script with a temporary SMTP mock server
	@$(PYTHON) script/mock_smtp_server.py $(HOST) $(PORT) >/tmp/net_smtp_mock.log 2>&1 & \
	server_pid=$$!; \
	trap 'kill $$server_pid >/dev/null 2>&1 || true; wait $$server_pid >/dev/null 2>&1 || true' EXIT INT TERM; \
	sleep 0.5; \
	bash script/test_smtp.sh $(HOST) $(PORT)

clean: ## Remove temporary files
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete 2>/dev/null || true
