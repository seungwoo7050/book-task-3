# 15 Event Pipeline Structure

## 이 글이 답할 질문

- aggregate_id를 기준으로 ordering을 맞추고, consumer는 processed event tracking으로 중복 처리를 막는다.
- consumer idempotency를 별도 책임으로 두어 relay와 downstream 처리의 경계를 선명하게 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `03-platform-engineering/15-event-pipeline` 안에서 `20-relay-consumer-and-delivery-boundary.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 5단계: Relay 구현 -> 6단계: Consumer 구현 -> 7단계: CLI 진입점 -> 8단계: Kafka 토픽 생성
- 세션 본문: `relay/main.go, consumer/main.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/relay/relay.go`
- 코드 앵커 2: `solution/go/consumer/consumer.go`
- 코드 설명 초점: 이 블록은 동기 write path와 비동기 side effect를 분리하는 설계의 핵심 증거다. "나중에 처리한다"가 아니라 "어떻게 안전하게 넘긴다"를 설명하게 해 준다.
- 개념 설명: relay는 outbox row를 브로커로 밀어내는 별도 프로세스다.
- 마지막 단락: 다음 글에서는 `30-repro-and-e2e-proof.md`에서 이어지는 경계를 다룬다.
