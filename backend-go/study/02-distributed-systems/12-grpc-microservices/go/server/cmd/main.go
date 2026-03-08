// Command server starts the gRPC ProductCatalog server.
package main

import (
	"fmt"
	"log/slog"
	"net"
	"os"
	"os/signal"
	"syscall"

	"google.golang.org/grpc"

	"github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices/server/interceptors"
	"github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices/server/store"
)

const defaultPort = 50051

func main() {
	logger := slog.New(slog.NewTextHandler(os.Stdout, nil))

	productStore := store.NewProductStore()

	// Seed some products.
	productStore.Create(&store.Product{
		Name: "Mechanical Keyboard", Description: "Cherry MX switches",
		Price: 129.99, Categories: []string{"electronics", "peripherals"}, Stock: 50,
	})
	productStore.Create(&store.Product{
		Name: "Go Programming Book", Description: "Advanced Go patterns",
		Price: 39.99, Categories: []string{"books", "programming"}, Stock: 200,
	})

	// Valid tokens for auth interceptor.
	validTokens := map[string]bool{
		"Bearer secret-token-123": true,
	}

	srv := grpc.NewServer(
		grpc.ChainUnaryInterceptor(
			interceptors.LoggingUnaryInterceptor(logger),
			interceptors.AuthUnaryInterceptor(validTokens),
		),
		grpc.ChainStreamInterceptor(
			interceptors.LoggingStreamInterceptor(logger),
		),
	)

	// NOTE: In a full implementation, the generated service would be registered:
	// pb.RegisterProductCatalogServer(srv, catalog.NewCatalogService(productStore))
	_ = productStore

	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", defaultPort))
	if err != nil {
		logger.Error("failed to listen", "error", err)
		os.Exit(1)
	}

	// Graceful shutdown.
	go func() {
		quit := make(chan os.Signal, 1)
		signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
		<-quit
		logger.Info("shutting down gRPC server")
		srv.GracefulStop()
	}()

	logger.Info("starting gRPC server", "port", defaultPort)
	if err := srv.Serve(lis); err != nil {
		logger.Error("server error", "error", err)
		os.Exit(1)
	}
}
