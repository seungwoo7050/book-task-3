# 17 Game Store Capstone Structure

## 이 글이 답할 질문

- idempotency key, optimistic locking, outbox relay, rate limiting을 한 프로젝트 안에서 다시 조합했다.
- OAuth나 마이크로서비스는 제외하고 거래 일관성과 재현성에 집중했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `04-capstone/17-game-store-capstone` 안에서 `20-purchase-flow-and-tx-core.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 5단계: domain 패키지 -> 6단계: repository 구현 -> 7단계: txn 패키지 (재사용) -> 8단계: service 구현
- 세션 본문: `txn/retry.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/internal/service/purchase_service.go`
- 코드 앵커 2: `solution/go/internal/txn/retry.go`
- 코드 설명 초점: 이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.
- 개념 설명: capstone의 핵심은 새 알고리즘보다 “여러 운영 제약이 한 곳에서 만날 때의 구조”다.
- 마지막 단락: 다음 글에서는 `30-relay-http-and-ops-surface.md`에서 이어지는 경계를 다룬다.
