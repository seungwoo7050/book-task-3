# 10-concurrency-patterns-go 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 worker pool이 job 제출, 결과 수집, graceful shutdown을 지원한다, pipeline이 Generator -> Filter -> Sink 3단계로 동작한다, 모든 단계가 context cancellation을 존중한다를 한 흐름으로 설명하고 검증한다. 핵심은 `main`와 `Generate`, `Filter` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- worker pool이 job 제출, 결과 수집, graceful shutdown을 지원한다.
- pipeline이 Generator -> Filter -> Sink 3단계로 동작한다.
- 모든 단계가 context cancellation을 존중한다.
- 첫 진입점은 `../study/01-backend-core/10-concurrency-patterns/solution/go/cmd/pipeline/main.go`이고, 여기서 `main`와 `Generate` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/01-backend-core/10-concurrency-patterns/solution/go/cmd/pipeline/main.go`: `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/01-backend-core/10-concurrency-patterns/solution/go/cmd/workerpool/main.go`: `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/01-backend-core/10-concurrency-patterns/solution/go/pipeline/pipeline.go`: `Generate`, `Filter`, `Sink`, `FanOut`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/01-backend-core/10-concurrency-patterns/solution/go/workerpool/pool.go`: `NewPool`, `worker`, `Submit`, `Results`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/01-backend-core/10-concurrency-patterns/problem/code/pipeline.go`: `Generate`, `Filter`, `Sink`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/01-backend-core/10-concurrency-patterns/problem/code/workerpool.go`: `NewPool`, `Submit`, `Results`, `Stop`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/01-backend-core/10-concurrency-patterns/solution/go/pipeline/pipeline_test.go`: `TestGenerateBasic`, `TestGenerateContextCancel`, `TestFilterEvenNumbers`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/01-backend-core/10-concurrency-patterns/solution/go/workerpool/pool_test.go`: `TestPoolBasic`, `TestPoolErrorPropagation`, `TestPoolContextCancellation`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../study/01-backend-core/10-concurrency-patterns/problem/code/pipeline.go`와 `../study/01-backend-core/10-concurrency-patterns/solution/go/cmd/pipeline/main.go`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `TestGenerateBasic` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make -C /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/10-concurrency-patterns/problem test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/10-concurrency-patterns/problem test
```

- `../study/01-backend-core/10-concurrency-patterns/problem/code/pipeline.go` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `TestGenerateBasic`와 `TestGenerateContextCancel`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/10-concurrency-patterns/problem test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/01-backend-core/10-concurrency-patterns/solution/go/cmd/pipeline/main.go`
- `../study/01-backend-core/10-concurrency-patterns/solution/go/cmd/workerpool/main.go`
- `../study/01-backend-core/10-concurrency-patterns/solution/go/pipeline/pipeline.go`
- `../study/01-backend-core/10-concurrency-patterns/solution/go/workerpool/pool.go`
- `../study/01-backend-core/10-concurrency-patterns/problem/code/pipeline.go`
- `../study/01-backend-core/10-concurrency-patterns/problem/code/workerpool.go`
- `../study/01-backend-core/10-concurrency-patterns/solution/go/pipeline/pipeline_test.go`
- `../study/01-backend-core/10-concurrency-patterns/solution/go/workerpool/pool_test.go`
- `../study/01-backend-core/10-concurrency-patterns/problem/Makefile`
- `../study/01-backend-core/10-concurrency-patterns/solution/go/go.mod`
