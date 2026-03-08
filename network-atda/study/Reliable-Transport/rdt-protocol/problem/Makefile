# RDT Protocol — Makefile
#
# Usage:
#   make run-rdt3          Run the RDT 3.0 demo (skeleton)
#   make run-gbn           Run the GBN demo (skeleton)
#   make run-solution-rdt3 Run the RDT 3.0 solution
#   make run-solution-gbn  Run the GBN solution
#   make test              Run all tests
#   make clean             Remove temporary files

PYTHON    := python3
LOSS_RATE := 0.2
CORRUPT_RATE := 0.1

.PHONY: run-rdt3 run-gbn run-solution-rdt3 run-solution-gbn test clean help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-24s\033[0m %s\n", $$1, $$2}'

run-rdt3: ## Run the RDT 3.0 skeleton
	$(PYTHON) code/rdt3_skeleton.py --loss $(LOSS_RATE) --corrupt $(CORRUPT_RATE)

run-gbn: ## Run the GBN skeleton
	$(PYTHON) code/gbn_skeleton.py --loss $(LOSS_RATE) --corrupt $(CORRUPT_RATE)

run-solution-rdt3: ## Run the RDT 3.0 solution
	$(PYTHON) ../python/src/rdt3.py --loss $(LOSS_RATE) --corrupt $(CORRUPT_RATE)

run-solution-gbn: ## Run the GBN solution
	$(PYTHON) ../python/src/gbn.py --loss $(LOSS_RATE) --corrupt $(CORRUPT_RATE)

test: ## Run all tests
	bash script/test_rdt.sh

clean: ## Remove temporary files
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete 2>/dev/null || true
