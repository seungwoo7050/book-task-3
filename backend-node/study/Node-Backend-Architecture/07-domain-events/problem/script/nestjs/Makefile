.PHONY: install build start test test-e2e
SOLUTION_DIR := ../solve/solution

install:
	cd code && pnpm install

build:
	cd code && pnpm run build

start:
	cd code && pnpm run start:dev

test:
	cd $(SOLUTION_DIR) && pnpm run test

test-e2e:
	cd $(SOLUTION_DIR) && pnpm run test:e2e
