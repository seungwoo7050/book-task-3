# 17 Game Store Capstone — Repro And E2E Hardening

`04-capstone/17-game-store-capstone`는 거래 일관성, outbox, 운영 기본 요소를 하나의 게임 상점 API로 통합한 필수 capstone이다. 이 글에서는 12단계: E2E 테스트 -> 13단계: 전체 검증 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 12단계: E2E 테스트
- 13단계: 전체 검증

## Day 1
### Session 1

- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/e2e/purchase_flow_test.go`, `solution/go/Makefile`
- 처음 가설: OAuth나 마이크로서비스는 제외하고 거래 일관성과 재현성에 집중했다.
- 실제 진행: 

CLI:

```bash
make e2e
# 구매 → 조회 → 멱등성 → 인벤토리 확인

make build
make test
go test -race ./...
```

검증 신호:

- 2026-03-08 기준 `mkdir -p ./bin && go build -o ./bin/api ./cmd/api`가 통과했다.
- 2026-03-08 기준 `go test ./...`가 통과했다.
- 2026-03-08 기준 `make repro`가 통과했다.

핵심 코드: `solution/go/e2e/purchase_flow_test.go`

```go
type purchaseResponse struct {
	PurchaseID string    `json:"purchase_id"`
	PlayerID   string    `json:"player_id"`
	ItemID     string    `json:"item_id"`
	Price      int64     `json:"price"`
	NewBalance int64     `json:"new_balance"`
	Status     string    `json:"status"`
	CreatedAt  time.Time `json:"created_at"`
}

type errorResponse struct {
	Error string `json:"error"`
}

type inventoryEnvelope struct {
	PlayerID string                 `json:"player_id"`
	Items    []domain.InventoryItem `json:"items"`
}
```

왜 이 코드가 중요했는가:

이 테스트나 재현 스크립트는 프로젝트의 공개 표면을 말이 아니라 입력과 결과로 고정한다. 최종 글에서 이 증거를 빼면 구현은 보여도 완료 기준은 흐려진다.

새로 배운 것:

- e2e 테스트는 unit test가 놓치는 통합 문제를 빠르게 드러낸다.

보조 코드: `solution/go/Makefile`

```text
.PHONY: help up down logs wait-db migrate reset-schema run test test-race e2e repro

COMPOSE := docker compose -f docker-compose.yml
DATABASE_URL ?= postgresql://postgres:postgres@localhost:54329/game_store?sslmode=disable

help: ## Show available commands
	@grep -E '^[a-zA-Z0-9_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

up: ## Start PostgreSQL container
	$(COMPOSE) up -d db
	$(MAKE) wait-db

down: ## Stop containers
	$(COMPOSE) down

logs: ## Show DB container logs
	$(COMPOSE) logs -f db
```

왜 이 코드도 같이 봐야 하는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

CLI:

```bash
cd 04-capstone/17-game-store-capstone/go
mkdir -p ./bin
go build -o ./bin/api ./cmd/api
go test ./...
make repro
```

검증 신호:

- 2026-03-08 기준 `mkdir -p ./bin && go build -o ./bin/api ./cmd/api`가 통과했다.
- 2026-03-08 기준 `go test ./...`가 통과했다.
- 2026-03-08 기준 `make repro`가 통과했다.

다음:

- 선택 검증이나 운영 환경에서만 가능한 경계를 짧게 남긴다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/e2e/purchase_flow_test.go` 같은 결정적인 코드와 `cd 04-capstone/17-game-store-capstone/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
