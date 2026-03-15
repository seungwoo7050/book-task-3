# E-event-messaging-lab evidence ledger

- 작성 기준일: 2026-03-14
- 복원 원칙: 기존 blog 본문은 입력 근거로 쓰지 않고, source, tests, build config, 재실행 결과만 사용했다.
- 핵심 근거: `problem/README.md`, `docs/README.md`, `spring/build.gradle.kts`, `spring/Makefile`, `EventMessagingController.java`, `EventMessagingService.java`, `OutboxEventEntity.java`, `OutboxEventRepository.java`, `V2__outbox_events.sql`, `EventMessagingApiTest.java`, `HealthApiTest.java`, `LabInfoApiSmokeTest.java`

## Phase 1. API contract와 테스트 기준 확인

- 목표: 이 lab이 실제 broker publish를 검증하는지, 아니면 outbox 상태 전이를 검증하는지 먼저 확인한다.
- 확인 파일:
  - `spring/src/main/java/com/webpong/study2/app/events/api/EventMessagingController.java`
  - `spring/src/test/java/com/webpong/study2/app/EventMessagingApiTest.java`
- 확인 결과:
  - API는 emit, publish, list 세 개뿐이다.
  - 테스트는 order event 생성 -> publish -> outbox list 확인만 다룬다.
  - topic, producer ack, consumer side assert는 없다.
- 핵심 앵커:

```java
mockMvc
    .perform(post("/api/v1/outbox-events/publish"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$[0].status").value("PUBLISHED"));
```

## Phase 2. schema와 service에서 publish 의미 확인

- 목표: publish가 실제 runtime에서 무엇을 하는지 확인한다.
- 확인 파일:
  - `spring/src/main/resources/db/migration/V2__outbox_events.sql`
  - `spring/src/main/java/com/webpong/study2/app/events/application/EventMessagingService.java`
  - `spring/src/main/java/com/webpong/study2/app/events/domain/OutboxEventEntity.java`
- 확인 결과:
  - outbox schema에는 payload와 status만 있고, retry/failure/timestamp metadata가 없다.
  - `emitOrderPlaced()`는 JSON payload 문자열을 직접 조합해 `PENDING` row를 저장한다.
  - `publishPending()`은 `findByStatus("PENDING")` 후 `markPublished()`만 수행한다.
- 핵심 앵커:

```java
pending.forEach(OutboxEventEntity::markPublished);
```

- 메모:
  - KafkaTemplate이나 producer client 호출이 없다.
  - publish는 row state transition이지 external delivery가 아니다.

## Phase 3. Kafka dependency와 실제 runtime 거리 확인

- 목표: 문서가 말하는 Kafka-oriented structure가 runtime에서 어디까지 실제인지 확인한다.
- 확인 파일:
  - `spring/build.gradle.kts`
  - `spring/src/main/resources/application.yml`
- 확인 결과:
  - build에는 `spring-kafka`와 kafka testcontainers가 들어 있다.
  - config에는 `spring.kafka.bootstrap-servers`가 있다.
  - 하지만 main source에서 Kafka client/API 사용 흔적은 없다.
- 메모:
  - 2026-03-14 `bootRun`은 Kafka/Redpanda 없이 정상 기동했다.
  - 즉 현재 runtime은 broker-independent하다.

## Phase 4. 2026-03-14 재실행 검증

- lint:

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/E-event-messaging-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'
```

- 결과: `BUILD SUCCESSFUL in 1m 29s`

- test:

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/E-event-messaging-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test'
```

- 결과: `BUILD SUCCESSFUL in 1m 22s`

- smoke:

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/E-event-messaging-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test --tests "*SmokeTest"'
```

- 결과: `BUILD SUCCESSFUL in 1m 15s`

- manual boot run:

```bash
docker run --rm -u $(id -u):$(id -g) -p 18084:8080 \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/E-event-messaging-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew bootRun'
```

- manual HTTP checks:
  - initial `GET /api/v1/outbox-events` -> `[]`
  - emit `ORDER-1` -> `PENDING`
  - emit `ORDER-2` -> `PENDING`
  - first `POST /api/v1/outbox-events/publish` -> 두 row 모두 `PUBLISHED`
  - second `POST /api/v1/outbox-events/publish` -> `[]`
  - final `GET /api/v1/outbox-events` -> 두 row 모두 `PUBLISHED`
  - `GET /api/v1/health/live` -> `200`, `X-Trace-Id` 확인

## 이번 Todo의 결론

- 이 lab은 outbox boundary 설명에는 성공하지만, broker integration을 구현한 단계는 아니다.
- 문서에 반드시 남겨야 할 현재 한계:
  - Kafka/Redpanda 없이도 동일하게 동작하는 local status transition
  - retry, DLQ, failure metadata 부재
  - payload와 delivery metadata를 외부에서 관찰할 표면 부재
