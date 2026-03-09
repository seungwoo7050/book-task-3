# Knowledge Index

## Reusable concepts

### Refresh token hashing

- one-sentence definition:
  - refresh token 원문 대신 hash를 DB에 저장해 탈취 시 직접 재사용을 어렵게 만드는 방식이다.
- where it appears in this lab:
  - `auth` 모듈의 `RefreshTokenEntity`, `HashingSupport`, `AuthService.refresh`
- where it should reappear in later labs or the capstone:
  - 다른 Spring 인증 프로젝트나 FastAPI auth 설계에서도 그대로 재사용 가능하다.

### Optimistic locking for inventory

- one-sentence definition:
  - 같은 상품 재고를 동시에 수정할 때 version 충돌로 stale write를 막는 방식이다.
- where it appears in this lab:
  - `ProductEntity.version`, `OrderService.checkout`
- where it should reappear in later labs or the capstone:
  - 재고, 좌석 예약, 쿠폰 발급처럼 경쟁이 있는 모든 write path

### Idempotency key

- one-sentence definition:
  - 같은 요청이 중복 도착해도 한 번만 반영되도록 요청 식별자를 저장하는 방식이다.
- where it appears in this lab:
  - `/api/v1/payments/mock/confirm`, `payments.idempotency_key`
- where it should reappear in later labs or the capstone:
  - 결제, webhook 처리, 외부 API callback 수신

### Outbox pattern

- one-sentence definition:
  - DB 변경과 메시지 발행 사이의 불일치를 줄이기 위해 이벤트를 먼저 DB에 적재하고 별도 publisher가 내보내는 방식이다.
- where it appears in this lab:
  - `outbox_events`, `PaymentService`, `OutboxPublisher`
- where it should reappear in later labs or the capstone:
  - 주문 완료, 이메일 발송, 알림 발행, 감사 로그 전달

### Selective Redis usage

- one-sentence definition:
  - 모든 상태를 Redis로 옮기지 않고, 짧은 TTL 또는 빠른 변경이 필요한 상태에만 제한적으로 쓰는 판단이다.
- where it appears in this lab:
  - cart 저장소와 auth attempt limiter
- where it should reappear in later labs or the capstone:
  - 캐시, rate limiting, ephemeral session-like state

## Glossary

- modular monolith:
  - 하나의 배포 단위지만 코드 내부 모듈 경계를 명확히 두는 구조를 뜻한다.
- persisted flow:
  - 요청 처리 결과가 메모리 데모가 아니라 DB나 외부 저장소에 남는 실제 데이터 흐름을 뜻한다.
- compensation:
  - 이미 반영한 작업을 되돌리기 위해 별도 보상 동작을 수행하는 것을 뜻한다. 이 캡스톤에서는 reservation release가 가장 가까운 예다.
- dedup key:
  - 같은 이벤트를 여러 번 처리하지 않기 위해 저장하는 중복 제거 식별자다.

## References

### Reference 1

- title:
  - commerce-backend-v2 Spring README
- URL or local path:
  - `/Users/woopinbell/work/web-pong/study2/capstone/commerce-backend-v2/spring/README.md`
- checked date:
  - `2026-03-09`
- why it was consulted:
  - 공개 README와 실제 구현 범위를 맞추기 위해 확인했다.
- what was learned:
  - 구현된 API surface와 known tradeoff를 추적 문서에도 같은 톤으로 유지해야 한다는 점을 확인했다.
- what changed in the code or design because of it:
  - Notion 초안에서도 “production-ready”가 아니라 “portfolio-grade study project”라는 표현을 고정했다.

### Reference 2

- title:
  - commerce-backend-v2 Verification
- URL or local path:
  - `/Users/woopinbell/work/web-pong/study2/capstone/commerce-backend-v2/docs/verification.md`
- checked date:
  - `2026-03-09`
- why it was consulted:
  - 초안 문서에 넣을 검증 근거를 실제 실행 명령 기준으로 맞추기 위해 확인했다.
- what was learned:
  - `make test`에는 Testcontainers messaging test가 포함되므로 Docker 전제조건을 명시해야 한다.
- what changed in the code or design because of it:
  - `spring/README.md`에 Docker 가용성 전제 문장을 추가했다.

### Reference 3

- title:
  - OrderService implementation
- URL or local path:
  - `/Users/woopinbell/work/web-pong/study2/capstone/commerce-backend-v2/spring/src/main/java/com/webpong/study2/app/order/application/OrderService.java`
- checked date:
  - `2026-03-09`
- why it was consulted:
  - 주문 상태 전이, reservation 생성/해제 규칙을 정확하게 적기 위해 확인했다.
- what was learned:
  - checkout에서 stock reserve와 order/item/reservation 생성을 한 트랜잭션 안에서 묶고 있다는 점이 이 캡스톤의 핵심이다.
- what changed in the code or design because of it:
  - domain/state 문서와 Notion의 문제 정의에서 “payment보다 checkout 시점에 stock을 먼저 잡는다”는 설명을 명확히 넣었다.

### Reference 4

- title:
  - PaymentService implementation
- URL or local path:
  - `/Users/woopinbell/work/web-pong/study2/capstone/commerce-backend-v2/spring/src/main/java/com/webpong/study2/app/payment/application/PaymentService.java`
- checked date:
  - `2026-03-09`
- why it was consulted:
  - idempotency, order-paid outbox insertion, notification fallback 로직을 확인하기 위해 봤다.
- what was learned:
  - messaging feature flag가 꺼진 로컬 테스트 환경에서는 synchronous notification fallback이 작동한다.
- what changed in the code or design because of it:
  - 테스트 설계를 “기본 테스트는 fallback, 통합 테스트는 Kafka”로 분리했다.

### Reference 5

- title:
  - compose health probe helper
- URL or local path:
  - `/Users/woopinbell/work/web-pong/tools/compose_probe.sh`
- checked date:
  - `2026-03-09`
- why it was consulted:
  - 문서의 Compose 검증 근거가 실제로 어떤 수준인지 확인하기 위해 봤다.
- what was learned:
  - 현재 Compose 검증은 live/ready health probe 중심이며, 도메인 시나리오까지 자동 검증하지는 않는다.
- what changed in the code or design because of it:
  - 문서와 회고에서 Compose 검증 범위를 과장하지 않도록 표현을 조정했다.
