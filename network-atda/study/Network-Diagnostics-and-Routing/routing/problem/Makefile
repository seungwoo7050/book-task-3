# Distance-Vector Routing — Makefile
#
# Usage:
#   make run-sim                     # Run skeleton with default topology
#   make run-sim TOPO=data/topo2.json
#   make run-solution                # Run solution
#   make test                        # Run test suite
#   make clean

PYTHON := python3
TOPO   := data/topology.json

.PHONY: run-sim run-solution test clean help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

run-sim: ## Run the skeleton DV simulation
	$(PYTHON) code/dv_skeleton.py $(TOPO)

run-solution: ## Run the solution DV simulation
	$(PYTHON) ../python/src/dv_routing.py $(TOPO)

test: ## Run the test script
	bash script/test_routing.sh

clean: ## Remove temporary files
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete 2>/dev/null || true
