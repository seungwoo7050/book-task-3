# Problem — Game Store Capstone

## Target Position

- Junior Backend Engineer (Go)
- 평가 관점: "기술 과시"보다 "완성도 + 명확성 + 재현성"

## Product Scenario

플레이어가 아이템을 구매하면 시스템은 다음을 보장해야 한다.

1. 잔액 차감
2. 인벤토리 반영
3. 구매 기록 저장
4. 이벤트 발행 예약(outbox)

모든 단계는 중복 요청과 동시 요청에서도 일관성을 유지해야 한다.

## MVP Scope (필수)

### A. API

1. `GET /v1/healthcheck`
2. `POST /v1/purchases`
3. `GET /v1/purchases/{id}`
4. `GET /v1/players/{id}/inventory`

### B. Consistency

1. `Idempotency-Key` 헤더 기반 중복 요청 안전 처리
2. 잔액 차감 시 낙관적 잠금(`version`)
3. 직렬화 충돌(예: SQLSTATE `40001`) 재시도 정책

### C. Event Flow

1. purchase 성공 시 outbox row 기록
2. relay worker가 미발행 이벤트를 읽어 publisher 호출
3. 발행 성공 시 `published_at` 마킹

### D. Ops Basics

1. 요청/에러 구조화 로그(`log/slog`)
2. 간단한 rate limiting 미들웨어
3. graceful shutdown (API + relay)

## Out of Scope (이번 과제 제외)

- 서비스 분리(마이크로서비스)
- 복잡한 권한/인증 체계(OAuth 등)
- 분산 트레이싱/서비스 메시
- 멀티 리전 운영

## Data Model (MVP)

1. `players(id, name, balance, version, created_at)`
2. `catalog_items(id, sku, name, price, created_at)`
3. `purchases(id, player_id, item_id, price, created_at)`
4. `inventories(id, player_id, item_id, qty, updated_at)`
5. `idempotency_keys(key, request_hash, response_json, created_at)`
6. `outbox(id, aggregate_id, event_type, payload_json, created_at, published_at)`

## Non-Functional Requirements (필수 3개)

1. Reliability: 중복 요청 시 동일 결과 반환
2. Maintainability: handler/service/repository 계층 분리
3. Testability: 핵심 도메인 로직 table-driven tests

## Evaluation Criteria

| Criteria | Weight |
|---|---:|
| 트랜잭션/멱등성/잠금 정확성 | 35% |
| Outbox 릴레이 안정성 | 20% |
| 코드 구조/가독성 | 20% |
| 테스트 품질 | 15% |
| 문서/재현성 | 10% |

## Delivery Checklist

- [ ] 실행 가이드 (`README`)
- [ ] API 예시 (`curl`)
- [ ] 장애/재시도 동작 설명
- [ ] 테스트 실행 결과
