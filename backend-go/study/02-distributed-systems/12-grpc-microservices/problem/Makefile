.PHONY: proto build-server build-client run-server run-client test clean

SRC_DIR := ../go

proto:
	@echo "Generating protobuf code..."
	cd $(SRC_DIR) && protoc --go_out=. --go_opt=paths=source_relative \
		--go-grpc_out=. --go-grpc_opt=paths=source_relative \
		proto/catalog.proto

build-server:
	mkdir -p ./bin
	cd $(SRC_DIR) && go build -o ../problem/bin/server ./server/cmd

build-client:
	mkdir -p ./bin
	cd $(SRC_DIR) && go build -o ../problem/bin/client ./client/cmd

run-server:
	cd $(SRC_DIR) && go run ./server/cmd

run-client:
	cd $(SRC_DIR) && go run ./client/cmd

test:
	cd $(SRC_DIR) && go test -v -race -count=1 ./...

clean:
	@rm -rf bin/
