# E-event-messaging-lab evidence ledger

- 복원 방식: 세밀한 세션 기록 대신 `Phase 1 -> Phase 3`로 복원했다.
- 근거: `README.md`, `problem/README.md`, `docs/README.md`, `spring/Makefile`, `EventMessagingService.java`, `OutboxEventEntity.java`, `V2__outbox_events.sql`, `EventMessagingApiTest.java`, `spring/build/test-results/test/*.xml`, `../../docs/verification-report.md`
- 작업 환경 전제: macOS + VSCode 통합 터미널 기준.

## Phase 1

- 당시 목표: 이벤트 랩의 baseline을 broker 연동이 아니라 outbox lifecycle로 자른다.
- 변경 단위: `README.md`, `problem/README.md`, `EventMessagingApiTest.java`
- 처음 가설: Kafka나 Redpanda가 바로 등장해야 이벤트 랩이 된다고 생각했다.
- 실제 조치: order event 생성, publish, outbox list 조회를 한 테스트 흐름으로 고정했다.
- CLI:

```bash
cd spring
make test
```

- 검증 신호: `EventMessagingApiTest` 1개 테스트 통과, `HealthApiTest` 2개 테스트 통과
- 핵심 코드 앵커: `EventMessagingApiTest.outboxEventLifecycleWorks()`
- 새로 배운 것: 이벤트 아키텍처의 첫 기준은 broker client가 아니라 outbox 상태 전이다.
- 다음: `PENDING -> PUBLISHED` 전이를 schema와 서비스 코드에 연결한다.

## Phase 2

- 당시 목표: 이벤트 생성과 publish를 서로 다른 단계로 남긴다.
- 변경 단위: `V2__outbox_events.sql`, `OutboxEventEntity.java`, `EventMessagingService.java`
- 처음 가설: 이벤트를 만들면서 바로 publish 처리해도 학습 목적에는 충분할 수 있다고 봤다.
- 실제 조치: `emitOrderPlaced()`는 `PENDING` row만 만들고, `publishPending()`이 `PUBLISHED`로 전이하게 분리했다.
- CLI:

```bash
cd spring
make smoke
docker compose up --build
```

- 검증 신호: `LabInfoApiSmokeTest` 1개 테스트 통과, `2026-03-09` 검증 보고서 기준 lint/test/smoke/Compose health 통과
- 핵심 코드 앵커: `V2__outbox_events.sql`, `OutboxEventEntity.markPublished()`, `EventMessagingService.publishPending()`
- 새로 배운 것: outbox의 핵심은 메시지 전송이 아니라 아직 보내지 않은 사실을 DB에 남기는 단계 분리다.
- 다음: worker와 runtime guarantee를 아직 하지 않았다는 점을 docs에 고정한다.

## Phase 3

- 당시 목표: outbox baseline이 증명한 범위와 아직 미완인 worker/runtime 영역을 닫는다.
- 변경 단위: `docs/README.md`, `spring/README.md`, `TEST-com.webpong.study2.app.EventMessagingApiTest.xml`
- 처음 가설: outbox row와 publish 상태 전이만 있으면 나머지도 자연스럽게 읽힐 줄 알았다.
- 실제 조치: long-running worker, real consumer contract, DLQ/retry 심화가 아직 문서 단계라는 점을 남겼다.
- CLI:

```bash
cd spring
make lint
make test
make smoke
```

- 검증 신호: `2026-03-13` 기준 4개 suite, 총 5개 테스트, 실패 0
- 핵심 코드 앵커: `docs/README.md`의 의도적 단순화, `verification-report.md`
- 새로 배운 것: 이벤트 랩은 범위를 작게 잘라야 outbox 경계가 더 선명해진다.
- 다음: cache, idempotency, concurrency는 `F-cache-concurrency-lab`에서 묶어 본다.
