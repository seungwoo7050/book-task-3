# notion/ — CockroachDB 트랜잭션

이 디렉토리는 프로젝트 14 (CockroachDB Transactions)의 학습 과정을 블로그형 에세이로 기록합니다.

## 파일 목록

| 파일 | 내용 |
|------|------|
| [00-problem-framing.md](./00-problem-framing.md) | 왜 CockroachDB 트랜잭션을 직접 다뤄야 하는가 |
| [01-approach-log.md](./01-approach-log.md) | 계층 분리와 구현 과정 |
| [02-debug-log.md](./02-debug-log.md) | SQLSTATE 40001, 동시성, 멱등성에서 만난 문제들 |
| [03-retrospective.md](./03-retrospective.md) | 분산 데이터베이스 트랜잭션을 직접 다뤄보며 |
| [04-knowledge-index.md](./04-knowledge-index.md) | 다룬 개념 정리 |
| [05-development-timeline.md](./05-development-timeline.md) | CLI 명령어와 인프라 구성 타임라인 |

## 연관 프로젝트

- [08-sql-store-api](../../01-backend-core/08-sql-store-api/) — 단일 DB 트랜잭션과 낙관적 잠금의 첫 번째 경험
- [05-http-rest-basics](../../01-backend-core/05-http-rest-basics/) — 멱등성 키 개념 첫 등장
