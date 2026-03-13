# 12 gRPC Microservices — Client Flow And Proof

`02-distributed-systems/12-grpc-microservices`는 Protocol Buffers, unary/streaming RPC, interceptor를 작은 Product Catalog 서비스로 묶어 contract-first 감각을 익히는 과제다. 이 글에서는 8단계: 클라이언트 구현 (client/client.go) -> 9단계: 실행 및 검증 -> 10단계: 테스트 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 8단계: 클라이언트 구현 (client/client.go)
- 9단계: 실행 및 검증
- 10단계: 테스트

## Day 1
### Session 1

- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/client/client.go`, `solution/go/server/store/store_test.go`
- 처음 가설: client와 server를 분리해 retry, auth, logging interceptor를 서로 다른 관점에서 읽게 했다.
- 실제 진행: `grpc.Dial` with insecure credentials Round-robin load balancing Retry interceptor (max 3, exponential backoff) Logging interceptor 서버 시작 클라이언트 테스트 (별도 터미널) Store 테스트: CRUD, List 필터, 동시 접근 안전성.

CLI:

```bash
go run ./server/cmd
# starting gRPC server port=50051

go run ./client/cmd
```

검증 신호:

- 2026-03-07 기준 세 명령이 모두 통과했다.
- store 패키지 테스트는 정상 통과했고, client/server cmd 패키지는 smoke build 수준으로 검증했다.
- 남은 선택 검증: generated `.pb.go` 자동 생성 파이프라인은 아직 별도로 마련하지 않았다.

핵심 코드: `solution/go/client/client.go`

```go
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
```

왜 이 코드가 중요했는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

새로 배운 것:

- unary 중심 예제라도 client/server 분리와 retry 로직을 같이 보면 gRPC 특성이 더 잘 드러난다.

보조 코드: `solution/go/server/store/store_test.go`

```go
func TestCreateAndGet(t *testing.T) {
	s := NewProductStore()

	p := s.Create(&Product{
		Name:       "Widget",
		Price:      9.99,
		Categories: []string{"tools"},
		Stock:      100,
	})

	if p.ID == "" {
		t.Fatal("expected a generated ID")
	}

	got, err := s.Get(p.ID)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
```

왜 이 코드도 같이 봐야 하는가:

이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.

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

- generated `.pb.go` 자동 생성 파이프라인은 아직 별도로 마련하지 않았다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/client/client.go` 같은 결정적인 코드와 `cd 02-distributed-systems/12-grpc-microservices` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
