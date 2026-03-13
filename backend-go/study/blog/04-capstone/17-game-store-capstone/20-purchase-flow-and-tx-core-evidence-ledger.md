# 17 Game Store Capstone Evidence Ledger

## 20 purchase-flow-and-tx-core

- 시간 표지: 5단계: domain 패키지 -> 6단계: repository 구현 -> 7단계: txn 패키지 (재사용) -> 8단계: service 구현
- 당시 목표: idempotency key, optimistic locking, outbox relay, rate limiting을 한 프로젝트 안에서 다시 조합했다.
- 변경 단위: `txn/retry.go`
- 처음 가설: OAuth나 마이크로서비스는 제외하고 거래 일관성과 재현성에 집중했다.
- 실제 조치: 외부 의존 없는 순수 타입. `Store` struct에 전체 SQL 접근 메서드. 모든 쓰기 메서드는 `*sql.Tx` 인자. 프로젝트 14의 `txn/retry.go`를 그대로 복사. `PgError` 인터페이스, `IsRetryable`, `RunInTx`. `PurchaseService.Purchase` — 7단계 트랜잭션 로직: 멱등성 키 확인 → 플레이어/아이템 조회 → 잔액 차감 → 구매/인벤토리 → Outbox INSERT → 멱등성 키 INSERT

CLI:

```bash
go build ./internal/repository/

go test ./internal/txn/ -v
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/internal/service/purchase_service.go`
- 새로 배운 것: capstone의 핵심은 새 알고리즘보다 “여러 운영 제약이 한 곳에서 만날 때의 구조”다.
- 다음: 다음 글에서는 `30-relay-http-and-ops-surface.md`에서 이어지는 경계를 다룬다.
