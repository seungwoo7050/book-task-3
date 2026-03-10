# Retrospective — 메모리 데모에서 저장소 기반 흐름으로

## 좋아진 것: v1과의 거리

`commerce-backend`(v1)은 "이런 것들을 하나의 도메인에 넣을 수 있다"는 방향을 보여주는 scaffold였다. v2는 그 방향을 따라가되, 실제 저장소 기반 흐름을 만들었다. 인증은 DB-hashed refresh token과 CSRF header를 거치고, 주문은 checkout 트랜잭션에서 재고를 예약하고, 결제 확인은 idempotency key로 중복을 방지하며, 알림은 outbox → Kafka → notification 테이블로 저장된다. v1에서 메모리 데모로 존재하던 것들이 이제 PostgreSQL, Redis, Kafka를 거쳐 연결된다.

`CartStore` 추상화는 인터뷰에서 설명하기 좋은 선택이 되었다. "왜 Redis를 썼나?"에 대해 "장바구니는 DB에 넣기엔 일시적이고, 세션에 넣기엔 영속이 필요하다"라고 답할 수 있다. 동시에 "왜 Redis를 상품 캐시에는 안 썼나?"에 대해 "캐시 무효화 설명 비용이 포트폴리오 범위를 넘긴다"라고 답할 수 있다. Redis와 Kafka를 **어디에만 쓸지 제한한 판단**이 프로젝트를 덜 산만하게 만들었다.

테스트 품질도 올라갔다. MockMvc 시나리오 테스트(`CommercePortfolioApiTest`)만 있는 것이 아니라, Testcontainers 기반 메시징 테스트(`CommerceMessagingIntegrationTest`)까지 추가되어 "outbox → Kafka → notification 저장"을 한 번은 끝까지 연결해봤다는 증거가 생겼다.

## 여전히 약한 것

약한 부분은 세 가지 계층에 걸쳐 있다.

**외부 연동의 깊이.** Google OAuth는 authorize/callback contract를 mock으로 흉내 낸 수준이다. 실 provider 설정, token 갱신 실패, 계정 연동 해제 같은 edge case는 다루지 않는다. 결제도 mock-only라서 PG사 timeout, 중복 callback, 보상 처리까지 가지 못한다. 이 두 가지는 실제 sandbox 연동을 해야만 증명 가능한 영역이다.

**운영 측면의 미검증.** health/readiness와 Compose는 검증했지만, Kafka consumer를 장시간 돌렸을 때의 안정성이나 실제 AWS 배포는 증명하지 않았다. Docker Compose로 로컬에서 돌리는 것과 ECS/EKS에서 운영하는 것 사이에는 상당한 거리가 있다.

**도메인 경계의 인위성.** 이 프로젝트는 커머스 전체가 아니라 "포트폴리오에 필요한 경계"로 잘라낸 버전이다. 쿠폰, 배송, 환불, 정산은 의도적으로 제외했다. 면접에서 "왜 이것만?"이라는 질문이 나올 수 있고, "깊이와 범위의 균형"이라고 답할 근거는 있지만 한계를 인지하고 있어야 한다.

## 다시 한다면

**단기: 주문 취소 API.** `PENDING_PAYMENT` 단계에서만 주문 취소를 허용하는 customer API를 추가하고, reservation release를 테스트로 고정한다. 현재 상태 전이는 `PENDING_PAYMENT` → `PAID`만 있는데, 취소 → 재고 반환 흐름이 추가되면 상태 머신의 설명 가능성이 훨씬 올라간다.

**중기: CDC 기반 outbox.** 현재 outbox publisher는 polling 방식이다. Debezium 같은 CDC 기반 접근이 어떤 차이를 만드는지 — polling의 지연 vs CDC의 인프라 복잡성 — 을 정리해 볼 가치가 있다.

**설계 재고: OrderService와 PaymentService의 책임 분리.** 지금도 읽히지만, 결제 관련 규칙이 더 늘어나면 두 서비스의 상태 전이 로직이 서로 얽힐 가능성이 있다. 더 명시적인 application service 조합이나 domain event layer로 분리했다면, 결제 확인 → 주문 상태 전이 → outbox 삽입 흐름이 한 곳에서 읽혔을 것이다.
