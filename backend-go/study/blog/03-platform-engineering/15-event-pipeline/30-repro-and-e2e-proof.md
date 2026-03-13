# 15 Event Pipeline — Repro And E2E Proof

`03-platform-engineering/15-event-pipeline`는 outbox pattern, relay, idempotent consumer를 통해 DB 정합성과 비동기 전달 경계를 함께 다루는 대표 과제다. 이 글에서는 9단계: E2E 테스트 -> 10단계: 빌드 및 검증 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 9단계: E2E 테스트
- 10단계: 빌드 및 검증

## Day 1
### Session 1

- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/e2e/pipeline_flow_test.go`, `solution/go/Makefile`
- 처음 가설: consumer idempotency를 별도 책임으로 두어 relay와 downstream 처리의 경계를 선명하게 했다.
- 실제 진행: 전체 흐름: 구매 → outbox INSERT → relay 발행 → consumer 처리

CLI:

```bash
make e2e
# RUN_E2E=1 DATABASE_URL=... KAFKA_BROKERS=... go test ./e2e -v -count=1

make build
make test
make test-race
make smoke
```

검증 신호:

- make smoke
- 2026-03-08 기준 `make -C problem build`가 통과했다.
- 2026-03-08 기준 `make -C problem test`가 통과했다.
- 2026-03-08 기준 `cd solution/go && make repro`가 통과했다.

핵심 코드: `solution/go/e2e/pipeline_flow_test.go`

```go
func TestRelayPublishesAndConsumerDedupesAcrossRestart(t *testing.T) {
	requireRuntime(t)

	db := openDB(t)
	t.Cleanup(func() { _ = db.Close() })
	resetState(t, db)

	broker := os.Getenv("KAFKA_BROKER")
	if broker == "" {
		broker = defaultKafkaBroker
	}
	topic := fmt.Sprintf("game.purchases.e2e.%d", time.Now().UnixNano())

	eventID := "22222222-2222-2222-2222-222222222222"
	aggregateID := "33333333-3333-3333-3333-333333333333"
	payload := outbox.PurchasePayload{
		PlayerID:   aggregateID,
		ItemName:   "sword_of_fire",
```

왜 이 코드가 중요했는가:

이 블록은 병렬성과 보호 정책을 아이디어가 아니라 코드 invariant로 바꾼다. goroutine, channel, token을 어떤 경계로 묶었는지가 여기서 드러난다.

새로 배운 것:

- consumer는 at-least-once 환경을 가정하고 중복 처리를 견뎌야 한다.

보조 코드: `solution/go/Makefile`

```text
.PHONY: help up down logs wait-db wait-kafka migrate reset-schema build run-relay run-consumer test test-race e2e smoke repro

COMPOSE := docker compose -p event-pipeline -f docker-compose.yml
DATABASE_URL ?= postgresql://root@localhost:26258/defaultdb?sslmode=disable
KAFKA_BROKER ?= localhost:9093
KAFKA_TOPIC ?= game.purchases

help: ## Show available commands
	@grep -E '^[a-zA-Z0-9_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

up: ## Start CockroachDB and Redpanda
	$(COMPOSE) up -d db kafka
	$(MAKE) wait-db
	$(MAKE) wait-kafka

down: ## Stop containers
	$(COMPOSE) down -v
```

왜 이 코드도 같이 봐야 하는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

CLI:

```bash
cd 03-platform-engineering/15-event-pipeline
make -C problem build
make -C problem test

cd 03-platform-engineering/15-event-pipeline/solution/go
make repro
```

검증 신호:

- 2026-03-08 기준 `make -C problem build`가 통과했다.
- 2026-03-08 기준 `make -C problem test`가 통과했다.
- 2026-03-08 기준 `cd solution/go && make repro`가 통과했다.

다음:

- 선택 검증이나 운영 환경에서만 가능한 경계를 짧게 남긴다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/e2e/pipeline_flow_test.go` 같은 결정적인 코드와 `cd 03-platform-engineering/15-event-pipeline` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
