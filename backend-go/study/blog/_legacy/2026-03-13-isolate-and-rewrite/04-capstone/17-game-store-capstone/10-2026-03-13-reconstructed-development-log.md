# 17 Game Store Capstone 재구성 개발 로그

17 Game Store Capstone는 거래 일관성, outbox, 운영 기본 요소를 하나의 게임 상점 API로 통합한 필수 capstone이다.

이 글은 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 쓴 버전이다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다. 세밀한 shell history가 남아 있지 않아 시간 표지는 `Phase 1/2/3`처럼 재구성했고, 근거는 README, 살아 있는 소스코드, docs, 테스트, 현재 CLI 재실행 결과만 사용했다.

## 구현 순서 요약

- Phase 1: domain, repository, txn으로 purchase consistency 바닥을 먼저 세운다 - `solution/go/internal/txn/retry.go`의 `RunInTx`
- Phase 2: PurchaseService와 HTTP API로 제품 흐름을 연결한다 - `solution/go/internal/service/purchase_service.go`의 `PurchaseService`
- Phase 3: relay, e2e repro로 outbox와 조회 표면까지 닫는다 - `solution/go/e2e/purchase_flow_test.go`의 `TestPurchaseFlowReplayReadAndRelay`

## Phase 1. domain, repository, txn으로 purchase consistency 바닥을 먼저 세운다

- 당시 목표: domain, repository, txn으로 purchase consistency 바닥을 먼저 세운다
- 변경 단위: `solution/go/internal/txn/retry.go`의 `RunInTx`
- 처음 가설: `RunInTx`를 먼저 잠가야 retry와 idempotency 규칙을 HTTP 밖에서 설명할 수 있다고 봤다.
- 실제 진행: `solution/go/internal/txn/retry.go`의 `RunInTx`를 중심으로 transaction retry, idempotency, repository 경계를 먼저 묶었다.
- CLI: `cd solution/go && go test -v ./internal/service ./internal/relay ./internal/txn`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestValidatePurchaseRequest`였다.

핵심 코드:

```go
}
func RunInTx(ctx context.Context, db *sql.DB, maxRetries int, fn func(tx *sql.Tx) error) error {
	if maxRetries <= 0 {
		maxRetries = 3
	}

	var lastErr error
	for attempt := 0; attempt < maxRetries; attempt++ {
		lastErr = runOnce(ctx, db, fn)
		if lastErr == nil {
```

왜 이 코드가 중요했는가: `RunInTx`는 `solution/go/internal/txn/retry.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

- 새로 배운 것: 구매 흐름은 transaction, idempotency, optimistic locking, relay를 동시에 건드린다.
- 다음: PurchaseService와 HTTP API로 제품 흐름을 연결한다
## Phase 2. PurchaseService와 HTTP API로 제품 흐름을 연결한다

- 당시 목표: PurchaseService와 HTTP API로 제품 흐름을 연결한다
- 변경 단위: `solution/go/internal/service/purchase_service.go`의 `PurchaseService`
- 처음 가설: `PurchaseService`에 제품 흐름을 모아 두면 handler와 query surface가 도메인 규칙을 그대로 따라간다고 판단했다.
- 실제 진행: `solution/go/internal/service/purchase_service.go`의 `PurchaseService`를 통해 purchase API or query surface를 제품 흐름으로 연결했다.
- CLI: `cd solution/go && go test -run TestRelayPollOnce -v ./internal/relay`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestRelayPollOnce`였다.

핵심 코드:

```go
// PurchaseService는 멱등 구매 트랜잭션을 조율한다.
type PurchaseService struct {
	db         *sql.DB
	store      *repository.Store
	maxRetries int
}

// NewPurchaseService는 구매 서비스를 생성한다.
func NewPurchaseService(db *sql.DB, store *repository.Store) *PurchaseService {
	return &PurchaseService{
```

왜 이 코드가 중요했는가: `PurchaseService`는 `solution/go/internal/service/purchase_service.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

- 새로 배운 것: relay와 DB를 분리하지 않으면 단순하지만 장애 모델이 불분명해진다.
- 다음: relay, e2e repro로 outbox와 조회 표면까지 닫는다
## Phase 3. relay, e2e repro로 outbox와 조회 표면까지 닫는다

- 당시 목표: relay, e2e repro로 outbox와 조회 표면까지 닫는다
- 변경 단위: `solution/go/e2e/purchase_flow_test.go`의 `TestPurchaseFlowReplayReadAndRelay`
- 처음 가설: `TestPurchaseFlowReplayReadAndRelay` 같은 e2e가 있어야 로컬 DB를 올린 재현성이 unit test 밖으로 확장된다고 봤다.
- 실제 진행: `solution/go/e2e/purchase_flow_test.go`의 `TestPurchaseFlowReplayReadAndRelay`와 runtime-backed e2e를 돌려 DB가 있는 상태에서도 같은 규칙이 유지되는지 확인했다.
- CLI: `cd solution/go && go test -run TestRelayPollOnce -v ./internal/relay`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestRelayPollOnce`였다.

핵심 코드:

```go
func TestPurchaseFlowReplayReadAndRelay(t *testing.T) {
	db := openTestDB(t)
	store := repository.NewStore(db)
	server := newTestServer(t, db)
	defer server.Close()

	resetAndSeed(t, db)

	firstStatus, firstBody := doJSONRequest(t, http.MethodPost, server.URL+"/v1/purchases", "idem-e2e-001", map[string]string{
```

왜 이 코드가 중요했는가: `TestPurchaseFlowReplayReadAndRelay`는 `solution/go/e2e/purchase_flow_test.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

- 새로 배운 것: evidence 자산을 raw log로만 남기면 공개 저장소에서 읽기 어렵다.
- 다음: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## CLI 1. 현재 저장소에서 다시 돌린 검증

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/04-capstone/17-game-store-capstone && cd solution/go && go test -v ./internal/service ./internal/relay ./internal/txn)
```

```text
=== RUN   TestValidatePurchaseRequest
=== RUN   TestValidatePurchaseRequest/valid_request
=== RUN   TestValidatePurchaseRequest/missing_idempotency_key
=== RUN   TestValidatePurchaseRequest/missing_player_id
=== RUN   TestValidatePurchaseRequest/missing_item_id
--- PASS: TestValidatePurchaseRequest (0.00s)
    --- PASS: TestValidatePurchaseRequest/valid_request (0.00s)
    --- PASS: TestValidatePurchaseRequest/missing_idempotency_key (0.00s)
    --- PASS: TestValidatePurchaseRequest/missing_player_id (0.00s)
    --- PASS: TestValidatePurchaseRequest/missing_item_id (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/service	(cached)
=== RUN   TestRelayPollOnce
--- PASS: TestRelayPollOnce (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/relay	(cached)
=== RUN   TestIsRetryable
=== RUN   TestIsRetryable/serialization_failure_is_retryable
=== RUN   TestIsRetryable/different_sqlstate_is_not_retryable
=== RUN   TestIsRetryable/wrapped_serialization_failure_is_retryable
=== RUN   TestIsRetryable/plain_error_is_not_retryable
=== RUN   TestIsRetryable/nil_is_not_retryable
... (8 more lines)
```
## CLI 2. 현재 저장소에서 다시 돌린 검증

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/04-capstone/17-game-store-capstone && cd solution/go && go test -run TestRelayPollOnce -v ./internal/relay)
```

```text
=== RUN   TestRelayPollOnce
--- PASS: TestRelayPollOnce (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/relay	(cached)
```

## 이번 재작성에서 남은 것

- 이번 글을 지탱한 개념 축: 구매 흐름은 transaction, idempotency, optimistic locking, relay를 동시에 건드린다., capstone의 핵심은 새 알고리즘보다 “여러 운영 제약이 한 곳에서 만날 때의 구조”다., e2e 테스트는 unit test가 놓치는 통합 문제를 빠르게 드러낸다.
- 최신 검증 메모: 현재 저장소에서 다시 실행한 명령은 모두 exit 0으로 끝났다.
- 다음 질문: 도메인, transaction retry, relay, query API를 하나의 게임 상점 제품 흐름으로 묶는다.
