# 12 gRPC Microservices — Proto Contract And Service Shape

`02-distributed-systems/12-grpc-microservices`는 Protocol Buffers, unary/streaming RPC, interceptor를 작은 Product Catalog 서비스로 묶어 contract-first 감각을 익히는 과제다. 이 글에서는 1단계: 프로젝트 초기화 -> 2단계: gRPC 의존성 설치 -> 3단계: 디렉토리 구조 생성 -> 4단계: Proto 정의 (proto/catalog.proto) 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 1단계: 프로젝트 초기화
- 2단계: gRPC 의존성 설치
- 3단계: 디렉토리 구조 생성
- 4단계: Proto 정의 (proto/catalog.proto)

## Day 1
### Session 1

- 당시 목표: Product Catalog용 gRPC 서비스 계약을 설계해야 한다.
- 변경 단위: `solution/go/proto/catalog.proto`, `solution/go/server/store/store.go`
- 처음 가설: generated code 자동화보다 계약과 호출 흐름을 먼저 이해시키기 위해 hand-written shim 예제를 택했다.
- 실제 진행: 메시지: Product, 각 RPC별 Request/Response, PriceUpdate 등.

CLI:

```bash
cd study/02-distributed-systems/12-grpc-microservices/go
go mod init github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices

go get google.golang.org/grpc@v1.62.0
go get google.golang.org/protobuf
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/proto/catalog.proto`

```proto
message Product {
  string id = 1;
  string name = 2;
  string description = 3;
  double price = 4;
  repeated string categories = 5;
  int32 stock = 6;
  google.protobuf.Timestamp created_at = 7;
  google.protobuf.Timestamp updated_at = 8;
}

// GetProductRequest is the request message for GetProduct RPC.
message GetProductRequest {
  string id = 1;
}

// CreateProductRequest is the request message for CreateProduct RPC.
message CreateProductRequest {
```

왜 이 코드가 중요했는가:

이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.

새로 배운 것:

- proto-first는 API 계약을 코드보다 먼저 고정하는 접근이다.

보조 코드: `solution/go/server/store/store.go`

```go
type Product struct {
	ID          string
	Name        string
	Description string
	Price       float64
	Categories  []string
	Stock       int32
	CreatedAt   time.Time
	UpdatedAt   time.Time
}

var (
	ErrNotFound      = errors.New("product not found")
	ErrAlreadyExists = errors.New("product already exists")
)

type ProductStore struct {
	mu       sync.RWMutex
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

- 다음 글에서는 `20-server-store-and-interceptors.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/proto/catalog.proto` 같은 결정적인 코드와 `cd 02-distributed-systems/12-grpc-microservices` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
