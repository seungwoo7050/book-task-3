# 12 gRPC Microservices — Server Store And Interceptors

`02-distributed-systems/12-grpc-microservices`는 Protocol Buffers, unary/streaming RPC, interceptor를 작은 Product Catalog 서비스로 묶어 contract-first 감각을 익히는 과제다. 이 글에서는 5단계: ProductStore 구현 (server/store/store.go) -> 6단계: Interceptor 구현 (server/interceptors/interceptors.go) -> 7단계: 서버 구현 (server/cmd/main.go) 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 5단계: ProductStore 구현 (server/store/store.go)
- 6단계: Interceptor 구현 (server/interceptors/interceptors.go)
- 7단계: 서버 구현 (server/cmd/main.go)

## Day 1
### Session 1

- 당시 목표: server-side streaming과 bidirectional streaming 흐름을 hand-written shim 기준으로 재현했다.
- 변경 단위: `solution/go/server/interceptors/interceptors.go`, `solution/go/server/cmd/main.go`
- 처음 가설: client와 server를 분리해 retry, auth, logging interceptor를 서로 다른 관점에서 읽게 했다.
- 실제 진행: 08의 Repository 패턴을 gRPC에 맞춰 적용: `sync.RWMutex` + `map[string]*Product` `atomic.Int64`로 ID 생성 (`prod-1`, `prod-2`, ...) `copyProduct`로 방어적 복사 CRUD + List(카테고리 필터) 세 가지 interceptor: `LoggingUnaryInterceptor` — method, duration, status code 로깅 (slog) `LoggingStreamInterceptor` — stream RPC 로깅 `AuthUnaryInterceptor` — metadata에서 authorization 토큰 검증 포트 50051, Seed 데이터 2개, graceful shutdown (SIGINT/SIGTERM).

CLI:

```bash
cd 02-distributed-systems/12-grpc-microservices
make -C problem build-server
make -C problem build-client
make -C problem test
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/server/interceptors/interceptors.go`

```go
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
```

왜 이 코드가 중요했는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

새로 배운 것:

- interceptor는 HTTP middleware와 비슷하지만 RPC 레벨의 횡단 관심사를 다룬다.

보조 코드: `solution/go/server/cmd/main.go`

```go
func main() {
	logger := slog.New(slog.NewTextHandler(os.Stdout, nil))

	productStore := store.NewProductStore()
	productStore.Create(&store.Product{
		Name: "Mechanical Keyboard", Description: "Cherry MX switches",
		Price: 129.99, Categories: []string{"electronics", "peripherals"}, Stock: 50,
	})
	productStore.Create(&store.Product{
		Name: "Go Programming Book", Description: "Advanced Go patterns",
		Price: 39.99, Categories: []string{"books", "programming"}, Stock: 200,
	})
	validTokens := map[string]bool{
		"Bearer secret-token-123": true,
	}

	srv := grpc.NewServer(
		grpc.ChainUnaryInterceptor(
```

왜 이 코드도 같이 봐야 하는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

CLI:

```bash
cd 02-distributed-systems/12-grpc-microservices
make -C problem build-server
make -C problem build-client
make -C problem test
```

검증 신호:

- 2026-03-07 기준 세 명령이 모두 통과했다.
- store 패키지 테스트는 정상 통과했고, client/server cmd 패키지는 smoke build 수준으로 검증했다.

다음:

- 다음 글에서는 `30-client-flow-and-proof.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/server/interceptors/interceptors.go` 같은 결정적인 코드와 `cd 02-distributed-systems/12-grpc-microservices` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
