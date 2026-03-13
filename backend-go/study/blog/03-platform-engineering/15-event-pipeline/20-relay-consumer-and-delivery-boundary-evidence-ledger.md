# 15 Event Pipeline Evidence Ledger

## 20 relay-consumer-and-delivery-boundary

- 시간 표지: 5단계: Relay 구현 -> 6단계: Consumer 구현 -> 7단계: CLI 진입점 -> 8단계: Kafka 토픽 생성
- 당시 목표: aggregate_id를 기준으로 ordering을 맞추고, consumer는 processed event tracking으로 중복 처리를 막는다.
- 변경 단위: `relay/main.go`, `consumer/main.go`
- 처음 가설: consumer idempotency를 별도 책임으로 두어 relay와 downstream 처리의 경계를 선명하게 했다.
- 실제 조치: `Relay.Run(ctx)` — ticker 루프, 폴링 → Kafka 발행 → MarkPublished. 설정: `PollInterval` (기본 1초), `BatchSize` (기본 100). Key = AggregateID, Headers = event_type + event_id + aggregate_type. 2단계 멱등성: 인메모리 map → DB processed_events. `FetchMessage` + `CommitMessages` 수동 커밋. Handler 실패 시 오프셋 미커밋 → 자동 재전달. 각각 독립 프로세스로 실행 가능. 파티션 3개: Consumer Group 내 최대 3개 Consumer 병렬 처리.

CLI:

```bash
go test ./relay/ -v

go test ./consumer/ -v
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/relay/relay.go`
- 새로 배운 것: relay는 outbox row를 브로커로 밀어내는 별도 프로세스다.
- 다음: 다음 글에서는 `30-repro-and-e2e-proof.md`에서 이어지는 경계를 다룬다.
