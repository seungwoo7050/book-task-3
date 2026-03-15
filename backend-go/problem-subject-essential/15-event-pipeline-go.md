# 15-event-pipeline-go 문제지

## 왜 중요한가

구매 이벤트를 DB transaction과 Kafka publish 사이에서 정합성을 잃지 않도록 outbox pattern으로 구현한다.

## 목표

시작 위치의 구현을 완성해 purchase transaction 안에서 outbox row를 함께 기록한다, relay가 미발행 이벤트를 읽어 Kafka topic으로 전달한다, aggregate_id 기준 ordering을 유지한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/03-platform-engineering/15-event-pipeline/solution/go/cmd/consumer/main.go`
- `../study/03-platform-engineering/15-event-pipeline/solution/go/cmd/relay/main.go`
- `../study/03-platform-engineering/15-event-pipeline/solution/go/consumer/consumer.go`
- `../study/03-platform-engineering/15-event-pipeline/solution/go/outbox/model.go`
- `../study/03-platform-engineering/15-event-pipeline/solution/go/consumer/consumer_test.go`
- `../study/03-platform-engineering/15-event-pipeline/solution/go/e2e/pipeline_flow_test.go`
- `../study/03-platform-engineering/15-event-pipeline/solution/go/docker-compose.yml`
- `../study/03-platform-engineering/15-event-pipeline/problem/Makefile`

## starter code / 입력 계약

- `../study/03-platform-engineering/15-event-pipeline/solution/go/cmd/consumer/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- purchase transaction 안에서 outbox row를 함께 기록한다.
- relay가 미발행 이벤트를 읽어 Kafka topic으로 전달한다.
- aggregate_id 기준 ordering을 유지한다.
- consumer가 idempotent하게 이벤트를 처리한다.
- HTTP purchase -> relay -> consumer 흐름이 연결된다.

## 제외 범위

- 복잡한 orchestration
- 대규모 production Kafka tuning
- `../study/03-platform-engineering/15-event-pipeline/solution/go/docker-compose.yml` fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `New`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestGetHeader`와 `TestConsumerIdempotency`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/03-platform-engineering/15-event-pipeline/solution/go/docker-compose.yml` fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/15-event-pipeline/problem test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/15-event-pipeline/problem test
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/15-event-pipeline/solution/go test
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`15-event-pipeline-go_answer.md`](15-event-pipeline-go_answer.md)에서 확인한다.
