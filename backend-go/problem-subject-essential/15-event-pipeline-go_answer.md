# 15-event-pipeline-go 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 purchase transaction 안에서 outbox row를 함께 기록한다, relay가 미발행 이벤트를 읽어 Kafka topic으로 전달한다, aggregate_id 기준 ordering을 유지한다를 한 흐름으로 설명하고 검증한다. 핵심은 `main`와 `New`, `Run` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- purchase transaction 안에서 outbox row를 함께 기록한다.
- relay가 미발행 이벤트를 읽어 Kafka topic으로 전달한다.
- aggregate_id 기준 ordering을 유지한다.
- 첫 진입점은 `../study/03-platform-engineering/15-event-pipeline/solution/go/cmd/consumer/main.go`이고, 여기서 `main`와 `New` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/03-platform-engineering/15-event-pipeline/solution/go/cmd/consumer/main.go`: `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/03-platform-engineering/15-event-pipeline/solution/go/cmd/relay/main.go`: `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/03-platform-engineering/15-event-pipeline/solution/go/consumer/consumer.go`: `New`, `Run`, `isProcessed`, `markProcessed`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/03-platform-engineering/15-event-pipeline/solution/go/outbox/model.go`: 핵심 구현을 담는 파일이다.
- `../study/03-platform-engineering/15-event-pipeline/solution/go/outbox/repository.go`: `NewRepository`, `InsertTx`, `GetUnpublished`, `MarkPublished`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/03-platform-engineering/15-event-pipeline/solution/go/consumer/consumer_test.go`: `TestGetHeader`, `TestConsumerIdempotency`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/03-platform-engineering/15-event-pipeline/solution/go/e2e/pipeline_flow_test.go`: `TestRelayPublishesAndConsumerDedupesAcrossRestart`, `requireRuntime`, `openDB`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/03-platform-engineering/15-event-pipeline/solution/go/outbox/repository_test.go`: `TestPurchasePayloadMarshal`, `TestEventModel`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../study/03-platform-engineering/15-event-pipeline/solution/go/cmd/consumer/main.go`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `TestGetHeader` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make -C /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/15-event-pipeline/problem test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/15-event-pipeline/problem test
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/15-event-pipeline/solution/go test
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `TestGetHeader`와 `TestConsumerIdempotency`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/15-event-pipeline/problem test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/03-platform-engineering/15-event-pipeline/solution/go/cmd/consumer/main.go`
- `../study/03-platform-engineering/15-event-pipeline/solution/go/cmd/relay/main.go`
- `../study/03-platform-engineering/15-event-pipeline/solution/go/consumer/consumer.go`
- `../study/03-platform-engineering/15-event-pipeline/solution/go/outbox/model.go`
- `../study/03-platform-engineering/15-event-pipeline/solution/go/outbox/repository.go`
- `../study/03-platform-engineering/15-event-pipeline/solution/go/consumer/consumer_test.go`
- `../study/03-platform-engineering/15-event-pipeline/solution/go/e2e/pipeline_flow_test.go`
- `../study/03-platform-engineering/15-event-pipeline/solution/go/outbox/repository_test.go`
- `../study/03-platform-engineering/15-event-pipeline/solution/go/docker-compose.yml`
- `../study/03-platform-engineering/15-event-pipeline/problem/Makefile`
