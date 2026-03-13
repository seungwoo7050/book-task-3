# outbox row를 먼저 남겨야 이벤트 경계가 보인다

`E-event-messaging-lab`은 이벤트를 보내는 순간보다, 이벤트를 언제 "기록된 사실"로 인정하는지가 더 중요하다고 보는 랩이다. order change를 DB에 `PENDING`으로 먼저 남기고, 그 다음에야 publish를 시도해야 request-response 밖의 흐름을 설명할 수 있다. macOS + VSCode 통합 터미널에서 `make test`를 다시 돌리면 이 설계가 테스트 한 흐름 안에서 아주 선명하게 보인다.

## 구현 순서 요약

- `problem/README.md`와 `docs/README.md`가 outbox boundary를 current scope로 고정한다.
- `OutboxEventEntity`가 이벤트 사실을 DB row로 표현한다.
- `EventMessagingService`가 emit과 publish를 다른 메서드로 분리한다.
- `EventMessagingApiTest`가 `PENDING -> PUBLISHED` lifecycle을 검증한다.

## Phase 1

### Session 1

- 당시 목표:
  - 이벤트 랩의 중심을 브로커가 아니라 outbox boundary로 정한다.
- 변경 단위:
  - `problem/README.md`
  - `docs/README.md`
  - `spring/README.md`
- 처음 가설:
  - worker, consumer, retry를 한 번에 넣으면 outbox가 왜 필요한지보다 비동기 시스템 전체가 전면에 나온다.
- 실제 진행:
  - current scope를 outbox table, order event 생성 endpoint, pending -> published lifecycle로 좁혔다.
  - Redpanda-ready Compose 환경은 "다음 단계"를 위한 자리로만 남겼다.

CLI:

```bash
cp .env.example .env
make run
```

검증 신호:

- `spring/README.md`가 VSCode 통합 터미널 기준 명령을 고정했고, docs는 long-running worker가 아직 없다는 점까지 같이 적어 두었다.

핵심 코드:

```java
@Table(name = "outbox_events")
public class OutboxEventEntity {
```

왜 이 코드가 중요했는가:

- 이 테이블 이름이 있어야 이벤트가 "메시지"가 아니라 "먼저 저장되는 사실"로 읽힌다. outbox의 출발점은 브로커가 아니라 persistence다.

새로 배운 것:

- 이벤트 설계의 첫 질문은 "누가 consume하나"가 아니라 "무엇을 durable fact로 남기나"다.

다음:

- emit과 publish를 서로 다른 메서드와 상태 전이로 나눈다.

## Phase 2

### Session 1

- 당시 목표:
  - 이벤트 생성과 publish handoff를 코드 구조에서 분리한다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/events/domain/OutboxEventEntity.java`
  - `spring/src/main/java/com/webpong/study2/app/events/application/EventMessagingService.java`
  - `spring/src/main/java/com/webpong/study2/app/events/api/EventMessagingController.java`
- 처음 가설:
  - emit에서 `PENDING`, publish에서 `PUBLISHED`로 상태를 바꾸면 비동기 경계가 설명 가능한 단위가 된다.
- 실제 진행:
  - `/orders/{orderId}/events`는 `ORDER_PLACED` row를 `PENDING`으로 저장한다.
  - `/outbox-events/publish`는 pending row만 찾아 `markPublished()`를 호출한다.
  - `/outbox-events`는 현재 outbox 상태를 그대로 노출한다.

CLI:

```bash
make test
```

검증 신호:

- `2026-03-13` macOS + VSCode 통합 터미널 재실행에서 `make test`가 `BUILD SUCCESSFUL`로 끝났다.

핵심 코드:

```java
public List<EventResponse> publishPending() {
  List<OutboxEventEntity> pending = outboxEventRepository.findByStatus("PENDING");
  pending.forEach(OutboxEventEntity::markPublished);
  return pending.stream().map(EventResponse::from).toList();
}
```

왜 이 코드가 중요했는가:

- publish를 단순 side effect로 숨기지 않고, 현재 pending row 집합을 상태 전이로 처리한다는 사실이 이 메서드에 그대로 들어 있다.

새로 배운 것:

- outbox 패턴을 이해하는 데 중요한 건 브로커 client API보다 "pending 집합을 언제 어떻게 비운다고 볼 것인가"다.

다음:

- emit -> publish -> list 순서를 테스트에 고정한다.

## Phase 3

### Session 1

- 당시 목표:
  - outbox lifecycle이 API 응답에서 직접 보이도록 검증한다.
- 변경 단위:
  - `spring/src/test/java/com/webpong/study2/app/EventMessagingApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`
- 처음 가설:
  - `ORDER-1` 한 건만으로도 event creation과 publish handoff를 충분히 증명할 수 있다.
- 실제 진행:
  - emit 호출에서 `PENDING`, publish 호출에서 `PUBLISHED`, list 호출에서 `ORDER_PLACED` event type을 차례로 확인했다.

CLI:

```bash
make test
make smoke
docker compose up --build
```

검증 신호:

- `2026-03-13` 재실행 후 XML 리포트 4개, `failures=0`이 확인됐다.
- `2026-03-09` 검증 기록에는 lint/test/smoke/Compose health 확인 통과가 남아 있다.

핵심 코드:

```java
mockMvc
    .perform(post("/api/v1/outbox-events/publish"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$[0].status").value("PUBLISHED"));
```

왜 이 코드가 중요했는가:

- publish가 성공했다는 말을 로그로만 남기지 않고, API 응답에서 상태 이름이 바뀌는 장면을 드러낸다. 이게 있어야 다음 단계의 worker나 Kafka 연결도 같은 언어로 설명할 수 있다.

새로 배운 것:

- 이벤트 시스템의 설명력은 결국 상태 이름에서 나온다. `PENDING`, `PUBLISHED` 같은 이름이 이후 retry와 replay 설계의 출발점이 된다.

다음:

- scheduled publisher, real Kafka publish/consume, failure metadata는 다음 확장 지점으로 남긴다.
