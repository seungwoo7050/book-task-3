# Retrospective

## What improved

- 기존 `commerce-backend`가 보여주던 “통합 방향”은 유지하면서, 실제 저장소 기반 흐름이 생겼다. 이제 인증, 주문, 결제, 알림이 메모리 데모가 아니라 DB와 Redis, Kafka를 거쳐 연결된다.
- `CartStore` 추상화, outbox 패턴, refresh token hashing 같은 선택은 인터뷰에서 설명 가능한 수준으로 정리되었다. 특히 Redis와 Kafka를 어디에만 쓸지 제한한 판단이 프로젝트를 덜 산만하게 만들었다.
- 테스트 품질이 좋아졌다. MockMvc 시나리오 테스트만 있는 것이 아니라, Testcontainers 기반 메시징 테스트까지 추가되어 “한 번은 끝까지 연결해봤다”는 증거가 생겼다.

## What is still weak

- Google OAuth는 여전히 callback contract를 흉내 낸 수준이고, 실 provider 설정과 edge case를 다루지 않는다.
- 결제는 mock-only라서, 외부 PG 특유의 timeout, 중복 callback, 보상 처리까지는 다루지 못한다.
- 운영 측면에서도 health/readiness와 Compose는 검증했지만, 장기 실행 상태의 Kafka consumer 안정성이나 실제 AWS 배포는 증명하지 않았다.
- 도메인 자체도 커머스 전체가 아니라 “포트폴리오에 필요한 경계” 중심으로 잘라낸 버전이다. 쿠폰, 배송, 환불, 정산 같은 복잡도는 의도적으로 제외되어 있다.

## What to revisit

- one near-term follow-up:
  - 주문 취소를 `PENDING_PAYMENT` 단계에서만 허용하는 customer API를 추가하고, reservation release를 테스트로 고정한다.
- one deeper topic worth studying later:
  - outbox polling 대신 CDC 기반 접근이 어떤 차이를 만드는지 정리해 볼 가치가 있다.
- one thing you would redesign if you restarted the lab:
  - `OrderService`와 `PaymentService` 사이의 상태 전이 로직을 더 명시적인 application service 조합 또는 domain event layer로 분리했을 것이다. 지금도 읽히지만, 결제 관련 규칙이 더 늘어나면 서비스 책임이 비대해질 가능성이 있다.
