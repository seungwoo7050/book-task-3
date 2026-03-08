.PHONY: install build start dev test clean

SOLUTION_DIR := ../solve/solution
CODE_DIR := ./code

install:
	cd $(CODE_DIR) && pnpm install

build:
	cd $(SOLUTION_DIR) && pnpm install && pnpm run build

start:
	cd $(SOLUTION_DIR) && pnpm run start

dev:
	cd $(SOLUTION_DIR) && pnpm run start:dev

test:
	cd $(SOLUTION_DIR) && pnpm run test

clean:
	cd $(CODE_DIR) && rm -rf node_modules dist
	cd $(SOLUTION_DIR) && rm -rf node_modules dist
