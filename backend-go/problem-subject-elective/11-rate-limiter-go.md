# 11-rate-limiter-go 문제지

## 왜 중요한가

Token Bucket rate limiter를 구현하고 per-client HTTP middleware로 통합한다.

## 목표

시작 위치의 구현을 완성해 Token Bucket이 refill rate와 burst를 지원한다, Allow()가 thread-safe하게 동작한다, per-client limiter가 IP 기준으로 분리된다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/01-backend-core/11-rate-limiter/solution/go/limiter.go`
- `../study/01-backend-core/11-rate-limiter/solution/go/middleware.go`
- `../study/01-backend-core/11-rate-limiter/solution/go/limiter_test.go`
- `../study/01-backend-core/11-rate-limiter/solution/go/middleware_test.go`
- `../study/01-backend-core/11-rate-limiter/problem/Makefile`
- `../study/01-backend-core/11-rate-limiter/solution/go/go.mod`

## starter code / 입력 계약

- `../study/01-backend-core/11-rate-limiter/solution/go/limiter.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- Token Bucket이 refill rate와 burst를 지원한다.
- Allow()가 thread-safe하게 동작한다.
- per-client limiter가 IP 기준으로 분리된다.
- stale entry cleanup goroutine이 context cancellation을 존중한다.
- 초과 요청에 429와 Retry-After를 반환한다.

## 제외 범위

- shared distributed limiter
- global quota coordination
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `NewLimiter`와 `Allow`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestLimiterBasic`와 `TestLimiterRefill`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `make -C /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/11-rate-limiter/problem test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/11-rate-limiter/problem test
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`11-rate-limiter-go_answer.md`](11-rate-limiter-go_answer.md)에서 확인한다.
