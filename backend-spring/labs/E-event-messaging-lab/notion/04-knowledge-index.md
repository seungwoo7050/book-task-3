# Knowledge Index — 이벤트 메시징 개념 사전

## 재사용 가능한 개념들

### Outbox 패턴

DB 트랜잭션과 메시지 발행 사이의 원자성(atomicity)을 보장하기 위한 패턴이다. 핵심 아이디어는 단순하다: 이벤트를 Kafka에 바로 보내는 대신, DB의 outbox 테이블에 저장한다. 이 저장은 비즈니스 로직의 DB 트랜잭션과 같은 트랜잭션에서 일어나므로, "비즈니스는 성공했는데 이벤트는 유실된" 상태가 발생하지 않는다.

이 랩에서의 구현:
```java
@Transactional
public EventResponse emitOrderPlaced(String orderId) {
    // 이 save는 비즈니스 트랜잭션의 일부
    OutboxEventEntity entity = outboxEventRepository.save(
        new OutboxEventEntity("ORDER", orderId, "ORDER_PLACED",
            "{\"orderId\":\"" + orderId + "\"}", "PENDING"));
    return EventResponse.from(entity);
}
```

outbox 행이 DB에 존재한다는 것 자체가 "이 이벤트는 반드시 발행되어야 한다"는 계약이다. 별도의 프로세스(scheduled publisher)가 이 행을 읽어서 실제 Kafka에 발행하고, 성공하면 PUBLISHED로 전환한다.

### Publish-Oriented Flow

요청 처리의 결과를 "무엇을 반환할 것인가"가 아니라 "어떤 이벤트를 발생시킬 것인가"로 바라보는 설계 관점이다. 주문이 접수되면 `ORDER_PLACED` 이벤트를 생성하고, 이 이벤트가 다른 시스템(결제, 재고, 알림)으로 전달되는 것이 핵심 흐름이 된다.

이 관점에서 HTTP 응답은 "이벤트가 성공적으로 생성되었다"는 확인이지, 모든 후속 처리가 완료되었다는 의미가 아니다. 이것이 request-response와 event-driven의 근본적인 차이다.

### DLQ(Dead Letter Queue) 사고방식

재처리가 불가능한 메시지를 별도로 격리해서 관찰하는 전략이다. 메시지 처리가 실패할 때 무한 재시도 대신, 일정 횟수 실패 후 DLQ 토픽으로 보내서 사람이 검토할 수 있게 한다.

이 랩에서는 아직 구현되지 않았지만, outbox의 status 필드를 확장하면 자연스럽게 도입할 수 있다: PENDING → PUBLISHED (성공), PENDING → FAILED (발행 실패), FAILED → DLQ (재시도 한도 초과).

### Event Sourcing과의 차이

Outbox 패턴과 Event Sourcing은 다르다. Event Sourcing은 상태를 이벤트의 시퀀스로 재구성하는 설계이고, Outbox는 기존 CRUD 시스템에서 이벤트를 안전하게 외부로 전달하기 위한 전술적 패턴이다. 이 랩은 Event Sourcing이 아니다 — outbox_events 테이블은 발행을 위한 임시 저장소이지, 시스템의 진실 원본(source of truth)이 아니다.

## 용어 사전

- **Broker**: Producer와 consumer 사이에서 메시지를 전달하는 시스템. Kafka, RabbitMQ, Redpanda 등이 있다. 이 랩에서는 Redpanda(Kafka 호환)를 사용한다.

- **Outbox row**: 아직 발행되지 않았거나 발행 이력을 담는 durable 이벤트 레코드. aggregate_type, aggregate_id, event_type, payload, status 필드를 가진다.

- **Aggregate type / Aggregate ID**: 이벤트가 어떤 도메인 객체에서 발생했는지를 식별하는 정보. "ORDER" / "ORDER-1"처럼 사용한다. 이 필드들이 있으면 나중에 특정 aggregate의 이벤트만 필터링하거나, topic routing에 사용할 수 있다.

- **Redpanda**: Apache Kafka와 호환되는 스트리밍 플랫폼. JVM 없이 C++로 작성되어 Zookeeper도 필요 없고, 단일 컨테이너로 동작한다. 로컬 개발 환경에 적합하다.

- **Consumer group**: 같은 토픽에서 메시지를 소비하는 consumer들의 논리적 그룹. 그룹 내에서 파티션이 분배되어 병렬 처리가 가능하다. 이 랩에서는 아직 consumer가 없다.

- **Idempotency**: 같은 연산을 여러 번 실행해도 결과가 달라지지 않는 성질. 메시징에서는 같은 이벤트가 두 번 발행되거나 소비되었을 때 시스템이 일관성을 유지하는 것이 중요하다.

## 참고 자료

- **E-event-messaging-lab docs/README.md** — 현재 구현(outbox, event creation, lifecycle), 단순화(no publisher worker, state transition only), 다음 개선(scheduled publisher, real Kafka records)이 정리되어 있다.
- **problem/README.md** — "Show how a Spring backend can move from request-response only logic toward event-driven integration without jumping straight to microservices."
- **Microservices Patterns (Chris Richardson)** — Outbox 패턴, Saga 패턴, Event Sourcing의 차이를 체계적으로 설명하는 참고서.

