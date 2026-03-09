# 지식 인덱스 — 이벤트 파이프라인에서 다룬 개념들

## Transactional Outbox Pattern

DB 쓰기와 이벤트 발행의 일관성을 보장하는 패턴. 비즈니스 로직과 같은 트랜잭션에서 outbox 테이블에 이벤트를 INSERT. 별도 프로세스(Relay)가 outbox를 폴링하여 메시지 브로커에 발행. DB 트랜잭션이 원자성을 보장하므로 이벤트 유실이 없다.

## At-Least-Once Delivery

메시지가 최소 한 번은 전달되지만, 중복 전달될 수 있는 의미론. Outbox Relay가 발행 후 MarkPublished 실패 시 재발행. Consumer는 멱등 처리로 중복을 흡수해야 한다.

## Idempotent Consumer (멱등 컨슈머)

같은 메시지를 여러 번 받아도 결과가 한 번 처리한 것과 같은 Consumer. 이 프로젝트에서는 2단계: 인메모리 캐시 (`map[string]struct{}`) + DB 테이블 (`processed_events`). `INSERT ON CONFLICT DO NOTHING`으로 영속적 중복 방지.

## Kafka Message Key

Kafka 메시지의 키. 같은 키를 가진 메시지는 같은 파티션에 배치되어 순서가 보장된다. `AggregateID`를 키로 사용해 같은 엔티티의 이벤트가 순서대로 처리되도록 함.

## Consumer Group

Kafka에서 여러 Consumer가 토픽의 파티션을 분담하는 메커니즘. `kafka.ReaderConfig`의 `GroupID`로 설정. 파티션 수만큼 Consumer를 병렬 실행 가능.

## FetchMessage + CommitMessages

`kafka.Reader`의 수동 커밋 패턴. `FetchMessage`로 메시지를 가져오고, 처리 성공 후 `CommitMessages`로 오프셋을 명시적으로 커밋. `ReadMessage`(자동 커밋)와 다르게 처리 실패 시 메시지가 재전달된다.

## Partial Index

조건을 만족하는 행만 포함하는 인덱스. `WHERE published_at IS NULL`로 미발행 이벤트만 인덱싱. 인덱스 크기가 작고 조회 성능이 높다. PostgreSQL, CockroachDB 지원.

## segmentio/kafka-go

Go용 순수 Go 구현 Kafka 클라이언트. `kafka.Writer`(프로듀서)와 `kafka.Reader`(컨슈머). librdkafka(C 라이브러리)에 의존하지 않아 빌드가 간단. CGO 불요.

## Redpanda

Apache Kafka 호환 스트리밍 플랫폼. C++로 작성되어 JVM 불필요. Docker에서 `--mode=dev-container`로 빠른 단일 노드 설정. `rpk` CLI로 토픽 관리. Kafka 프로토콜을 그대로 구현하므로 기존 Kafka 클라이언트가 호환.

## Kafka Headers

Kafka 메시지에 키-값 메타데이터를 첨부하는 기능. `event_type`, `event_id`, `aggregate_type`을 헤더에 담아 Consumer가 페이로드를 파싱하기 전에 라우팅을 결정할 수 있다.

## Cleanup / Purge

Outbox, processed_events 등 운영 테이블의 크기를 관리하는 패턴. `DELETE WHERE published_at IS NOT NULL AND published_at < now() - interval`. CockroachDB에서는 대량 DELETE가 분산 트랜잭션으로 실행되므로 배치 삭제가 효율적.
