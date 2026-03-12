package interceptors

import (
	"context"
	"log/slog"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
)

func LoggingUnaryInterceptor(logger *slog.Logger) grpc.UnaryServerInterceptor {
	return func(
		ctx context.Context,
		req any,
		info *grpc.UnaryServerInfo,
		handler grpc.UnaryHandler,
	) (any, error) {
		start := time.Now()

		resp, err := handler(ctx, req)

		code := codes.OK
		if err != nil {
			code = status.Code(err)
		}

		logger.Info("unary rpc",
			"method", info.FullMethod,
			"duration", time.Since(start).String(),
			"code", code.String(),
		)

		return resp, err
	}
}
func LoggingStreamInterceptor(logger *slog.Logger) grpc.StreamServerInterceptor {
	return func(
		srv any,
		ss grpc.ServerStream,
		info *grpc.StreamServerInfo,
		handler grpc.StreamHandler,
	) error {
		start := time.Now()

		err := handler(srv, ss)

		code := codes.OK
		if err != nil {
			code = status.Code(err)
		}

		logger.Info("stream rpc",
			"method", info.FullMethod,
			"duration", time.Since(start).String(),
			"code", code.String(),
		)

		return err
	}
}
func AuthUnaryInterceptor(validTokens map[string]bool) grpc.UnaryServerInterceptor {
	return func(
		ctx context.Context,
		req any,
		info *grpc.UnaryServerInfo,
		handler grpc.UnaryHandler,
	) (any, error) {
		md, ok := metadata.FromIncomingContext(ctx)
		if !ok {
			return nil, status.Errorf(codes.Unauthenticated, "missing metadata")
		}

		tokens := md.Get("authorization")
		if len(tokens) == 0 {
			return nil, status.Errorf(codes.Unauthenticated, "missing authorization token")
		}

		if !validTokens[tokens[0]] {
			return nil, status.Errorf(codes.Unauthenticated, "invalid authorization token")
		}

		return handler(ctx, req)
	}
}
