package main

import (
	"log"
	"log/slog"
	"os"

	clientpkg "github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices/client"
)

func main() {
	target := "localhost:50051"
	if value := os.Getenv("GRPC_TARGET"); value != "" {
		target = value
	}

	conn, err := clientpkg.NewConnection(target, slog.Default())
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	log.Printf("gRPC client connection initialized for %s", target)
}
