# 접근 과정 — gRPC 서비스 구축

## Proto 정의 (contract-first)

REST API는 코드를 먼저 작성하고 문서를 나중에 만드는 경우가 많다. gRPC는 반대다. `.proto` 파일에서 서비스 계약을 먼저 정의하고, 코드를 생성한다.

```protobuf
service ProductCatalog {
  rpc GetProduct(GetProductRequest) returns (Product);
  rpc ListProducts(ListProductsRequest) returns (stream Product);
  rpc PriceWatch(stream PriceWatchRequest) returns (stream PriceUpdate);
}
```

`stream` 키워드가 스트리밍을 선언한다:
- 반환만 `stream` → Server streaming
- 요청만 `stream` → Client streaming
- 양쪽 `stream` → Bidirectional streaming

`google.protobuf.Timestamp`를 import해서 시간 필드를 표현했다. `string`으로 ISO 8601을 쓸 수도 있지만, proto의 well-known type을 쓰는 게 정석이다.

## 인메모리 Store (server/store)

`ProductStore`는 08의 Repository 패턴과 동일한 구조다:
- `sync.RWMutex`로 맵 보호
- `atomic.Int64`로 ID 생성
- `copyProduct`로 방어적 복사 (맵에 저장된 포인터가 외부에서 수정되지 않도록)

08과 다른 점: SQL 대신 순수 맵, HTTP가 아닌 gRPC 계층에서 사용.

## Interceptor (gRPC 미들웨어)

gRPC에서는 미들웨어를 interceptor라 부른다. HTTP의 `func(http.Handler) http.Handler`에 대응한다.

### Logging Interceptor

```go
func LoggingUnaryInterceptor(logger *slog.Logger) grpc.UnaryServerInterceptor {
    return func(ctx, req, info, handler) (any, error) {
        start := time.Now()
        resp, err := handler(ctx, req)
        // method, duration, status code 로깅
        return resp, err
    }
}
```

Unary와 Stream 각각 별도 interceptor가 필요하다. HTTP에서는 하나의 미들웨어가 모든 요청을 처리하지만, gRPC는 호출 패턴별로 시그니처가 다르다.

### Auth Interceptor

```go
func AuthUnaryInterceptor(validTokens map[string]bool) grpc.UnaryServerInterceptor
```

gRPC metadata에서 `authorization` 키를 읽는다. HTTP의 `Authorization` 헤더와 동일한 역할. metadata는 HTTP/2 헤더로 전송된다.

인증 실패 시 `codes.Unauthenticated`를 반환한다. HTTP의 401에 대응.

### Interceptor 체이닝

```go
grpc.ChainUnaryInterceptor(
    interceptors.LoggingUnaryInterceptor(logger),
    interceptors.AuthUnaryInterceptor(validTokens),
)
```

06의 미들웨어 체인(`recoverPanic → logRequest → router`)과 동일한 개념이지만, gRPC는 `Chain...Interceptor` 함수로 체이닝한다.

## 클라이언트 (client/)

### Retry with Exponential Backoff

```go
func retryInterceptor(maxRetries int, logger *slog.Logger) grpc.UnaryClientInterceptor
```

`codes.Unavailable` 에러에서만 재시도한다. backoff: 100ms → 200ms → 400ms (2^attempt * 100ms). context가 취소되면 즉시 중단.

### Round-Robin Load Balancing

```go
grpc.WithDefaultServiceConfig(`{"loadBalancingConfig": [{"round_robin":{}}]}`)
```

여러 서버 인스턴스가 있을 때, 요청을 순환 분배한다. DNS resolver와 함께 동작한다.

## Graceful Shutdown

06에서 배운 패턴이 gRPC에서도 그대로 적용된다:

```go
go func() {
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit
    srv.GracefulStop()
}()
```
