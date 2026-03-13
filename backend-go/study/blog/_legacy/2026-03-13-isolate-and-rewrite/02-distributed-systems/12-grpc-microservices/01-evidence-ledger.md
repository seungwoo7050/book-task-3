# 12 gRPC Microservices Evidence Ledger

이 문서는 기존 `blog/` 초안을 입력으로 읽지 않고, 살아 있는 근거만으로 chronology를 복원한 ledger다.

## 근거 묶음

- 프로젝트 요약: Protocol Buffers, unary/streaming RPC, interceptor를 작은 Product Catalog 서비스로 묶어 contract-first 감각을 익히는 과제다.
- 구현 디렉터리: `solution/go`
- 주요 구현 파일: `solution/go/server/store/store.go`, `solution/go/server/interceptors/interceptors.go`, `solution/go/server/store/store_test.go`
- 대표 검증 명령: `cd solution/go && go test -run TestCreateAndGet -v ./server/store`, `cd solution/go && go test -v -race -count=1 ./...`
- 핵심 개념 축: proto-first는 API 계약을 코드보다 먼저 고정하는 접근이다., interceptor는 HTTP middleware와 비슷하지만 RPC 레벨의 횡단 관심사를 다룬다., unary 중심 예제라도 client/server 분리와 retry 로직을 같이 보면 gRPC 특성이 더 잘 드러난다.
- chronology 복원 주석: 이 경로의 git 이력은 대체로 큰 source drop과 문서 보강 위주라 세밀한 시각 정보를 주지 못한다. 그래서 chronology는 README, 살아 있는 소스코드, 테스트, 현재 CLI 재실행 결과를 기준으로 Phase 1/2/3 형태로 복원했다.

## Git History Anchor

- `2026-03-08 46051f3 A large commit`
- `2026-03-09 69364e2 docs(notion): backend-go`
- `2026-03-12 0e12fb8 Track 3에 대한 전반적인 개선 완료 (backend go/node/spring, front react )`

## Chronology Ledger

### 1. Phase 1 - ProductStore로 CRUD 바닥을 먼저 세운다

- 당시 목표: ProductStore로 CRUD 바닥을 먼저 세운다
- 변경 단위: `solution/go/server/store/store.go`의 `NewProductStore`
- 처음 가설: `NewProductStore`로 CRUD 바닥을 먼저 세우면 transport와 proto는 뒤에서 갈아끼우기 쉽다고 봤다.
- 실제 조치: `solution/go/server/store/store.go`의 `NewProductStore`를 기준으로 CRUD 바닥과 not-found 처리를 먼저 세웠다.
- CLI: `cd solution/go && go test -run TestCreateAndGet -v ./server/store`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestCreateAndGet`였다.
- 핵심 코드 앵커:
- `NewProductStore`: `solution/go/server/store/store.go`

```go
func NewProductStore() *ProductStore {
	s := &ProductStore{
		products: make(map[string]*Product),
	}
	s.nextID.Store(1)
	return s
}
func (s *ProductStore) Create(p *Product) *Product {
	s.mu.Lock()
```

- 새로 배운 것: proto-first는 API 계약을 코드보다 먼저 고정하는 접근이다.
- 다음: server, client, interceptor로 transport 경계를 얹는다
### 2. Phase 2 - server, client, interceptor로 transport 경계를 얹는다

- 당시 목표: server, client, interceptor로 transport 경계를 얹는다
- 변경 단위: `solution/go/server/interceptors/interceptors.go`의 `LoggingUnaryInterceptor`
- 처음 가설: `LoggingUnaryInterceptor`에 공통 interceptor를 모아 두면 client, server 양쪽 계약을 더 선명하게 드러낼 수 있다고 판단했다.
- 실제 조치: `solution/go/server/interceptors/interceptors.go`의 `LoggingUnaryInterceptor`를 붙여 logging, auth, rpc transport 경계를 드러냈다.
- CLI: `cd solution/go && go test -v -race -count=1 ./...`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `?   	github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices/client	[no test files]`였다.
- 핵심 코드 앵커:
- `LoggingUnaryInterceptor`: `solution/go/server/interceptors/interceptors.go`

```go
func LoggingUnaryInterceptor(logger *slog.Logger) grpc.UnaryServerInterceptor {
	return func(
		ctx context.Context,
		req any,
		info *grpc.UnaryServerInfo,
		handler grpc.UnaryHandler,
	) (any, error) {
		start := time.Now()
```

- 새로 배운 것: round-robin과 retry는 감각을 보여 주지만, production-grade observability나 timeout 정책은 더 필요하다.
- 다음: store tests와 race 검증으로 rpc 표면을 잠근다
### 3. Phase 3 - store tests와 race 검증으로 rpc 표면을 잠근다

- 당시 목표: store tests와 race 검증으로 rpc 표면을 잠근다
- 변경 단위: `solution/go/server/store/store_test.go`의 `TestCreateAndGet`
- 처음 가설: `TestCreateAndGet`와 race 테스트가 있어야 store와 rpc 표면이 같이 검증된다고 봤다.
- 실제 조치: `solution/go/server/store/store_test.go`의 `TestCreateAndGet`와 race test를 함께 돌려 store와 proto surface가 같이 살아 있는지 확인했다.
- CLI: `cd solution/go && go test -v -race -count=1 ./...`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `?   	github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices/client	[no test files]`였다.
- 핵심 코드 앵커:
- `TestCreateAndGet`: `solution/go/server/store/store_test.go`

```go
func TestCreateAndGet(t *testing.T) {
	s := NewProductStore()

	p := s.Create(&Product{
		Name:       "Widget",
		Price:      9.99,
		Categories: []string{"tools"},
		Stock:      100,
	})
```

- 새로 배운 것: unary call만 보고 gRPC를 “HTTP와 크게 다르지 않다”고 오해하기 쉽다.
- 다음: 최종 글은 이 세 phase를 같은 순서로 묶어 development log로 다시 쓴다.

## Latest CLI Excerpt

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/02-distributed-systems/12-grpc-microservices && cd solution/go && go test -run TestCreateAndGet -v ./server/store)
```

```text
=== RUN   TestCreateAndGet
--- PASS: TestCreateAndGet (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices/server/store	(cached)
```

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/02-distributed-systems/12-grpc-microservices && cd solution/go && go test -v -race -count=1 ./...)
```

```text
?   	github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices/client	[no test files]
?   	github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices/client/cmd	[no test files]
?   	github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices/server/cmd	[no test files]
?   	github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices/server/interceptors	[no test files]
=== RUN   TestCreateAndGet
--- PASS: TestCreateAndGet (0.00s)
=== RUN   TestGetNotFound
--- PASS: TestGetNotFound (0.00s)
=== RUN   TestUpdate
--- PASS: TestUpdate (0.00s)
=== RUN   TestDelete
--- PASS: TestDelete (0.00s)
=== RUN   TestList
=== RUN   TestList/no_filter
=== RUN   TestList/filter_electronics
=== RUN   TestList/filter_books
=== RUN   TestList/filter_nonexistent
--- PASS: TestList (0.00s)
    --- PASS: TestList/no_filter (0.00s)
    --- PASS: TestList/filter_electronics (0.00s)
    --- PASS: TestList/filter_books (0.00s)
    --- PASS: TestList/filter_nonexistent (0.00s)
... (2 more lines)
```
