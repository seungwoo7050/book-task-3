# E-event-messaging-lab Evidence Ledger

- 복원 기준:
  - `problem/README.md`, `docs/README.md`, outbox entity/service/controller, MockMvc 테스트, `2026-03-13` 재실행 CLI를 바탕으로 chronology를 재구성했다.
- 기존 blog 처리:
  - 기존 `blog/`가 없어 격리할 대상은 없었다.

## Phase 1

- 시간 표지: Phase 1
- 당시 목표:
  - 이벤트 랩의 중심을 "브로커 사용"이 아니라 "이벤트 경계"로 고정한다.
- 변경 단위:
  - `problem/README.md`
  - `docs/README.md`
  - `spring/README.md`
- 처음 가설:
  - 분산 시스템 키워드를 먼저 꺼내면 outbox가 왜 필요한지보다 Kafka 자체가 전면에 나온다.
- 실제 조치:
  - 도메인 변경 사실을 outbox record로 남기고, publish는 다른 단계로 넘기는 랩으로 scope를 고정했다.
  - DLQ, retry, long-running worker는 현재 단계에서 제외했다.
- CLI:

```bash
cp .env.example .env
make run
```

- 검증 신호:
  - `spring/README.md`는 VSCode 터미널 기준 진입점을, docs는 pending -> published lifecycle과 Redpanda-ready 환경을 현재 증명 범위로 기록한다.
- 핵심 코드 앵커:
  - `OutboxEventEntity`, `EventMessagingService`, `EventMessagingApiTest`가 이 랩의 중심 근거가 된다.
- 새로 배운 것:
  - 이벤트 시스템의 첫 단계는 consumer가 아니라 "이벤트를 안전하게 기록하는 위치"를 정하는 일이다.
- 다음:
  - order event 생성과 publish boundary를 코드에서 분리한다.

## Phase 2

- 시간 표지: Phase 2
- 당시 목표:
  - 이벤트 생성과 publish를 서로 다른 상태 전이로 만든다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/events/domain/OutboxEventEntity.java`
  - `spring/src/main/java/com/webpong/study2/app/events/application/EventMessagingService.java`
  - `spring/src/main/java/com/webpong/study2/app/events/api/EventMessagingController.java`
- 처음 가설:
  - emit 단계에서 `PENDING`을 남기고, publish 단계에서만 `PUBLISHED`로 바꾸면 브로커 handoff의 의미가 분명해진다.
- 실제 조치:
  - `/orders/{orderId}/events`는 `ORDER_PLACED` outbox row를 `PENDING`으로 저장한다.
  - `/outbox-events/publish`는 pending row들을 찾아 `markPublished()`를 호출한다.
  - `/outbox-events`는 현재 outbox 상태를 그대로 보여 준다.
- CLI:

```bash
make test
```

- 검증 신호:
  - `2026-03-13` 재실행에서 `make test`가 `BUILD SUCCESSFUL`로 끝났다.
- 핵심 코드 앵커:

```java
outboxEventRepository.save(
    new OutboxEventEntity(
        "ORDER", orderId, "ORDER_PLACED", "{\"orderId\":\"" + orderId + "\"}", "PENDING"));
```

- 새로 배운 것:
  - 이벤트 경계는 "메시지를 보냈다"가 아니라 "도메인 변경 사실을 DB에 먼저 남겼다"에서 시작한다.
- 다음:
  - 이 상태 전이가 테스트와 CLI에서 실제로 어떻게 보이는지 확인한다.

## Phase 3

- 시간 표지: Phase 3
- 당시 목표:
  - outbox row가 `PENDING -> PUBLISHED`로 이동하는 과정을 API 수준에서 증명한다.
- 변경 단위:
  - `spring/src/test/java/com/webpong/study2/app/EventMessagingApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`
- 처음 가설:
  - emit -> publish -> list 순서만 고정해도 "이벤트 생성"과 "브로커 handoff"가 다른 문제라는 점이 충분히 드러난다.
- 실제 조치:
  - `ORDER-1`에 대한 event emit 호출이 `PENDING`을 반환하는지 검증했다.
  - publish 호출 이후 list에서 같은 event가 `ORDER_PLACED`, `PUBLISHED` 상태로 보이는지 확인했다.
- CLI:

```bash
make test
make smoke
docker compose up --build
```

- 검증 신호:
  - `2026-03-13` 재실행 후 XML 리포트 4개, `failures=0`이 확인됐다.
  - `2026-03-09` 검증 기록에는 lint/test/smoke/Compose health 확인 통과가 남아 있다.
- 핵심 코드 앵커:

```java
pending.forEach(OutboxEventEntity::markPublished);
```

- 새로 배운 것:
  - 이벤트 시스템을 설명할 때 publish 성공 여부보다 중요한 건 outbox row가 어떤 상태 이름으로 이동하느냐다. 그 이름이 retry와 replay 논의의 출발점이 된다.
- 다음:
  - scheduled publisher, real Kafka publish/consume, failure metadata는 다음 단계로 남긴다.
