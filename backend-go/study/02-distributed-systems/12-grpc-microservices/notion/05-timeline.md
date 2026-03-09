# 타임라인 — gRPC 마이크로서비스 개발 전체 과정

## 1단계: 프로젝트 초기화

```bash
cd study/02-distributed-systems/12-grpc-microservices/go
go mod init github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices
```

## 2단계: gRPC 의존성 설치

```bash
go get google.golang.org/grpc@v1.62.0
go get google.golang.org/protobuf
```

## 3단계: 디렉토리 구조 생성

```bash
mkdir -p proto
mkdir -p server/store
mkdir -p server/interceptors
mkdir -p server/cmd
mkdir -p client/cmd
```

```
go/
├── go.mod
├── proto/
│   └── catalog.proto
├── server/
│   ├── store/
│   │   ├── store.go
│   │   └── store_test.go
│   ├── interceptors/
│   │   └── interceptors.go
│   └── cmd/
│       └── main.go
└── client/
    ├── client.go
    └── cmd/
        └── main.go
```

## 4단계: Proto 정의 (proto/catalog.proto)

```protobuf
syntax = "proto3";
package catalog;

service ProductCatalog {
  rpc GetProduct(GetProductRequest) returns (Product);
  rpc CreateProduct(CreateProductRequest) returns (Product);
  rpc UpdateProduct(UpdateProductRequest) returns (Product);
  rpc DeleteProduct(DeleteProductRequest) returns (DeleteProductResponse);
  rpc ListProducts(ListProductsRequest) returns (stream Product);
  rpc PriceWatch(stream PriceWatchRequest) returns (stream PriceUpdate);
}
```

메시지: Product, 각 RPC별 Request/Response, PriceUpdate 등.

## 5단계: ProductStore 구현 (server/store/store.go)

08의 Repository 패턴을 gRPC에 맞춰 적용:
- `sync.RWMutex` + `map[string]*Product`
- `atomic.Int64`로 ID 생성 (`prod-1`, `prod-2`, ...)
- `copyProduct`로 방어적 복사
- CRUD + List(카테고리 필터)

## 6단계: Interceptor 구현 (server/interceptors/interceptors.go)

세 가지 interceptor:
1. `LoggingUnaryInterceptor` — method, duration, status code 로깅 (slog)
2. `LoggingStreamInterceptor` — stream RPC 로깅
3. `AuthUnaryInterceptor` — metadata에서 authorization 토큰 검증

## 7단계: 서버 구현 (server/cmd/main.go)

```go
srv := grpc.NewServer(
    grpc.ChainUnaryInterceptor(
        interceptors.LoggingUnaryInterceptor(logger),
        interceptors.AuthUnaryInterceptor(validTokens),
    ),
    grpc.ChainStreamInterceptor(
        interceptors.LoggingStreamInterceptor(logger),
    ),
)
```

포트 50051, Seed 데이터 2개, graceful shutdown (SIGINT/SIGTERM).

## 8단계: 클라이언트 구현 (client/client.go)

```go
func NewConnection(target string, logger *slog.Logger) (*grpc.ClientConn, error)
```

- `grpc.Dial` with insecure credentials
- Round-robin load balancing
- Retry interceptor (max 3, exponential backoff)
- Logging interceptor

## 9단계: 실행 및 검증

### 서버 시작

```bash
go run ./server/cmd
# starting gRPC server port=50051
```

### 클라이언트 테스트 (별도 터미널)

```bash
go run ./client/cmd
```

### grpcurl 사용 (protoc 없이)

```bash
# grpcurl 설치
brew install grpcurl

# 서비스 목록 (reflection 필요)
grpcurl -plaintext localhost:50051 list

# 상품 생성
grpcurl -plaintext \
  -H "authorization: Bearer secret-token-123" \
  -d '{"name":"test","description":"test product","price":9.99}' \
  localhost:50051 catalog.ProductCatalog/CreateProduct
```

## 10단계: 테스트

```bash
go test ./server/store/...
```

Store 테스트: CRUD, List 필터, 동시 접근 안전성.

## 파일 목록

| 순서 | 파일 | 설명 |
|------|------|------|
| 1 | `go.mod` | 모듈 정의, grpc/protobuf 의존성 |
| 2 | `proto/catalog.proto` | 서비스 정의, 메시지 타입 |
| 3 | `server/store/store.go` | ProductStore (인메모리 CRUD) |
| 4 | `server/store/store_test.go` | Store 테스트 |
| 5 | `server/interceptors/interceptors.go` | Logging + Auth interceptor |
| 6 | `server/cmd/main.go` | gRPC 서버 엔트리포인트 |
| 7 | `client/client.go` | 클라이언트 연결, retry, logging |
| 8 | `client/cmd/main.go` | 클라이언트 엔트리포인트 |
