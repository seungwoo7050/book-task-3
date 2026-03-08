.PHONY: run test bench clean

SRC_DIR := ../go

test:
	@echo "Running tests..."
	cd $(SRC_DIR) && go test -v -race -count=1 ./...

bench:
	@echo "Running benchmarks..."
	cd $(SRC_DIR) && go test -bench=. -benchmem ./...

run-workerpool:
	@echo "Running worker pool example..."
	cd $(SRC_DIR) && go run ./cmd/workerpool

run-pipeline:
	@echo "Running pipeline example..."
	cd $(SRC_DIR) && go run ./cmd/pipeline

clean:
	cd $(SRC_DIR) && go clean -testcache
