# E-event-messaging-lab structure outline

## 글 목표

- 이 lab을 "Kafka demo"가 아니라 "outbox lifecycle demo"로 다시 정의한다.
- publish endpoint의 실제 의미가 broker delivery가 아니라 row state transition임을 분명히 적는다.
- build/config에 존재하는 messaging 무게와 runtime 구현 사이의 거리를 같이 보여 준다.

## 글 순서

1. controller/test를 보고 이 lab의 public contract가 outbox 상태 전이 중심이라는 점을 먼저 확정한다.
2. schema/entity/service를 따라가며 publish의 실제 동작을 설명한다.
3. Kafka dependency와 broker-free bootRun 재검증을 연결해 현재 범위를 닫는다.
4. retry/DLQ/worker/metadata 부재를 한계로 명시한다.

## 반드시 넣을 코드 앵커

- `EventMessagingController.publish()`
- `EventMessagingService.emitOrderPlaced()`
- `EventMessagingService.publishPending()`
- `OutboxEventEntity.markPublished()`
- `V2__outbox_events.sql`
- `EventMessagingApiTest.outboxEventLifecycleWorks()`

## 반드시 넣을 검증 신호

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/E-event-messaging-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test'

docker run --rm -u $(id -u):$(id -g) -p 18084:8080 \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/E-event-messaging-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew bootRun'
```

## 반드시 남길 한계

- publish가 external broker send가 아닌 상태 변경인 점
- Kafka dependency가 있어도 runtime path에서 실제로 사용되지 않는 점
- retry, DLQ, worker, delivery metadata가 아직 없는 점
