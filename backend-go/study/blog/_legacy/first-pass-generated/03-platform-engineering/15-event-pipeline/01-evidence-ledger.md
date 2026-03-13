# 15 Event Pipeline Evidence Ledger

이 문서는 기존 `blog/` 초안을 입력으로 읽지 않고, 살아 있는 근거만으로 chronology를 복원한 ledger다.

## 근거 묶음

- 프로젝트 요약: outbox pattern, relay, idempotent consumer를 통해 DB 정합성과 비동기 전달 경계를 함께 다루는 대표 과제다.
- 구현 디렉터리: `solution/go`
- 주요 구현 파일: `solution/go/outbox/repository.go`, `solution/go/relay/relay.go`, `solution/go/e2e/pipeline_flow_test.go`
- 대표 검증 명령: `cd solution/go && go test -v ./outbox ./relay ./consumer`, `cd solution/go && go test -run TestConsumerIdempotency -v ./consumer`
- 핵심 개념 축: `outbox pattern은 DB 변경과 이벤트 기록을 한 트랜잭션 안에 묶는다.`, `relay는 outbox row를 브로커로 밀어내는 별도 프로세스다.`, `consumer는 at-least-once 환경을 가정하고 중복 처리를 견뎌야 한다.`, `message key를 aggregate id로 두면 같은 집계 단위의 순서를 지키기 쉽다.`
- chronology 복원 주석: 이 경로의 git 이력은 대체로 큰 source drop과 문서 보강 위주라 세밀한 시각 정보를 주지 못한다. 그래서 chronology는 README, 살아 있는 소스코드, 테스트, 현재 CLI 재실행 결과를 기준으로 Phase 1/2/3 형태로 복원했다.

## Git History Anchor

- `2026-03-08 46051f3 A large commit`
- `2026-03-09 69364e2 docs(notion): backend-go`
- `2026-03-12 0e12fb8 Track 3에 대한 전반적인 개선 완료 (backend go/node/spring, front react )`

## Chronology Ledger

                ### 1. Phase 1 - Outbox repository로 DB write side를 먼저 고정한다

        - 당시 목표: Outbox repository로 DB write side를 먼저 고정한다
        - 변경 단위: `solution/go/outbox/repository.go`의 `Repository.GetUnpublished`
        - 처음 가설: `Repository.GetUnpublished`를 먼저 세워야 DB write와 publish 경계가 뒤섞이지 않는다고 봤다.
        - 실제 조치: `solution/go/outbox/repository.go`의 `Repository.GetUnpublished`에서 outbox persistence와 publish 대상 추출 규칙을 먼저 세웠다.
        - CLI: `cd solution/go && go test -v ./outbox ./relay ./consumer`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestPurchasePayloadMarshal`였다.
        - 핵심 코드 앵커:
        - `Repository.GetUnpublished`: `solution/go/outbox/repository.go`

        ```go
        // GetUnpublished는 아직 발행되지 않은 이벤트를 생성 시각 순으로 조회한다.
func (r *Repository) GetUnpublished(ctx context.Context, limit int) ([]Event, error) {
	rows, err := r.DB.QueryContext(ctx,
		`SELECT id, aggregate_type, aggregate_id, event_type, payload, created_at
		 FROM outbox
		 WHERE published_at IS NULL
		 ORDER BY created_at ASC
		 LIMIT $1`,
		limit,
	)
        ```

        - 새로 배운 것: outbox pattern은 DB 변경과 이벤트 기록을 한 트랜잭션 안에 묶는다.
        - 다음: Relay와 Consumer로 publish, consume 경계를 분리한다
        ### 2. Phase 2 - Relay와 Consumer로 publish, consume 경계를 분리한다

        - 당시 목표: Relay와 Consumer로 publish, consume 경계를 분리한다
        - 변경 단위: `solution/go/relay/relay.go`의 `Relay.Run`
        - 처음 가설: `Relay.Run`에 relay or consumer loop를 모아 두면 restart-safe 흐름을 더 짧게 설명할 수 있다고 판단했다.
        - 실제 조치: `solution/go/relay/relay.go`의 `Relay.Run`를 통해 relay, consumer, dedupe 흐름을 분리했다.
        - CLI: `cd solution/go && go test -run TestConsumerIdempotency -v ./consumer`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestConsumerIdempotency`였다.
        - 핵심 코드 앵커:
        - `Relay.Run`: `solution/go/relay/relay.go`

        ```go
        // Run은 ctx가 취소될 때까지 폴링 루프를 실행한다.
func (r *Relay) Run(ctx context.Context) error {
	r.logger.Info("relay started", "interval", r.interval, "batch", r.batch)

	ticker := time.NewTicker(r.interval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
        ```

        - 새로 배운 것: consumer idempotency 저장소가 없으면 중복 허용이 어렵다.
        - 다음: e2e와 dedupe tests로 restart-safe pipeline을 검증한다
        ### 3. Phase 3 - e2e와 dedupe tests로 restart-safe pipeline을 검증한다

        - 당시 목표: e2e와 dedupe tests로 restart-safe pipeline을 검증한다
        - 변경 단위: `solution/go/e2e/pipeline_flow_test.go`의 `TestRelayPublishesAndConsumerDedupesAcrossRestart`
        - 처음 가설: `TestRelayPublishesAndConsumerDedupesAcrossRestart` 같은 e2e가 있어야 dedupe와 restart 시나리오를 실제 runtime에서 검증할 수 있다고 봤다.
        - 실제 조치: `solution/go/e2e/pipeline_flow_test.go`의 `TestRelayPublishesAndConsumerDedupesAcrossRestart`와 runtime e2e를 돌려 restart 이후에도 같은 이벤트가 중복 처리되지 않는지 확인했다.
        - CLI: `cd solution/go && go test -run TestConsumerIdempotency -v ./consumer`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestConsumerIdempotency`였다.
        - 핵심 코드 앵커:
        - `TestRelayPublishesAndConsumerDedupesAcrossRestart`: `solution/go/e2e/pipeline_flow_test.go`

        ```go
        func TestRelayPublishesAndConsumerDedupesAcrossRestart(t *testing.T) {
	requireRuntime(t)

	db := openDB(t)
	t.Cleanup(func() { _ = db.Close() })
	resetState(t, db)

	broker := os.Getenv("KAFKA_BROKER")
	if broker == "" {
        ```

        - 새로 배운 것: relay와 consumer를 한 프로세스로 섞으면 책임 분리가 흐려진다.
        - 다음: 최종 글은 이 세 phase를 같은 순서로 묶어 development log로 다시 쓴다.

## Latest CLI Excerpt

        ```bash
(cd /Users/woopinbell/work/book-task-3/study/03-platform-engineering/15-event-pipeline && cd solution/go && go test -v ./outbox ./relay ./consumer)
```

```text
=== RUN   TestPurchasePayloadMarshal
=== RUN   TestPurchasePayloadMarshal/basic_purchase
=== RUN   TestPurchasePayloadMarshal/zero_balance
--- PASS: TestPurchasePayloadMarshal (0.00s)
    --- PASS: TestPurchasePayloadMarshal/basic_purchase (0.00s)
    --- PASS: TestPurchasePayloadMarshal/zero_balance (0.00s)
=== RUN   TestEventModel
--- PASS: TestEventModel (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/03-platform-engineering/15-event-pipeline/outbox	0.430s
=== RUN   TestConfigDefaults
=== RUN   TestConfigDefaults/zero_values_get_defaults
=== RUN   TestConfigDefaults/custom_values_preserved
--- PASS: TestConfigDefaults (0.00s)
    --- PASS: TestConfigDefaults/zero_values_get_defaults (0.00s)
    --- PASS: TestConfigDefaults/custom_values_preserved (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/03-platform-engineering/15-event-pipeline/relay	0.696s
=== RUN   TestGetHeader
=== RUN   TestGetHeader/found
=== RUN   TestGetHeader/not_found
=== RUN   TestGetHeader/empty_headers
... (10 more lines)
```

```bash
(cd /Users/woopinbell/work/book-task-3/study/03-platform-engineering/15-event-pipeline && cd solution/go && go test -run TestConsumerIdempotency -v ./consumer)
```

```text
=== RUN   TestConsumerIdempotency
--- PASS: TestConsumerIdempotency (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/03-platform-engineering/15-event-pipeline/consumer	0.289s
```
