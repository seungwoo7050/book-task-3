# 15 Event Pipeline Structure Outline

이 문서는 chronology ledger를 바탕으로 최종 blog를 어떤 순서로 전개할지 먼저 고정한 설계 메모다. 기존 `blog/` 초안은 입력에서 제외했고, 실제 코드, README, docs, 테스트, CLI만을 근거로 삼는다.

## Planned Files

- `00-series-map.md`: 프로젝트 범위, source-of-truth, 읽는 순서를 잡는 진입 문서
- `01-evidence-ledger.md`: 파일, 함수, CLI 단위 chronology를 거칠게 복원한 근거 문서
- `10-2026-03-13-reconstructed-development-log.md`: 구현 순서와 판단 전환점을 세션 흐름으로 다시 쓴 최종 blog

## Final Blog Flow

- 도입: README 한 줄 요약과 이번 재검증 범위를 붙여 글의 위치를 먼저 밝힌다.
- 구현 순서 요약: Phase 1 -> Phase 2 -> Phase 3 순서를 미리 보여 준다.
- 세션형 chronology: 각 phase에서 당시 목표, 가설, 조치, 코드 앵커, 검증 신호를 순서대로 다시 적는다.
- CLI로 닫는 구간: 현재 저장소에서 다시 실행한 명령과 excerpt를 붙여 README 계약이 아직 살아 있는지 확인한다.
- 남은 질문: 개념 축과 다음 실험 지점을 남긴다.

## Section Plan

### 1. Phase 1 - Outbox repository로 DB write side를 먼저 고정한다

- 목표: Outbox repository로 DB write side를 먼저 고정한다
- 변경 단위: `solution/go/outbox/repository.go`의 `Repository.GetUnpublished`
- 핵심 가설: `Repository.GetUnpublished`를 먼저 세워야 DB write와 publish 경계가 뒤섞이지 않는다고 봤다.
- 반드시 넣을 코드 앵커: `Repository.GetUnpublished`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestPurchasePayloadMarshal`였다.
- 새로 배운 것 섹션 포인트: outbox pattern은 DB 변경과 이벤트 기록을 한 트랜잭션 안에 묶는다.
- 다음 섹션 연결 문장: Relay와 Consumer로 publish, consume 경계를 분리한다
### 2. Phase 2 - Relay와 Consumer로 publish, consume 경계를 분리한다

- 목표: Relay와 Consumer로 publish, consume 경계를 분리한다
- 변경 단위: `solution/go/relay/relay.go`의 `Relay.Run`
- 핵심 가설: `Relay.Run`에 relay or consumer loop를 모아 두면 restart-safe 흐름을 더 짧게 설명할 수 있다고 판단했다.
- 반드시 넣을 코드 앵커: `Relay.Run`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestConsumerIdempotency`였다.
- 새로 배운 것 섹션 포인트: consumer idempotency 저장소가 없으면 중복 허용이 어렵다.
- 다음 섹션 연결 문장: e2e와 dedupe tests로 restart-safe pipeline을 검증한다
### 3. Phase 3 - e2e와 dedupe tests로 restart-safe pipeline을 검증한다

- 목표: e2e와 dedupe tests로 restart-safe pipeline을 검증한다
- 변경 단위: `solution/go/e2e/pipeline_flow_test.go`의 `TestRelayPublishesAndConsumerDedupesAcrossRestart`
- 핵심 가설: `TestRelayPublishesAndConsumerDedupesAcrossRestart` 같은 e2e가 있어야 dedupe와 restart 시나리오를 실제 runtime에서 검증할 수 있다고 봤다.
- 반드시 넣을 코드 앵커: `TestRelayPublishesAndConsumerDedupesAcrossRestart`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestConsumerIdempotency`였다.
- 새로 배운 것 섹션 포인트: relay와 consumer를 한 프로세스로 섞으면 책임 분리가 흐려진다.
- 다음 섹션 연결 문장: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/15-event-pipeline && cd solution/go && go test -v ./outbox ./relay ./consumer)
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
ok  	github.com/woopinbell/go-backend/study/03-platform-engineering/15-event-pipeline/outbox	(cached)
=== RUN   TestConfigDefaults
=== RUN   TestConfigDefaults/zero_values_get_defaults
=== RUN   TestConfigDefaults/custom_values_preserved
--- PASS: TestConfigDefaults (0.00s)
    --- PASS: TestConfigDefaults/zero_values_get_defaults (0.00s)
    --- PASS: TestConfigDefaults/custom_values_preserved (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/03-platform-engineering/15-event-pipeline/relay	(cached)
=== RUN   TestGetHeader
=== RUN   TestGetHeader/found
=== RUN   TestGetHeader/not_found
=== RUN   TestGetHeader/empty_headers
... (10 more lines)
```

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/15-event-pipeline && cd solution/go && go test -run TestConsumerIdempotency -v ./consumer)
```

```text
=== RUN   TestConsumerIdempotency
--- PASS: TestConsumerIdempotency (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/03-platform-engineering/15-event-pipeline/consumer	(cached)
```
