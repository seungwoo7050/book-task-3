.PHONY: test bench run clean

SRC_DIR := ../solution/go

test:
	@echo "Running tests..."
	cd $(SRC_DIR) && go test -v -race -count=1 ./...

bench:
	@echo "Running benchmarks..."
	cd $(SRC_DIR) && go test -bench=. -benchmem ./...

clean:
	cd $(SRC_DIR) && go clean -testcache
