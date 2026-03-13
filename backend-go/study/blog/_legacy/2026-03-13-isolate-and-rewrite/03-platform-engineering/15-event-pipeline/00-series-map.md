# 15 Event Pipeline 시리즈 맵

이 시리즈는 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다.

## 이번 재작성 범위

- 문제 계약: [`README.md`](../../../03-platform-engineering/15-event-pipeline/README.md), [`problem/README.md`](../../../03-platform-engineering/15-event-pipeline/problem/README.md)
- 구현 표면:
- `solution/go/outbox/repository.go`
- `solution/go/relay/relay.go`
- `solution/go/e2e/pipeline_flow_test.go`
- 검증 표면: `cd solution/go && go test -v ./outbox ./relay ./consumer`, `cd solution/go && go test -run TestConsumerIdempotency -v ./consumer`
- 개념 축: outbox pattern은 DB 변경과 이벤트 기록을 한 트랜잭션 안에 묶는다., relay는 outbox row를 브로커로 밀어내는 별도 프로세스다., consumer는 at-least-once 환경을 가정하고 중복 처리를 견뎌야 한다.

## 챕터 구성

1. [`01-evidence-ledger.md`](01-evidence-ledger.md)
   실제 코드, 테스트, CLI, git history에서 복원한 chronology ledger
2. [`_structure-outline.md`](_structure-outline.md)
   최종 blog를 어떤 순서와 코드 앵커로 전개할지 먼저 고정한 구조 설계
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md)
   구현 순서, 판단 전환점, 검증 신호를 한 편으로 다시 쓴 최종 blog

## 이번에 따라간 질문

outbox, relay, consumer를 나눠 DB write와 Kafka publish를 느슨하게 연결한다.
