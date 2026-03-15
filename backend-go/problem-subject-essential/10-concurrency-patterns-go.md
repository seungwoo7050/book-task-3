# 10-concurrency-patterns-go 문제지

## 왜 중요한가

Go의 핵심 동시성 패턴인 worker pool과 pipeline을 구현하고 goroutine lifecycle을 안전하게 관리한다.

## 목표

시작 위치의 구현을 완성해 worker pool이 job 제출, 결과 수집, graceful shutdown을 지원한다, pipeline이 Generator -> Filter -> Sink 3단계로 동작한다, 모든 단계가 context cancellation을 존중한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/01-backend-core/10-concurrency-patterns/problem/code/pipeline.go`
- `../study/01-backend-core/10-concurrency-patterns/problem/code/workerpool.go`
- `../study/01-backend-core/10-concurrency-patterns/solution/go/cmd/pipeline/main.go`
- `../study/01-backend-core/10-concurrency-patterns/solution/go/cmd/workerpool/main.go`
- `../study/01-backend-core/10-concurrency-patterns/solution/go/pipeline/pipeline.go`
- `../study/01-backend-core/10-concurrency-patterns/solution/go/workerpool/pool.go`
- `../study/01-backend-core/10-concurrency-patterns/solution/go/pipeline/pipeline_test.go`
- `../study/01-backend-core/10-concurrency-patterns/solution/go/workerpool/pool_test.go`

## starter code / 입력 계약

- ../study/01-backend-core/10-concurrency-patterns/problem/code/pipeline.go에서 starter 코드와 입력 경계를 잡는다.
- ../study/01-backend-core/10-concurrency-patterns/problem/code/workerpool.go에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- worker pool이 job 제출, 결과 수집, graceful shutdown을 지원한다.
- pipeline이 Generator -> Filter -> Sink 3단계로 동작한다.
- 모든 단계가 context cancellation을 존중한다.
- goroutine leak 없이 종료된다.
- benchmark로 throughput을 확인한다.

## 제외 범위

- distributed queue
- production backpressure policy
- `../study/01-backend-core/10-concurrency-patterns/problem/code/pipeline.go` starter skeleton을 정답 구현으로 착각하지 않는다.

## 성공 체크리스트

- `../study/01-backend-core/10-concurrency-patterns/problem/code/pipeline.go`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `main`와 `Generate`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestGenerateBasic`와 `TestGenerateContextCancel`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `make -C /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/10-concurrency-patterns/problem test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/10-concurrency-patterns/problem test
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`10-concurrency-patterns-go_answer.md`](10-concurrency-patterns-go_answer.md)에서 확인한다.
