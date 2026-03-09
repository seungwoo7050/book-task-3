# 문제 정의 — 배운 것을 하나로 엮는다

## 캡스톤이란

개별 기술을 익히는 것과 그것들을 조합해서 하나의 서비스를 만드는 것은 다르다. 프로젝트 01~16에서 각각 독립적으로 다뤘던 것들이 여기서 만난다:

- **HTTP API** (프로젝트 05, 06) → `httpapi/handler.go`
- **낙관적 잠금** (프로젝트 08, 14) → `repository/store.go`의 `DeductBalance`
- **멱등성 키** (프로젝트 14) → `service/purchase_service.go`
- **트랜잭션 재시도** (프로젝트 14) → `txn/retry.go`
- **Outbox 패턴** (프로젝트 15) → `relay/relay.go`
- **Rate Limiting** (프로젝트 11) → `httpapi/middleware.go`
- **구조화 로깅** (프로젝트 06, 09) → `slog`
- **Graceful Shutdown** (프로젝트 06) → `cmd/api/main.go`

## 시나리오

게임 스토어. 플레이어가 카탈로그 아이템을 구매하면:

1. 잔액 차감 (낙관적 잠금, `WHERE version = ?`)
2. 인벤토리 업데이트 (`ON CONFLICT DO UPDATE`)
3. 구매 이력 기록
4. Outbox 이벤트 삽입
5. 멱등성 키 저장

이 5단계가 하나의 CockroachDB 트랜잭션 안에서 실행된다.

## 주니어 백엔드 엔지니어의 평가 관점

문제 스펙이 명시한다: "기술 과시보다 완성도 + 명확성 + 재현성". 복잡한 아키텍처보다 확실하게 동작하는 서비스. 에러 처리가 빈틈없고, 재시도가 안전하고, 테스트로 증명할 수 있는 코드.

## 데이터 모델

6개 테이블: `players`, `catalog_items`, `purchases`, `inventories`, `idempotency_keys`, `outbox`

프로젝트 14의 4개 테이블에서 `catalog_items`(상품 마스터)와 `purchases`(구매 이력)가 추가됐다. `inventories`는 프로젝트 14의 `inventory`와 유사하지만 FK가 `catalog_items.id`를 가리킨다.
