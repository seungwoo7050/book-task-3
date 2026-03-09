# Problem Framing

## Goal

`study2/labs/E-event-messaging-lab`의 목표는 Spring 백엔드가 request-response만으로 끝나지 않을 때 어떤 경계를 가져야 하는지 보여주는 것이다. outbox table, domain event creation, publish/consume flow, duplicate handling, retry boundary는 마이크로서비스 이전에도 필요한 기본 패턴이다. 최소 성공 조건은 현재 scaffold가 outbox와 Kafka-oriented flow를 설명 가능하게 만들고, 아직 빠진 long-running publisher와 DLQ를 솔직하게 남기는 것이다.

## Inputs and constraints

- Java/Spring:
  - Java 21
  - Spring Boot 3.4.x
  - Spring Kafka
- Services:
  - PostgreSQL
  - Redpanda
- Correctness requirements:
  - durable outbox row
  - publish/consume reasoning
  - duplicate handling awareness
- Repository givens:
  - current status는 `verified scaffold`
  - no long-running publisher worker yet
- Decisions still needed:
  - 실제 Kafka consumer를 언제 필수로 붙일지

## Success criteria

- outbox persistence가 request path와 구분되어 설명돼야 한다.
- Kafka-oriented message flow가 Compose와 docs에서 보여야 한다.
- commands가 통과해야 한다.
- DLQ/retry가 아직 conceptual이라는 점을 숨기지 않아야 한다.

## Uncertainty log

- scaffold만으로 message reliability를 충분히 체감할 수 있는지는 약하다.
- 그래도 outbox boundary를 먼저 배우는 것이 낫다고 가정했다.
- capstone이나 후속 개선에서 real consumer contract를 더 깊게 검증해야 한다.

