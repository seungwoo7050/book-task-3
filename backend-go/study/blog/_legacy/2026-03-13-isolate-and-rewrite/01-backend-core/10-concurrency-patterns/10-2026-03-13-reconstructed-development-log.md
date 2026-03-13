# 10 Concurrency Patterns 재구성 개발 로그

10 Concurrency Patterns는 worker pool과 pipeline을 통해 goroutine lifecycle, channel, cancellation을 직접 다루는 본선 과제다.

이 글은 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 쓴 버전이다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다. 세밀한 shell history가 남아 있지 않아 시간 표지는 `Phase 1/2/3`처럼 재구성했고, 근거는 README, 살아 있는 소스코드, docs, 테스트, 현재 CLI 재실행 결과만 사용했다.

## 구현 순서 요약

- Phase 1: Pool과 worker goroutine으로 bounded concurrency를 먼저 고정한다 - `solution/go/workerpool/pool.go`의 `NewPool`
- Phase 2: Generate, Filter, FanOut으로 channel pipeline을 조립한다 - `solution/go/pipeline/pipeline.go`의 `FanOut`
- Phase 3: demo CLI와 benchmark로 concurrency 패턴 차이를 닫는다 - `solution/go/workerpool/pool_test.go`의 `TestPoolNoGoroutineLeaks`

## Phase 1. Pool과 worker goroutine으로 bounded concurrency를 먼저 고정한다

- 당시 목표: Pool과 worker goroutine으로 bounded concurrency를 먼저 고정한다
- 변경 단위: `solution/go/workerpool/pool.go`의 `NewPool`
- 처음 가설: `NewPool`처럼 worker lifecycle을 먼저 고정해야 goroutine 누수 여부를 나중에 설명할 수 있다고 봤다.
- 실제 진행: `solution/go/workerpool/pool.go`의 `NewPool`로 worker lifecycle과 cancellation path를 먼저 닫았다.
- CLI: `make -C problem run-workerpool`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `Running worker pool example...`였다.

핵심 코드:

```go
func NewPool(ctx context.Context, workers int, handler func(Job) Result) *Pool {
	ctx, cancel := context.WithCancel(ctx)

	p := &Pool{
		ctx:     ctx,
		cancel:  cancel,
		jobs:    make(chan Job, workers*2), // buffered to reduce blocking
		results: make(chan Result, workers*2),
		handler: handler,
```

왜 이 코드가 중요했는가: `NewPool`는 `solution/go/workerpool/pool.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

- 새로 배운 것: worker pool은 제한된 수의 goroutine으로 작업을 소비하는 패턴이다.
- 다음: Generate, Filter, FanOut으로 channel pipeline을 조립한다
## Phase 2. Generate, Filter, FanOut으로 channel pipeline을 조립한다

- 당시 목표: Generate, Filter, FanOut으로 channel pipeline을 조립한다
- 변경 단위: `solution/go/pipeline/pipeline.go`의 `FanOut`
- 처음 가설: `FanOut`를 통해 channel 흐름을 분리하면 backpressure와 cancellation을 코드 수준에서 읽기 쉬워진다고 판단했다.
- 실제 진행: `solution/go/pipeline/pipeline.go`의 `FanOut`를 통해 channel fan-out, filter, sink 흐름을 조립했다.
- CLI: `make -C problem run-pipeline`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `Running pipeline example...`였다.

핵심 코드:

```go
// FanOut은 입력 작업을 n개의 worker goroutine으로 분산 처리하고 결과를 하나로 모은다.
func FanOut(ctx context.Context, in <-chan int, n int, worker func(int) int) <-chan int {
	out := make(chan int)
	done := make(chan struct{})

	for i := 0; i < n; i++ {
		go func() {
			defer func() { done <- struct{}{} }()
			for val := range in {
				select {
```

왜 이 코드가 중요했는가: `FanOut`는 `solution/go/pipeline/pipeline.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

- 새로 배운 것: pipeline은 읽기 쉽지만 stage가 많아질수록 디버깅이 어려워질 수 있다.
- 다음: demo CLI와 benchmark로 concurrency 패턴 차이를 닫는다
## Phase 3. demo CLI와 benchmark로 concurrency 패턴 차이를 닫는다

- 당시 목표: demo CLI와 benchmark로 concurrency 패턴 차이를 닫는다
- 변경 단위: `solution/go/workerpool/pool_test.go`의 `TestPoolNoGoroutineLeaks`
- 처음 가설: demo와 테스트가 같이 있어야 concurrency 패턴 차이가 수치와 출력 둘 다에서 보인다고 봤다.
- 실제 진행: `solution/go/workerpool/pool_test.go`의 `TestPoolNoGoroutineLeaks`와 CLI demo를 함께 두어 leak 여부와 처리량 차이를 눈으로 확인하게 만들었다.
- CLI: `make -C problem test`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `Running tests...`였다.

핵심 코드:

```go
func TestPoolNoGoroutineLeaks(t *testing.T) {
	handler := func(j Job) Result {
		return Result{JobID: j.ID, Value: j.Payload}
	}

	ctx := context.Background()
	pool := NewPool(ctx, 4, handler)

	for i := 0; i < 5; i++ {
```

왜 이 코드가 중요했는가: `TestPoolNoGoroutineLeaks`는 `solution/go/workerpool/pool_test.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

- 새로 배운 것: benchmark 숫자만 보고 실서비스 concurrency 정책으로 바로 옮기면 과적합될 수 있다.
- 다음: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## CLI 1. 현재 저장소에서 다시 돌린 검증

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/10-concurrency-patterns && make -C problem run-workerpool)
```

```text
Running worker pool example...
cd ../solution/go && go run ./cmd/workerpool
Job 1: result = 1
Job 2: result = 4
Job 3: result = 9
Job 4: result = 16
Job 7: result = 49
Job 6: result = 36
Job 5: result = 25
Job 8: result = 64
Job 10: result = 100
Job 9: result = 81
Job 12: result = 144
Job 11: result = 121
Job 16: result = 256
Job 14: result = 196
Job 13: result = 169
Job 15: result = 225
Job 18: result = 324
Job 20: result = 400
Job 17: result = 289
Job 19: result = 361
... (1 more lines)
```
## CLI 2. 현재 저장소에서 다시 돌린 검증

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/10-concurrency-patterns && make -C problem run-pipeline)
```

```text
Running pipeline example...
cd ../solution/go && go run ./cmd/pipeline
Primes from 1 to 50: [2 3 5 7 11 13 17 19 23 29 31 37 41 43 47]
Count: 15
```

## 이번 재작성에서 남은 것

- 이번 글을 지탱한 개념 축: worker pool은 제한된 수의 goroutine으로 작업을 소비하는 패턴이다., pipeline은 단계별 channel 연결로 데이터 흐름을 분리한다., `context.Context`는 중단 신호를 한 방향으로 전파하는 공통 장치다., goroutine을 시작했다면 종료 경로와 channel close 책임도 같이 설계해야 한다.
- 최신 검증 메모: 현재 저장소에서 다시 실행한 명령은 모두 exit 0으로 끝났다.
- 다음 질문: worker pool과 pipeline을 각각 분리해 context cancellation, backpressure, fan-out을 비교한다.
