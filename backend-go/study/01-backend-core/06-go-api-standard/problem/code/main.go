// Starter skeleton for 01-go-api-standard.
// Complete the TODO items to build a working API server.
package main

import (
	"fmt"
	"log/slog"
	"os"
)

func main() {
	logger := slog.New(slog.NewTextHandler(os.Stdout, nil))

	// TODO: Read configuration from environment variables (PORT, ENV).

	// TODO: Initialize the application struct that holds dependencies
	//       (logger, config, models).

	// TODO: Set up the HTTP router using http.NewServeMux() with Go 1.22
	//       enhanced patterns. Register routes:
	//       - GET  /v1/healthcheck
	//       - POST /v1/movies
	//       - GET  /v1/movies/{id}
	//       - GET  /v1/movies
	//       - PATCH /v1/movies/{id}
	//       - DELETE /v1/movies/{id}

	// TODO: Wrap the router with middleware (logging, recovery, CORS).

	// TODO: Start the server with graceful shutdown support.

	logger.Info("TODO: implement the server")
	fmt.Println("starter skeleton — replace this with your implementation")
	os.Exit(0)
}
