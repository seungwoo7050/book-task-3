# 17 Game Store Capstone Structure Outline

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

### 1. Phase 1 - domain, repository, txn으로 purchase consistency 바닥을 먼저 세운다

- 목표: domain, repository, txn으로 purchase consistency 바닥을 먼저 세운다
- 변경 단위: `solution/go/internal/txn/retry.go`의 `RunInTx`
- 핵심 가설: `RunInTx`를 먼저 잠가야 retry와 idempotency 규칙을 HTTP 밖에서 설명할 수 있다고 봤다.
- 반드시 넣을 코드 앵커: `RunInTx`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestValidatePurchaseRequest`였다.
- 새로 배운 것 섹션 포인트: 구매 흐름은 transaction, idempotency, optimistic locking, relay를 동시에 건드린다.
- 다음 섹션 연결 문장: PurchaseService와 HTTP API로 제품 흐름을 연결한다
### 2. Phase 2 - PurchaseService와 HTTP API로 제품 흐름을 연결한다

- 목표: PurchaseService와 HTTP API로 제품 흐름을 연결한다
- 변경 단위: `solution/go/internal/service/purchase_service.go`의 `PurchaseService`
- 핵심 가설: `PurchaseService`에 제품 흐름을 모아 두면 handler와 query surface가 도메인 규칙을 그대로 따라간다고 판단했다.
- 반드시 넣을 코드 앵커: `PurchaseService`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestRelayPollOnce`였다.
- 새로 배운 것 섹션 포인트: relay와 DB를 분리하지 않으면 단순하지만 장애 모델이 불분명해진다.
- 다음 섹션 연결 문장: relay, e2e repro로 outbox와 조회 표면까지 닫는다
### 3. Phase 3 - relay, e2e repro로 outbox와 조회 표면까지 닫는다

- 목표: relay, e2e repro로 outbox와 조회 표면까지 닫는다
- 변경 단위: `solution/go/e2e/purchase_flow_test.go`의 `TestPurchaseFlowReplayReadAndRelay`
- 핵심 가설: `TestPurchaseFlowReplayReadAndRelay` 같은 e2e가 있어야 로컬 DB를 올린 재현성이 unit test 밖으로 확장된다고 봤다.
- 반드시 넣을 코드 앵커: `TestPurchaseFlowReplayReadAndRelay`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestRelayPollOnce`였다.
- 새로 배운 것 섹션 포인트: evidence 자산을 raw log로만 남기면 공개 저장소에서 읽기 어렵다.
- 다음 섹션 연결 문장: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## Fixed CLI Anchor

        ```bash
(cd /Users/woopinbell/work/book-task-3/study/04-capstone/17-game-store-capstone && cd solution/go && go test -v ./internal/service ./internal/relay ./internal/txn)
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
ok  	github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/service	0.813s
=== RUN   TestRelayPollOnce
--- PASS: TestRelayPollOnce (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/relay	0.415s
=== RUN   TestIsRetryable
=== RUN   TestIsRetryable/serialization_failure_is_retryable
=== RUN   TestIsRetryable/different_sqlstate_is_not_retryable
=== RUN   TestIsRetryable/wrapped_serialization_failure_is_retryable
=== RUN   TestIsRetryable/plain_error_is_not_retryable
=== RUN   TestIsRetryable/nil_is_not_retryable
... (8 more lines)
```

```bash
(cd /Users/woopinbell/work/book-task-3/study/04-capstone/17-game-store-capstone && cd solution/go && go test -run TestRelayPollOnce -v ./internal/relay)
```

```text
=== RUN   TestRelayPollOnce
--- PASS: TestRelayPollOnce (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/relay	0.261s
```
