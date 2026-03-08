.PHONY: install build start dev test clean

# Directory references
SOLUTION_DIR := ../solve/solution
CODE_DIR := ./code

# Install dependencies for starter code
install:
	cd $(CODE_DIR) && pnpm install

# Install and build the solution
build:
	cd $(SOLUTION_DIR) && pnpm install && pnpm run build

# Start the solution server
start:
	cd $(SOLUTION_DIR) && pnpm run start

# Start the solution server in dev mode
dev:
	cd $(SOLUTION_DIR) && pnpm run dev

# Run tests against the solution
test:
	cd $(SOLUTION_DIR) && pnpm run test

# Clean build artifacts
clean:
	cd $(CODE_DIR) && rm -rf node_modules dist
	cd $(SOLUTION_DIR) && rm -rf node_modules dist
