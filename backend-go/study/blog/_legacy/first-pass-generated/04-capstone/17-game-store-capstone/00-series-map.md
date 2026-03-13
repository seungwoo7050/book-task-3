# 17 Game Store Capstone 시리즈 맵

이 시리즈는 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다.

## 이번 재작성 범위

- 문제 계약: [`README.md`](../../04-capstone/17-game-store-capstone/README.md), [`problem/README.md`](../../04-capstone/17-game-store-capstone/problem/README.md)
- 구현 표면:
- `solution/go/internal/txn/retry.go`
- `solution/go/internal/service/purchase_service.go`
- `solution/go/e2e/purchase_flow_test.go`
- 검증 표면: `cd solution/go && go test -v ./internal/service ./internal/relay ./internal/txn`, `cd solution/go && go test -run TestRelayPollOnce -v ./internal/relay`
- 개념 축: `구매 흐름은 transaction, idempotency, optimistic locking, relay를 동시에 건드린다.`, `capstone의 핵심은 새 알고리즘보다 “여러 운영 제약이 한 곳에서 만날 때의 구조”다.`, `e2e 테스트는 unit test가 놓치는 통합 문제를 빠르게 드러낸다.`

## 챕터 구성

1. [`01-evidence-ledger.md`](01-evidence-ledger.md)
   실제 코드, 테스트, CLI, git history에서 복원한 chronology ledger
2. [`_structure-outline.md`](_structure-outline.md)
   최종 blog를 어떤 순서와 코드 앵커로 전개할지 먼저 고정한 구조 설계
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md)
   구현 순서, 판단 전환점, 검증 신호를 한 편으로 다시 쓴 최종 blog

## 이번에 따라간 질문

도메인, transaction retry, relay, query API를 하나의 게임 상점 제품 흐름으로 묶는다.
