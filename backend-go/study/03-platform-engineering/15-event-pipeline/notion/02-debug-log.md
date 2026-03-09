# 디버그 기록 — 분산 이벤트 파이프라인의 함정들

## Relay와 MarkPublished 사이의 실패 창

Kafka에 이벤트를 성공적으로 발행했지만 `MarkPublished`가 실패하면? 다음 폴링에서 같은 이벤트를 다시 발행한다. 이것이 at-least-once의 본질이다.

이 "중복 발행"은 의도된 것이다. 완벽히 한 번만 발행하려면(exactly-once), Kafka 트랜잭션과 DB 트랜잭션을 연결해야 하는데, 두 시스템이 분리돼 있으므로 2PC(Two-Phase Commit) 같은 무거운 프로토콜이 필요하다. Outbox 패턴은 이 복잡도를 Consumer의 멱등성에 위임한다.

## Consumer 재시작 시 인메모리 캐시 유실

Consumer가 재시작되면 `map[string]struct{}` 캐시가 비어진다. 하지만 `processed_events` 테이블에 기록이 남아있으므로, `isPersisted` 체크에서 중복을 잡아낸다. 캐시는 성능 최적화일 뿐, 정확성은 DB가 보장한다.

## Kafka Message Key와 파티셔닝

`AggregateID`를 message key로 사용하는 이유: Kafka는 같은 key를 가진 메시지를 같은 파티션에 배치한다. 같은 파티션 내에서는 메시지 순서가 보장된다. 즉, 한 플레이어의 이벤트는 항상 순서대로 처리된다.

만약 key를 설정하지 않으면 라운드로빈으로 파티션이 선택되어, 한 플레이어의 구매 이벤트가 뒤바뀌어 처리될 수 있다.

## FetchMessage vs ReadMessage

`kafka.Reader`에는 두 가지 읽기 방식이 있다:

- `ReadMessage`: 메시지를 읽고 자동으로 오프셋 커밋. 처리 실패 시 이미 커밋된 메시지는 재전달되지 않음 → 메시지 유실 가능.
- `FetchMessage` + `CommitMessages`: 수동 커밋. 처리 성공 후 명시적으로 커밋 → at-least-once 보장.

이 프로젝트에서는 `FetchMessage`를 사용.

## Redpanda vs Apache Kafka

Docker Compose에서 `redpandadata/redpanda:v24.3.5`를 사용했다. Kafka 호환이지만:
- JVM 불필요 → 메모리 절약 (`--memory=512M`)
- `--mode=dev-container`로 단일 노드 빠른 설정
- `rpk` CLI로 클러스터 관리

`segmentio/kafka-go` 라이브러리는 Kafka 프로토콜을 구현하므로 Redpanda에서도 그대로 동작.

## Partial Index의 효과

```sql
CREATE INDEX idx_outbox_unpublished ON outbox (created_at) WHERE published_at IS NULL;
```

발행된 이벤트는 인덱스에 포함되지 않으므로, outbox에 쌓인 이벤트가 많아도 미발행 이벤트 조회 속도에 영향이 없다. 일반 인덱스였다면 발행 완료된 이벤트도 인덱스에 포함되어 불필요한 I/O 발생.

## 에러 시 배치 중단

Relay에서 하나의 이벤트 발행이 실패하면 나머지 배치도 중단한다. 순서 보장을 위한 결정이다. 실패한 이벤트를 건너뛰고 다음 이벤트를 발행하면, 같은 aggregate의 이벤트 순서가 깨질 수 있다.
