# 접근 기록 — 6개 패키지로 구성된 캡스톤

## 패키지 구조 설계

```
internal/
├── config/     → 환경 변수 기반 설정
├── domain/     → 순수 도메인 타입 (외부 의존 없음)
├── httpapi/    → HTTP 핸들러 + 미들웨어
├── repository/ → SQL 쿼리 (database/sql)
├── service/    → 비즈니스 로직 조율
├── relay/      → Outbox 폴링 + 발행
└── txn/        → 트랜잭션 재시도 헬퍼
```

`internal/`을 사용해 외부 패키지에서 import할 수 없도록 했다.

## domain: 순수 타입

`Player`, `CatalogItem`, `Purchase`, `InventoryItem`, `IdempotencyRecord`, `OutboxEvent` — 모두 plain struct. JSON 태그만 있고 메서드나 외부 의존은 없다. domain 패키지가 다른 패키지를 import하지 않으므로 순환 의존이 원천 차단된다.

## repository: Store 패턴

하나의 `Store` struct에 모든 SQL 접근을 모았다. 프로젝트 14에서는 패키지 수준 함수였지만, 캡스톤에서는 `Store`에 메서드로 묶었다. 이유: 테스트에서 인터페이스로 대체하기 위해.

핵심 메서드:
- `GetPlayer`, `GetCatalogItem` — 조회
- `DeductBalance(ctx, tx, playerID, amount, version)` — 낙관적 잠금
- `CreatePurchase`, `UpsertInventory` — 구매/인벤토리
- `InsertOutboxEvent` — 트랜잭션 내 Outbox INSERT
- `InsertIdempotencyKey`, `GetIdempotencyKey` — 멱등성 키
- `ListUnpublishedOutbox`, `MarkOutboxPublished` — Relay용

모든 쓰기 메서드는 `*sql.Tx`를 인자로 받는다.

## service: PurchaseService와 QueryService

### PurchaseService.Purchase

`txn.RunInTx` 안에서 7단계:
1. 멱등성 키 확인 → 있고 hash 일치하면 캐시 반환, hash 불일치면 `ErrIdempotencyKeyConflict`
2. 플레이어 조회
3. 카탈로그 아이템 조회 + 잔액 체크
4. 잔액 차감 (낙관적 잠금)
5. 구매 이력 INSERT + 인벤토리 UPSERT
6. Outbox 이벤트 INSERT
7. 멱등성 키 INSERT

`request_hash`로 같은 멱등성 키에 다른 요청이 왔을 때를 감지한다. SHA256으로 `playerID|itemID`를 해시.

### 멱등성 키 충돌 처리

동시 요청이 같은 멱등성 키로 INSERT할 때 `ErrIdempotencyKeyExists` → `retryableTxError` 반환. `SQLState()` 메서드를 구현해서 `txn.RunInTx`가 40001과 동일하게 재시도.

### QueryService

읽기 전용: `GetPurchase`, `GetPlayerInventory`. 트랜잭션 없이 `*sql.DB`에서 직접 조회.

## httpapi: 핸들러와 미들웨어

4개 엔드포인트:
- `GET /v1/healthcheck`
- `POST /v1/purchases` — `Idempotency-Key` 헤더 필수
- `GET /v1/purchases/{id}`
- `GET /v1/players/{id}/inventory`

미들웨어 체인: `loggingMiddleware` → `rateLimitMiddleware` → `mux`

#### RateLimiter

Fixed-Window 방식. 프로젝트 11에서 Token Bucket을 구현했지만, 캡스톤에서는 단순화. `time.Second` 윈도우 내 요청 수를 세고 `limit`을 초과하면 429 반환.

## relay: 인터페이스 기반 설계

`OutboxStore`와 `Publisher` 두 인터페이스를 정의. repository의 구체 타입에 의존하지 않음. 테스트에서 mock Publisher를 주입할 수 있다. `PollOnce`가 공개 메서드라 단위 테스트에서 ticker 없이 한 배치를 직접 실행 가능.

## txn: 재사용

프로젝트 14의 `txn/retry.go`를 거의 그대로 가져왔다. `PgError` 인터페이스, `IsRetryable`, `RunInTx`. 검증된 코드를 재사용하는 것도 캡스톤의 의미.
