# 14-cockroach-tx-go 문제지

## 왜 중요한가

게임 플랫폼 구매 흐름에서 optimistic locking, idempotency key, CockroachDB transaction retry를 구현한다.

## 목표

시작 위치의 구현을 완성해 players, inventory, idempotency_keys, audit_log 중심 스키마를 구성한다, 잔액 차감이 optimistic locking으로 동작한다, idempotency key가 이전 응답을 재사용한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/03-platform-engineering/14-cockroach-tx/solution/go/cmd/server/main.go`
- `../study/03-platform-engineering/14-cockroach-tx/solution/go/handler/purchase.go`
- `../study/03-platform-engineering/14-cockroach-tx/solution/go/repository/audit.go`
- `../study/03-platform-engineering/14-cockroach-tx/solution/go/repository/idempotency.go`
- `../study/03-platform-engineering/14-cockroach-tx/solution/go/e2e/purchase_flow_test.go`
- `../study/03-platform-engineering/14-cockroach-tx/solution/go/service/purchase_test.go`
- `../study/03-platform-engineering/14-cockroach-tx/solution/go/docker-compose.yml`
- `../study/03-platform-engineering/14-cockroach-tx/problem/Makefile`

## starter code / 입력 계약

- `../study/03-platform-engineering/14-cockroach-tx/solution/go/cmd/server/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- players, inventory, idempotency_keys, audit_log 중심 스키마를 구성한다.
- 잔액 차감이 optimistic locking으로 동작한다.
- idempotency key가 이전 응답을 재사용한다.
- SQLSTATE 40001 재시도 helper를 제공한다.
- POST /api/purchase API로 흐름을 노출한다.

## 제외 범위

- 복잡한 인증/인가
- 분산 트레이싱
- `../study/03-platform-engineering/14-cockroach-tx/solution/go/docker-compose.yml` fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `ServeHTTP`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestPurchaseFlowReplayAndPersistence`와 `TestHealthz`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/03-platform-engineering/14-cockroach-tx/solution/go/docker-compose.yml` fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/14-cockroach-tx/problem test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/14-cockroach-tx/problem test
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/14-cockroach-tx/solution/go test
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`14-cockroach-tx-go_answer.md`](14-cockroach-tx-go_answer.md)에서 확인한다.
