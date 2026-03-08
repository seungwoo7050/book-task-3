// Package client provides a gRPC client with retry interceptor for the
// ProductCatalog service.
package client

import (
	"context"
	"log/slog"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/status"
)

// NewConnection creates a gRPC client connection with retry interceptor
// and round-robin load balancing.
func NewConnection(target string, logger *slog.Logger) (*grpc.ClientConn, error) {
	//nolint:staticcheck // grpc.Dial is deprecated but NewClient requires gRPC >= 1.63
	conn, err := grpc.Dial(
		target,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithDefaultServiceConfig(`{"loadBalancingConfig": [{"round_robin":{}}]}`),
		grpc.WithChainUnaryInterceptor(
			retryInterceptor(3, logger),
			loggingClientInterceptor(logger),
		),
	)
	return conn, err
}

// retryInterceptor retries UNAVAILABLE errors with exponential backoff.
func retryInterceptor(maxRetries int, logger *slog.Logger) grpc.UnaryClientInterceptor {
	return func(
		ctx context.Context,
		method string,
		req, reply any,
		cc *grpc.ClientConn,
		invoker grpc.UnaryInvoker,
		opts ...grpc.CallOption,
	) error {
		var lastErr error
		for attempt := 0; attempt <= maxRetries; attempt++ {
			lastErr = invoker(ctx, method, req, reply, cc, opts...)
			if lastErr == nil {
				return nil
			}

			if status.Code(lastErr) != codes.Unavailable {
				return lastErr
			}

			backoff := time.Duration(1<<uint(attempt)) * 100 * time.Millisecond
			logger.Warn("retrying rpc",
				"method", method,
				"attempt", attempt+1,
				"backoff", backoff.String(),
			)

			select {
			case <-ctx.Done():
				return ctx.Err()
			case <-time.After(backoff):
			}
		}
		return lastErr
	}
}

// loggingClientInterceptor logs every outgoing unary RPC call.
func loggingClientInterceptor(logger *slog.Logger) grpc.UnaryClientInterceptor {
	return func(
		ctx context.Context,
		method string,
		req, reply any,
		cc *grpc.ClientConn,
		invoker grpc.UnaryInvoker,
		opts ...grpc.CallOption,
	) error {
		start := time.Now()
		err := invoker(ctx, method, req, reply, cc, opts...)

		code := codes.OK
		if err != nil {
			code = status.Code(err)
		}

		logger.Info("client rpc",
			"method", method,
			"duration", time.Since(start).String(),
			"code", code.String(),
		)

		return err
	}
}
