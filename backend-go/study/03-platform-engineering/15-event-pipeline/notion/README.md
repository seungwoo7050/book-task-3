# notion/ — 이벤트 파이프라인

이 디렉토리는 프로젝트 15 (Event Pipeline)의 학습 과정을 블로그형 에세이로 기록합니다.

## 파일 목록

| 파일 | 내용 |
|------|------|
| [00-problem-framing.md](./00-problem-framing.md) | 왜 Outbox 패턴이 필요한가 |
| [01-approach-log.md](./01-approach-log.md) | Outbox Writer → Relay → Consumer 구현 과정 |
| [02-debug-log.md](./02-debug-log.md) | Kafka, CockroachDB, 중복처리에서 만난 문제들 |
| [03-retrospective.md](./03-retrospective.md) | at-least-once 의미론과 분산 시스템의 현실 |
| [04-knowledge-index.md](./04-knowledge-index.md) | 다룬 개념 정리 |
| [05-timeline.md](./05-timeline.md) | CLI 명령어와 인프라 구성 타임라인 |

## 연관 프로젝트

- [14-cockroach-tx](../14-cockroach-tx/) — CockroachDB 트랜잭션, 이 프로젝트의 DB 기반
- [13-distributed-log-core](../../02-distributed-systems/13-distributed-log-core/) — 커밋 로그의 내부 구조
- [10-concurrency-patterns](../../01-backend-core/10-concurrency-patterns/) — 고루틴/채널 패턴 (relay, consumer)
