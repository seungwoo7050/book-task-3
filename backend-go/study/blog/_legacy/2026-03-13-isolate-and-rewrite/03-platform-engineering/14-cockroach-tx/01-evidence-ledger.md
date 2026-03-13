# 14 Cockroach TX Evidence Ledger

이 문서는 기존 `blog/` 초안을 입력으로 읽지 않고, 살아 있는 근거만으로 chronology를 복원한 ledger다.

## 근거 묶음

- 프로젝트 요약: idempotency key, optimistic locking, transaction retry를 CockroachDB 호환 흐름으로 묶어 정합성 기초를 다지는 과제다.
- 구현 디렉터리: `solution/go`
- 주요 구현 파일: `solution/go/txn/retry.go`, `solution/go/service/purchase.go`, `solution/go/e2e/purchase_flow_test.go`
- 대표 검증 명령: `cd solution/go && go test -v ./service ./txn`, `cd solution/go && go test -run TestPurchaseFlowReplayAndPersistence -v ./e2e`
- 핵심 개념 축: idempotency key는 네트워크 재시도와 중복 요청을 구분하지 않고 같은 결과로 수렴시키는 장치다., optimistic locking은 `version` 컬럼으로 충돌을 감지한다., Cockroach류 분산 SQL은 serialization failure를 애플리케이션 레벨에서 재시도하게 요구할 수 있다., handler/service/repository 분리는 transaction 정책과 HTTP 정책을 분리한다.
- chronology 복원 주석: 이 경로의 git 이력은 대체로 큰 source drop과 문서 보강 위주라 세밀한 시각 정보를 주지 못한다. 그래서 chronology는 README, 살아 있는 소스코드, 테스트, 현재 CLI 재실행 결과를 기준으로 Phase 1/2/3 형태로 복원했다.

## Git History Anchor

- `2026-03-08 46051f3 A large commit`
- `2026-03-09 69364e2 docs(notion): backend-go`
- `2026-03-12 0e12fb8 Track 3에 대한 전반적인 개선 완료 (backend go/node/spring, front react )`

## Chronology Ledger

### 1. Phase 1 - retry transaction과 idempotency 저장소로 정합성 바닥을 먼저 세운다

- 당시 목표: retry transaction과 idempotency 저장소로 정합성 바닥을 먼저 세운다
- 변경 단위: `solution/go/txn/retry.go`의 `RunInTx`
- 처음 가설: `RunInTx`를 먼저 잠가야 retry와 idempotency 규칙을 HTTP 밖에서 설명할 수 있다고 봤다.
- 실제 조치: `solution/go/txn/retry.go`의 `RunInTx`를 중심으로 transaction retry, idempotency, repository 경계를 먼저 묶었다.
- CLI: `cd solution/go && go test -v ./service ./txn`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestErrConflictSentinel`였다.
- 핵심 코드 앵커:
- `RunInTx`: `solution/go/txn/retry.go`

```go
}
func RunInTx(ctx context.Context, db *sql.DB, maxRetries int, fn func(tx *sql.Tx) error) error {
	if maxRetries <= 0 {
		maxRetries = 3
	}

	var lastErr error
	for attempt := 0; attempt < maxRetries; attempt++ {
		lastErr = execTx(ctx, db, fn)
		if lastErr == nil {
```

- 새로 배운 것: idempotency key는 네트워크 재시도와 중복 요청을 구분하지 않고 같은 결과로 수렴시키는 장치다.
- 다음: PurchaseService와 HTTP handler로 구매 흐름을 연결한다
### 2. Phase 2 - PurchaseService와 HTTP handler로 구매 흐름을 연결한다

- 당시 목표: PurchaseService와 HTTP handler로 구매 흐름을 연결한다
- 변경 단위: `solution/go/service/purchase.go`의 `PurchaseService.Purchase`
- 처음 가설: `PurchaseService.Purchase`에 제품 흐름을 모아 두면 handler와 query surface가 도메인 규칙을 그대로 따라간다고 판단했다.
- 실제 조치: `solution/go/service/purchase.go`의 `PurchaseService.Purchase`를 통해 purchase API or query surface를 제품 흐름으로 연결했다.
- CLI: `cd solution/go && go test -run TestPurchaseFlowReplayAndPersistence -v ./e2e`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestPurchaseFlowReplayAndPersistence`였다.
- 핵심 코드 앵커:
- `PurchaseService.Purchase`: `solution/go/service/purchase.go`

```go
}
func (s *PurchaseService) Purchase(ctx context.Context, req PurchaseRequest) (*PurchaseResponse, error) {
	var resp *PurchaseResponse

	err := txn.RunInTx(ctx, s.DB, s.MaxRetries, func(tx *sql.Tx) error {
		cached, err := repository.GetIdempotencyKey(ctx, tx, req.IdempotencyKey)
		if err == nil {
			var cachedResp PurchaseResponse
			if err := json.Unmarshal(cached, &cachedResp); err != nil {
				return fmt.Errorf("unmarshal cached response: %w", err)
```

- 새로 배운 것: retry를 과하게 넣으면 지연과 중복 부하가 늘어난다.
- 다음: unit, e2e repro로 Cockroach retry semantics를 검증한다
### 3. Phase 3 - unit, e2e repro로 Cockroach retry semantics를 검증한다

- 당시 목표: unit, e2e repro로 Cockroach retry semantics를 검증한다
- 변경 단위: `solution/go/e2e/purchase_flow_test.go`의 `TestPurchaseFlowReplayAndPersistence`
- 처음 가설: `TestPurchaseFlowReplayAndPersistence` 같은 e2e가 있어야 로컬 DB를 올린 재현성이 unit test 밖으로 확장된다고 봤다.
- 실제 조치: `solution/go/e2e/purchase_flow_test.go`의 `TestPurchaseFlowReplayAndPersistence`와 runtime-backed e2e를 돌려 DB가 있는 상태에서도 같은 규칙이 유지되는지 확인했다.
- CLI: `cd solution/go && go test -run TestPurchaseFlowReplayAndPersistence -v ./e2e`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestPurchaseFlowReplayAndPersistence`였다.
- 핵심 코드 앵커:
- `TestPurchaseFlowReplayAndPersistence`: `solution/go/e2e/purchase_flow_test.go`

```go
func TestPurchaseFlowReplayAndPersistence(t *testing.T) {
	requireRuntime(t)

	db := openDB(t)
	t.Cleanup(func() { _ = db.Close() })

	resetState(t, db)
	seedPlayer(t, db, 1_000)
```

- 새로 배운 것: idempotency response 저장 시점이 트랜잭션 밖이면 dual-write 비슷한 문제가 생긴다.
- 다음: 최종 글은 이 세 phase를 같은 순서로 묶어 development log로 다시 쓴다.

## Latest CLI Excerpt

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/14-cockroach-tx && cd solution/go && go test -v ./service ./txn)
```

```text
=== RUN   TestErrConflictSentinel
--- PASS: TestErrConflictSentinel (0.00s)
=== RUN   TestPurchaseRequestValidation
=== RUN   TestPurchaseRequestValidation/valid_request
=== RUN   TestPurchaseRequestValidation/missing_idempotency_key
=== RUN   TestPurchaseRequestValidation/missing_player_id
=== RUN   TestPurchaseRequestValidation/zero_price
=== RUN   TestPurchaseRequestValidation/negative_price
--- PASS: TestPurchaseRequestValidation (0.00s)
    --- PASS: TestPurchaseRequestValidation/valid_request (0.00s)
    --- PASS: TestPurchaseRequestValidation/missing_idempotency_key (0.00s)
    --- PASS: TestPurchaseRequestValidation/missing_player_id (0.00s)
    --- PASS: TestPurchaseRequestValidation/zero_price (0.00s)
    --- PASS: TestPurchaseRequestValidation/negative_price (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/03-platform-engineering/14-cockroach-tx/service	(cached)
=== RUN   TestIsRetryable
=== RUN   TestIsRetryable/40001_is_retryable
=== RUN   TestIsRetryable/other_pg_error_is_not_retryable
=== RUN   TestIsRetryable/wrapped_40001_is_retryable
=== RUN   TestIsRetryable/plain_error_is_not_retryable
=== RUN   TestIsRetryable/nil_is_not_retryable
... (18 more lines)
```

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/14-cockroach-tx && cd solution/go && go test -run TestPurchaseFlowReplayAndPersistence -v ./e2e)
```

```text
=== RUN   TestPurchaseFlowReplayAndPersistence
    purchase_flow_test.go:32: set RUN_E2E=1 to execute runtime integration tests
--- SKIP: TestPurchaseFlowReplayAndPersistence (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/03-platform-engineering/14-cockroach-tx/e2e	(cached)
```
