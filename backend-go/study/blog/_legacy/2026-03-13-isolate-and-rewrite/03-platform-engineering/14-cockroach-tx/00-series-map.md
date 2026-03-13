# 14 Cockroach TX 시리즈 맵

이 시리즈는 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다.

## 이번 재작성 범위

- 문제 계약: [`README.md`](../../../03-platform-engineering/14-cockroach-tx/README.md), [`problem/README.md`](../../../03-platform-engineering/14-cockroach-tx/problem/README.md)
- 구현 표면:
- `solution/go/txn/retry.go`
- `solution/go/service/purchase.go`
- `solution/go/e2e/purchase_flow_test.go`
- 검증 표면: `cd solution/go && go test -v ./service ./txn`, `cd solution/go && go test -run TestPurchaseFlowReplayAndPersistence -v ./e2e`
- 개념 축: idempotency key는 네트워크 재시도와 중복 요청을 구분하지 않고 같은 결과로 수렴시키는 장치다., optimistic locking은 `version` 컬럼으로 충돌을 감지한다., Cockroach류 분산 SQL은 serialization failure를 애플리케이션 레벨에서 재시도하게 요구할 수 있다.

## 챕터 구성

1. [`01-evidence-ledger.md`](01-evidence-ledger.md)
   실제 코드, 테스트, CLI, git history에서 복원한 chronology ledger
2. [`_structure-outline.md`](_structure-outline.md)
   최종 blog를 어떤 순서와 코드 앵커로 전개할지 먼저 고정한 구조 설계
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md)
   구현 순서, 판단 전환점, 검증 신호를 한 편으로 다시 쓴 최종 blog

## 이번에 따라간 질문

retry 가능한 transaction, idempotency, audit log를 DB-backed purchase flow로 묶는다.
