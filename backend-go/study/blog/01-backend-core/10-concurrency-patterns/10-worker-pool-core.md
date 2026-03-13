# 10 Concurrency Patterns — Worker Pool Core

`01-backend-core/10-concurrency-patterns`는 worker pool과 pipeline을 통해 goroutine lifecycle, channel, cancellation을 직접 다루는 본선 과제다. 이 글에서는 1단계: 프로젝트 초기화 -> 2단계: 디렉토리 구조 생성 -> 3단계: Job, Result 타입 정의 (workerpool/pool.go) -> 4단계: Pool 구조체 및 NewPool -> 5단계: worker 루프 구현 -> 6단계: Submit, Stop, Cancel 구현 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 1단계: 프로젝트 초기화
- 2단계: 디렉토리 구조 생성
- 3단계: Job, Result 타입 정의 (workerpool/pool.go)
- 4단계: Pool 구조체 및 NewPool
- 5단계: worker 루프 구현
- 6단계: Submit, Stop, Cancel 구현

## Day 1
### Session 1

- 당시 목표: worker pool과 pipeline을 각각 구현해야 한다.
- 변경 단위: `solution/go/workerpool/pool.go`, `solution/go/cmd/workerpool/main.go`
- 처음 가설: 분산 큐 같은 외부 시스템을 제거하고 순수 Go 동시성 패턴에만 집중하게 했다.
- 실제 진행: 외부 의존성 없음. Go 1.22+. `NewPool`에서 worker goroutine을 즉시 시작한다. 이중 select 패턴: 바깥: job 수신 또는 context 취소 안쪽: result 전송 또는 context 취소 `Submit`: jobs 채널에 전송 (back-pressure) `Stop`: close(jobs) → wg.Wait `Cancel`: cancel() 호출

CLI:

```bash
cd study/01-backend-core/10-concurrency-patterns/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/10-concurrency-patterns

mkdir -p workerpool
mkdir -p pipeline
mkdir -p cmd/workerpool
mkdir -p cmd/pipeline
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/workerpool/pool.go`

```go
type Job struct {
	ID      int
	Payload any
}
type Result struct {
	JobID int
	Value any
	Err   error
}
type Pool struct {
	ctx     context.Context
	cancel  context.CancelFunc
	jobs    chan Job
	results chan Result
	handler func(Job) Result
	wg      sync.WaitGroup
}
```

왜 이 코드가 중요했는가:

이 블록은 동기 write path와 비동기 side effect를 분리하는 설계의 핵심 증거다. "나중에 처리한다"가 아니라 "어떻게 안전하게 넘긴다"를 설명하게 해 준다.

새로 배운 것:

- worker pool은 제한된 수의 goroutine으로 작업을 소비하는 패턴이다.

보조 코드: `solution/go/cmd/workerpool/main.go`

```go
func main() {
	handler := func(j workerpool.Job) workerpool.Result {
		time.Sleep(10 * time.Millisecond)
		n := j.Payload.(int)
		return workerpool.Result{JobID: j.ID, Value: n * n}
	}

	ctx := context.Background()
	pool := workerpool.NewPool(ctx, 4, handler)
	go func() {
		for i := 1; i <= 20; i++ {
			pool.Submit(workerpool.Job{ID: i, Payload: i})
		}
		pool.Stop()
	}()
	for result := range pool.Results() {
		fmt.Printf("Job %d: result = %v\n", result.JobID, result.Value)
	}
```

왜 이 코드도 같이 봐야 하는가:

이 블록은 동기 write path와 비동기 side effect를 분리하는 설계의 핵심 증거다. "나중에 처리한다"가 아니라 "어떻게 안전하게 넘긴다"를 설명하게 해 준다.

CLI:

```bash
cd 01-backend-core/10-concurrency-patterns
make -C problem test
make -C problem bench
```

검증 신호:

- 2026-03-07 기준 `make -C problem test`가 통과했다.
- 2026-03-07 기준 `make -C problem bench`가 통과했다.

다음:

- 다음 글에서는 `20-pipeline-cancellation-and-bench.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/workerpool/pool.go` 같은 결정적인 코드와 `cd 01-backend-core/10-concurrency-patterns` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
