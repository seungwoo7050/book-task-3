# Retrospective — Outbox가 가르쳐 준 것

## 나아진 점

### Kafka를 "handoff boundary"로 바라보게 되었다

이 랩을 진행하기 전에는 Kafka를 "메시지를 보내고 받는 파이프"로만 생각했다. 하지만 E-event-messaging-lab을 거치면서 더 중요한 질문이 드러났다. "메시지를 어디서 만들고, 어떻게 안전하게 파이프에 넣느냐"이다.

Kafka 자체는 신뢰성 있는 브로커이다. 문제는 Kafka에 메시지를 넣기 전 단계다. DB 트랜잭션이 커밋된 후에 `KafkaTemplate.send()`가 실패하면, "비즈니스는 성공했는데 이벤트는 유실되는" 상황이 발생한다. Outbox 패턴은 이 간극을 메우기 위해 존재한다.

### Outbox를 먼저 배우는 순서가 맞았다

처음부터 Kafka consumer와 DLQ까지 구현하려 했다면, "왜 outbox가 필요한지"를 제대로 이해하기 전에 브로커 설정과 consumer group 관리에 빠졌을 것이다. outbox 테이블에 PENDING 행을 저장하고, 그것을 PUBLISHED로 전환하는 단순한 흐름을 먼저 경험한 것이 올바른 순서였다.

`emitOrderPlaced()` 메서드가 `@Transactional` 안에서 outbox 행을 저장할 때, "이 save가 비즈니스 로직과 같은 트랜잭션에 있다"는 것이 outbox 패턴의 전부이고 핵심이다. 이것을 먼저 체감한 후에 실제 발행으로 나아가는 것이 순서다.

### Compose에 Redpanda를 두니 로컬 실험 그림이 분명해졌다

Kafka를 로컬에서 띄우려면 Zookeeper까지 설정해야 하는 번거로움이 있다. Redpanda는 Kafka 프로토콜을 호환하면서도 단일 컨테이너로 동작하므로, compose.yaml 하나에 메시지 브로커를 포함시킬 수 있다. `KAFKA_BOOTSTRAP_SERVERS: redpanda:9092`만 설정하면 Spring Kafka가 Redpanda를 Kafka처럼 사용한다.

## 아직 약한 점

### Long-running publisher가 없다

현재 "발행"은 `/api/v1/outbox-events/publish` 엔드포인트를 수동으로 호출하는 것이다. 프로덕션에서는 이것을 사람이 호출할 수 없다. `@Scheduled`로 주기적으로 PENDING 행을 조회해서 Kafka에 발행하는 워커가 필요하다. 이 워커가 없으면 outbox는 이벤트를 쌓기만 하고 실제로 보내지 않는 게시판이 된다.

### DLQ와 재시도 정책이 개념 수준이다

발행이 실패했을 때 어떻게 할 것인가? 재시도 횟수, backoff 간격, 재시도가 불가능한 메시지를 DLQ로 보내는 전략 — 이것들이 모두 빠져 있다. "DLQ를 안다"고 말하려면 최소한 한 번은 직접 구현해 봐야 한다.

### Consumer contract 검증이 없다

메시지를 발행하는 쪽만 있고, 소비하는 쪽이 없다. `@KafkaListener`를 구현하고, 소비된 메시지를 처리하고, 처리 실패 시의 동작을 정의해야 메시징 흐름이 완성된다. 현재는 절반만 있는 상태이다.

## 다음에 다시 볼 것들

- **Scheduled publisher job**: 5초마다 PENDING 이벤트를 조회해서 Kafka에 발행하고, 성공하면 PUBLISHED로 전환, 실패하면 retry count를 증가시키는 구현
- **Kafka consumer integration test**: Testcontainers로 Redpanda를 띄우고, 실제 토픽에서 메시지를 소비하는 테스트. `spring-kafka-test`가 이미 의존성에 포함되어 있다.
- **Capstone의 order-paid flow와 비교**: capstone 프로젝트에서 주문 결제 이벤트가 어떻게 처리되는지와 이 랩의 outbox 접근을 비교하면, 패턴의 실제 적용을 볼 수 있다.

