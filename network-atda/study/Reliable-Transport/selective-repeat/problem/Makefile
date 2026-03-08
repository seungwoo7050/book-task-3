# Selective Repeat — Makefile
#
# Usage:
#   make run-skeleton         Run the provided skeleton
#   make run-solution         Run the completed Selective Repeat implementation
#   make test                 Run the automated verification script
#   make clean                Remove temporary files

PYTHON := python3
LOSS_RATE := 0.2
CORRUPT_RATE := 0.1
WINDOW := 4

.PHONY: run-skeleton run-solution test clean help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

run-skeleton: ## Run the Selective Repeat skeleton
	PYTHONPATH=code $(PYTHON) code/selective_repeat_skeleton.py --loss $(LOSS_RATE) --corrupt $(CORRUPT_RATE) --window $(WINDOW)

run-solution: ## Run the Selective Repeat solution
	$(PYTHON) ../python/src/selective_repeat.py --loss $(LOSS_RATE) --corrupt $(CORRUPT_RATE) --window $(WINDOW)

test: ## Run the automated Selective Repeat checks
	bash script/test_selective_repeat.sh

clean: ## Remove temporary files
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete 2>/dev/null || true
