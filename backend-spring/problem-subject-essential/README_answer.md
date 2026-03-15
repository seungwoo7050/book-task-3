# backend-spring 서버 개발 필수 답안지

이 문서는 Spring 트랙에서 서버 공통성이 가장 직접적인 세 랩을 실제 `spring` 소스 기준으로 정리한 답안지다. 핵심은 웹 프레임워크 문법보다, 이벤트 handoff, 캐시와 경합, 운영 표면을 각각 독립된 설계 문제로 분리해 읽는 데 있다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [e-event-messaging-lab-spring](e-event-messaging-lab-spring_answer.md) | 시작 위치의 구현을 완성해 도메인 변경 사실을 outbox record로 남기는 흐름이 존재한다, "이벤트 생성"과 "브로커 publish"를 다른 문제로 나눠 설명할 수 있다, Kafka/Redpanda가 왜 필요한지 handoff boundary 관점에서 설명 가능하다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/E-event-messaging-lab/spring && ./gradlew test` |
| [f-cache-concurrency-lab-spring](f-cache-concurrency-lab-spring_answer.md) | 시작 위치의 구현을 완성해 inventory 조회와 reservation 흐름에서 cacheable read path와 idempotency key 처리가 보인다, 같은 JVM 안에서의 동시성 제어가 재고 차감 문제와 연결된다, Redis나 분산 락을 왜 다음 단계로 남겼는지 설명할 수 있다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/F-cache-concurrency-lab/spring && ./gradlew test` |
| [g-ops-observability-lab-spring](g-ops-observability-lab-spring_answer.md) | 시작 위치의 구현을 완성해 health/readiness, JSON logging, trace ID, Prometheus scrape target이 존재한다, Compose와 CI가 "운영 기본기"로서 어떤 역할을 하는지 설명할 수 있다, 현재 증명한 범위와 아직 미완인 운영 영역이 문서에 분리되어 있다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/G-ops-observability-lab/spring && ./gradlew test` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
