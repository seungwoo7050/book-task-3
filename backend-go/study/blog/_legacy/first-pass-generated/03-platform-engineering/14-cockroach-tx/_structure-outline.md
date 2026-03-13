# 14 Cockroach TX Structure Outline

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

### 1. Phase 1 - retry transaction과 idempotency 저장소로 정합성 바닥을 먼저 세운다

- 목표: retry transaction과 idempotency 저장소로 정합성 바닥을 먼저 세운다
- 변경 단위: `solution/go/txn/retry.go`의 `RunInTx`
- 핵심 가설: `RunInTx`를 먼저 잠가야 retry와 idempotency 규칙을 HTTP 밖에서 설명할 수 있다고 봤다.
- 반드시 넣을 코드 앵커: `RunInTx`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestErrConflictSentinel`였다.
- 새로 배운 것 섹션 포인트: idempotency key는 네트워크 재시도와 중복 요청을 구분하지 않고 같은 결과로 수렴시키는 장치다.
- 다음 섹션 연결 문장: PurchaseService와 HTTP handler로 구매 흐름을 연결한다
### 2. Phase 2 - PurchaseService와 HTTP handler로 구매 흐름을 연결한다

- 목표: PurchaseService와 HTTP handler로 구매 흐름을 연결한다
- 변경 단위: `solution/go/service/purchase.go`의 `PurchaseService.Purchase`
- 핵심 가설: `PurchaseService.Purchase`에 제품 흐름을 모아 두면 handler와 query surface가 도메인 규칙을 그대로 따라간다고 판단했다.
- 반드시 넣을 코드 앵커: `PurchaseService.Purchase`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestPurchaseFlowReplayAndPersistence`였다.
- 새로 배운 것 섹션 포인트: retry를 과하게 넣으면 지연과 중복 부하가 늘어난다.
- 다음 섹션 연결 문장: unit, e2e repro로 Cockroach retry semantics를 검증한다
### 3. Phase 3 - unit, e2e repro로 Cockroach retry semantics를 검증한다

- 목표: unit, e2e repro로 Cockroach retry semantics를 검증한다
- 변경 단위: `solution/go/e2e/purchase_flow_test.go`의 `TestPurchaseFlowReplayAndPersistence`
- 핵심 가설: `TestPurchaseFlowReplayAndPersistence` 같은 e2e가 있어야 로컬 DB를 올린 재현성이 unit test 밖으로 확장된다고 봤다.
- 반드시 넣을 코드 앵커: `TestPurchaseFlowReplayAndPersistence`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestPurchaseFlowReplayAndPersistence`였다.
- 새로 배운 것 섹션 포인트: idempotency response 저장 시점이 트랜잭션 밖이면 dual-write 비슷한 문제가 생긴다.
- 다음 섹션 연결 문장: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## Fixed CLI Anchor

        ```bash
(cd /Users/woopinbell/work/book-task-3/study/03-platform-engineering/14-cockroach-tx && cd solution/go && go test -v ./service ./txn)
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
(cd /Users/woopinbell/work/book-task-3/study/03-platform-engineering/14-cockroach-tx && cd solution/go && go test -run TestPurchaseFlowReplayAndPersistence -v ./e2e)
```

```text
=== RUN   TestPurchaseFlowReplayAndPersistence
    purchase_flow_test.go:32: set RUN_E2E=1 to execute runtime integration tests
--- SKIP: TestPurchaseFlowReplayAndPersistence (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/03-platform-engineering/14-cockroach-tx/e2e	0.467s
```
