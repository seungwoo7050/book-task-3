# 14 Cockroach TX — Repro And E2E Proof

`03-platform-engineering/14-cockroach-tx`는 idempotency key, optimistic locking, transaction retry를 CockroachDB 호환 흐름으로 묶어 정합성 기초를 다지는 과제다. 이 글에서는 10단계: E2E 테스트 -> 11단계: 빌드 및 검증 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 10단계: E2E 테스트
- 11단계: 빌드 및 검증

## Day 1
### Session 1

- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/e2e/purchase_flow_test.go`, `solution/go/Makefile`
- 처음 가설: HTTP handler, service, repo를 나눠 정합성 로직이 어디에 있어야 하는지 드러냈다.
- 실제 진행: `RUN_E2E=1` 환경변수로 게이트. CI에서는 DB가 있을 때만 실행.

CLI:

```bash
# CockroachDB 연동 통합 테스트
make e2e
# 내부: RUN_E2E=1 DATABASE_URL=... go test ./e2e -v -count=1

make build          # bin/server 바이너리 생성
make test           # 단위 테스트
make test-race      # -race 플래그
make smoke          # = make e2e
```

검증 신호:

- make smoke          # = make e2e
- 2026-03-08 기준 `make -C problem build`가 통과했다.
- 2026-03-08 기준 `make -C problem test`가 통과했다.
- 2026-03-08 기준 `cd solution/go && make repro`가 통과했다.

핵심 코드: `solution/go/e2e/purchase_flow_test.go`

```go
type purchaseResponse struct {
	Status     string `json:"status"`
	NewBalance int64  `json:"new_balance"`
	Item       string `json:"item"`
}

func TestPurchaseFlowReplayAndPersistence(t *testing.T) {
	requireRuntime(t)

	db := openDB(t)
	t.Cleanup(func() { _ = db.Close() })

	resetState(t, db)
	seedPlayer(t, db, 1_000)

	server := httptest.NewServer(&handler.PurchaseHandler{
		Service: service.NewPurchaseService(db),
	})
```

왜 이 코드가 중요했는가:

이 테스트나 재현 스크립트는 프로젝트의 공개 표면을 말이 아니라 입력과 결과로 고정한다. 최종 글에서 이 증거를 빼면 구현은 보여도 완료 기준은 흐려진다.

새로 배운 것:

- Cockroach류 분산 SQL은 serialization failure를 애플리케이션 레벨에서 재시도하게 요구할 수 있다.

보조 코드: `solution/go/Makefile`

```text
.PHONY: help up down logs wait-db migrate reset-schema build run test test-race e2e smoke repro

COMPOSE := docker compose -p cockroach-tx -f docker-compose.yml
DATABASE_URL ?= postgresql://root@localhost:26257/defaultdb?sslmode=disable
ADDR ?= :8080

help: ## Show available commands
	@grep -E '^[a-zA-Z0-9_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

up: ## Start CockroachDB
	$(COMPOSE) up -d db
	$(MAKE) wait-db

down: ## Stop containers
	$(COMPOSE) down -v

logs: ## Show CockroachDB logs
	$(COMPOSE) logs -f db
```

왜 이 코드도 같이 봐야 하는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

CLI:

```bash
cd 03-platform-engineering/14-cockroach-tx
make -C problem build
make -C problem test

cd 03-platform-engineering/14-cockroach-tx/solution/go
make repro
```

검증 신호:

- 2026-03-08 기준 `make -C problem build`가 통과했다.
- 2026-03-08 기준 `make -C problem test`가 통과했다.
- 2026-03-08 기준 `cd solution/go && make repro`가 통과했다.

다음:

- 선택 검증이나 운영 환경에서만 가능한 경계를 짧게 남긴다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/e2e/purchase_flow_test.go` 같은 결정적인 코드와 `cd 03-platform-engineering/14-cockroach-tx` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
