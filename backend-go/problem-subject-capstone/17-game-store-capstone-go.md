# 17-game-store-capstone-go 문제지

## 왜 중요한가

게임 상점 구매 흐름에서 트랜잭션, 멱등성, outbox, 운영 기본 요소를 통합한 단일 백엔드를 만든다.

## 목표

시작 위치의 구현을 완성해 GET /v1/healthcheck, POST /v1/purchases, 구매 조회, 인벤토리 조회 API를 제공한다, Idempotency-Key 기반 중복 요청 안전 처리와 낙관적 잠금을 구현한다, purchase 성공 시 outbox row를 기록하고 relay가 발행을 이어받는다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/04-capstone/17-game-store-capstone/solution/go/cmd/api/main.go`
- `../study/04-capstone/17-game-store-capstone/solution/go/internal/config/config.go`
- `../study/04-capstone/17-game-store-capstone/solution/go/internal/domain/types.go`
- `../study/04-capstone/17-game-store-capstone/solution/go/internal/httpapi/handler.go`
- `../study/04-capstone/17-game-store-capstone/solution/go/internal/relay/relay_test.go`
- `../study/04-capstone/17-game-store-capstone/solution/go/internal/service/purchase_service_test.go`
- `../study/04-capstone/17-game-store-capstone/solution/go/docker-compose.yml`
- `../study/04-capstone/17-game-store-capstone/solution/go/scripts/repro.sh`

## starter code / 입력 계약

- `../study/04-capstone/17-game-store-capstone/solution/go/cmd/api/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- GET /v1/healthcheck, POST /v1/purchases, 구매 조회, 인벤토리 조회 API를 제공한다.
- Idempotency-Key 기반 중복 요청 안전 처리와 낙관적 잠금을 구현한다.
- purchase 성공 시 outbox row를 기록하고 relay가 발행을 이어받는다.
- 구조화 로그, rate limiting, graceful shutdown을 포함한다.
- README 기준으로 build/test/repro가 가능해야 한다.

## 제외 범위

- 마이크로서비스 분리
- 복잡한 외부 인증
- `../study/04-capstone/17-game-store-capstone/solution/go/docker-compose.yml` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `Load`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `ListUnpublishedOutbox`와 `MarkOutboxPublished`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/04-capstone/17-game-store-capstone/solution/go/docker-compose.yml` 등 fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/backend-go/study/04-capstone/17-game-store-capstone/solution/go test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/backend-go/study/04-capstone/17-game-store-capstone/solution/go test
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`17-game-store-capstone-go_answer.md`](17-game-store-capstone-go_answer.md)에서 확인한다.
