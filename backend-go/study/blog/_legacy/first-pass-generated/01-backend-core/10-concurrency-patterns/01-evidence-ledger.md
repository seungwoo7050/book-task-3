# 10 Concurrency Patterns Evidence Ledger

이 문서는 기존 `blog/` 초안을 입력으로 읽지 않고, 살아 있는 근거만으로 chronology를 복원한 ledger다.

## 근거 묶음

- 프로젝트 요약: worker pool과 pipeline을 통해 goroutine lifecycle, channel, cancellation을 직접 다루는 본선 과제다.
- 구현 디렉터리: `solution/go`
- 주요 구현 파일: `solution/go/workerpool/pool.go`, `solution/go/pipeline/pipeline.go`, `solution/go/workerpool/pool_test.go`
- 대표 검증 명령: `make -C problem run-workerpool`, `make -C problem run-pipeline`, `make -C problem test`
- 핵심 개념 축: `worker pool은 제한된 수의 goroutine으로 작업을 소비하는 패턴이다.`, `pipeline은 단계별 channel 연결로 데이터 흐름을 분리한다.`, context.Context`는 중단 신호를 한 방향으로 전파하는 공통 장치다., `goroutine을 시작했다면 종료 경로와 channel close 책임도 같이 설계해야 한다.`
- chronology 복원 주석: 이 경로의 git 이력은 대체로 큰 source drop과 문서 보강 위주라 세밀한 시각 정보를 주지 못한다. 그래서 chronology는 README, 살아 있는 소스코드, 테스트, 현재 CLI 재실행 결과를 기준으로 Phase 1/2/3 형태로 복원했다.

## Git History Anchor

- `2026-03-08 46051f3 A large commit`
- `2026-03-09 69364e2 docs(notion): backend-go`
- `2026-03-12 0e12fb8 Track 3에 대한 전반적인 개선 완료 (backend go/node/spring, front react )`

## Chronology Ledger

                ### 1. Phase 1 - Pool과 worker goroutine으로 bounded concurrency를 먼저 고정한다

        - 당시 목표: Pool과 worker goroutine으로 bounded concurrency를 먼저 고정한다
        - 변경 단위: `solution/go/workerpool/pool.go`의 `NewPool`
        - 처음 가설: `NewPool`처럼 worker lifecycle을 먼저 고정해야 goroutine 누수 여부를 나중에 설명할 수 있다고 봤다.
        - 실제 조치: `solution/go/workerpool/pool.go`의 `NewPool`로 worker lifecycle과 cancellation path를 먼저 닫았다.
        - CLI: `make -C problem run-workerpool`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `Running worker pool example...`였다.
        - 핵심 코드 앵커:
        - `NewPool`: `solution/go/workerpool/pool.go`

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

        - 새로 배운 것: worker pool은 제한된 수의 goroutine으로 작업을 소비하는 패턴이다.
        - 다음: Generate, Filter, FanOut으로 channel pipeline을 조립한다
        ### 2. Phase 2 - Generate, Filter, FanOut으로 channel pipeline을 조립한다

        - 당시 목표: Generate, Filter, FanOut으로 channel pipeline을 조립한다
        - 변경 단위: `solution/go/pipeline/pipeline.go`의 `FanOut`
        - 처음 가설: `FanOut`를 통해 channel 흐름을 분리하면 backpressure와 cancellation을 코드 수준에서 읽기 쉬워진다고 판단했다.
        - 실제 조치: `solution/go/pipeline/pipeline.go`의 `FanOut`를 통해 channel fan-out, filter, sink 흐름을 조립했다.
        - CLI: `make -C problem run-pipeline`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `Running pipeline example...`였다.
        - 핵심 코드 앵커:
        - `FanOut`: `solution/go/pipeline/pipeline.go`

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

        - 새로 배운 것: pipeline은 읽기 쉽지만 stage가 많아질수록 디버깅이 어려워질 수 있다.
        - 다음: demo CLI와 benchmark로 concurrency 패턴 차이를 닫는다
        ### 3. Phase 3 - demo CLI와 benchmark로 concurrency 패턴 차이를 닫는다

        - 당시 목표: demo CLI와 benchmark로 concurrency 패턴 차이를 닫는다
        - 변경 단위: `solution/go/workerpool/pool_test.go`의 `TestPoolNoGoroutineLeaks`
        - 처음 가설: demo와 테스트가 같이 있어야 concurrency 패턴 차이가 수치와 출력 둘 다에서 보인다고 봤다.
        - 실제 조치: `solution/go/workerpool/pool_test.go`의 `TestPoolNoGoroutineLeaks`와 CLI demo를 함께 두어 leak 여부와 처리량 차이를 눈으로 확인하게 만들었다.
        - CLI: `make -C problem test`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `Running tests...`였다.
        - 핵심 코드 앵커:
        - `TestPoolNoGoroutineLeaks`: `solution/go/workerpool/pool_test.go`

        ```go
        func TestPoolNoGoroutineLeaks(t *testing.T) {
	handler := func(j Job) Result {
		return Result{JobID: j.ID, Value: j.Payload}
	}

	ctx := context.Background()
	pool := NewPool(ctx, 4, handler)

	for i := 0; i < 5; i++ {
        ```

        - 새로 배운 것: benchmark 숫자만 보고 실서비스 concurrency 정책으로 바로 옮기면 과적합될 수 있다.
        - 다음: 최종 글은 이 세 phase를 같은 순서로 묶어 development log로 다시 쓴다.

## Latest CLI Excerpt

        ```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/10-concurrency-patterns && make -C problem run-workerpool)
```

```text
Running worker pool example...
cd ../solution/go && go run ./cmd/workerpool
Job 3: result = 9
Job 1: result = 1
Job 4: result = 16
Job 2: result = 4
Job 8: result = 64
Job 7: result = 49
Job 6: result = 36
Job 5: result = 25
Job 12: result = 144
Job 10: result = 100
Job 11: result = 121
Job 9: result = 81
Job 16: result = 256
Job 13: result = 169
Job 15: result = 225
Job 14: result = 196
Job 18: result = 324
Job 20: result = 400
Job 17: result = 289
Job 19: result = 361
... (1 more lines)
```

```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/10-concurrency-patterns && make -C problem run-pipeline)
```

```text
Running pipeline example...
cd ../solution/go && go run ./cmd/pipeline
Primes from 1 to 50: [2 3 5 7 11 13 17 19 23 29 31 37 41 43 47]
Count: 15
```
