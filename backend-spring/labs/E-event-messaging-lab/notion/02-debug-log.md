# Debug Log — "Kafka를 쓴다"는 말이 만드는 과장

## 이 랩에서 만난 위험

이 랩의 핵심 문제는 runtime crash보다 “Kafka를 쓴다”는 표현이 실제 구현보다 더 크게 들리는 것이다.

build.gradle.kts에 `spring-kafka`가 있고, compose.yaml에 Redpanda가 있으며, outbox 테이블에 `aggregate_type`, `event_type` 같은 필드가 있다. 이 키워드들만 보면 마치 본격적인 이벤트 드리븐 아키텍처를 구현한 것 같다. 하지만 실제로 Kafka 토픽에 메시지를 발행하는 코드는 없고, consumer도 없고, 재시도 정책도 없다.

## 어떤 과정에서 이 문제를 인식했는가

docs/README.md를 작성할 때, "Kafka delivery is represented by state transition rather than a real topic consumer contract"라는 문장을 적으면서 이 간극을 명확히 인식했다. outbox의 status가 PENDING에서 PUBLISHED로 바뀌는 것이 현재의 "발행"이다. 실제 Kafka 토픽에 record를 보내는 것이 아니다.

이것은 D-data-jpa-lab에서 Querydsl이 설치되어 있지만 사용되지 않는 것과 같은 구조의 문제다. 기술 이름이 실제 구현 깊이보다 앞서 있다. 메시징 영역에서는 이 과장이 특히 위험한데, "이벤트 드리븐"이라는 말이 마이크로서비스 아키텍처까지 연상시키기 때문이다.

## 대응 방법

docs/README.md에서 현재 증명된 것과 아직 증명되지 않은 것을 명확히 분리했다.

현재 증명된 것:
- outbox 테이블에 이벤트가 PENDING 상태로 저장된다
- publish 호출로 PENDING → PUBLISHED 전환이 일어난다
- `EventMessagingApiTest`에서 이 생명주기가 검증된다

아직 증명되지 않은 것:
- scheduled publisher가 주기적으로 PENDING 이벤트를 Kafka에 발행하는 것
- consumer가 토픽에서 메시지를 읽고 처리하는 것
- 발행 실패 시 재시도하거나 DLQ로 보내는 것
- 중복 발행/소비에 대한 idempotency 처리

"Redpanda가 Compose에 있으니까 메시징 인프라는 준비된 것"이라고 생각할 수 있지만, 인프라가 있다는 것과 그 인프라를 통해 실제 메시지가 흐른다는 것은 다른 이야기다.

## 검증 방법

```bash
make test
# EventMessagingApiTest.outboxEventLifecycleWorks():
# 1. POST /api/v1/orders/ORDER-1/events → status: PENDING
# 2. POST /api/v1/outbox-events/publish → status: PUBLISHED
# 3. GET /api/v1/outbox-events → eventType: ORDER_PLACED

docker compose up --build
# Redpanda, PostgreSQL, Redis, Mailpit, 앱이 모두 기동되는지 확인
```

테스트는 H2 in-memory에서 실행되므로 Redpanda가 없어도 통과한다. 이것 자체가 "현재 코드가 Kafka에 의존하지 않는다"는 증거이기도 하다.

## 후속으로 남은 부채

- **Scheduled publisher**: `@Scheduled`나 별도 워커로 PENDING 이벤트를 실제 발행
- **Consumer 코드**: `@KafkaListener`로 토픽에서 메시지 소비
- **발행 실패 메타데이터**: FAILED, RETRY_PENDING 상태 확장
- **Idempotency key**: 중복 발행/소비 방지 메커니즘

