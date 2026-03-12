// Package client는 ProductCatalog 서비스용 gRPC 클라이언트 연결 유틸리티를 제공한다.
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

// NewConnection은 재시도 interceptor와 로드 밸런싱 설정을 포함한 gRPC 연결을 생성한다.
func NewConnection(target string, logger *slog.Logger) (*grpc.ClientConn, error) {
	//nolint:staticcheck // grpc.NewClient로 바꾸려면 더 높은 gRPC 버전이 필요하다.
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

// retryInterceptor는 UNAVAILABLE 오류를 지수 백오프로 재시도한다.
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

// loggingClientInterceptor는 모든 unary RPC 호출을 로그로 남긴다.
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
