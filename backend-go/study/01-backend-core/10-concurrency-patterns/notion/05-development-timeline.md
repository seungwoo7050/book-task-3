# 타임라인 — 동시성 패턴 개발 전체 과정

## 1단계: 프로젝트 초기화

```bash
cd study/01-backend-core/10-concurrency-patterns/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/10-concurrency-patterns
```

외부 의존성 없음. Go 1.22+.

## 2단계: 디렉토리 구조 생성

```bash
mkdir -p workerpool
mkdir -p pipeline
mkdir -p cmd/workerpool
mkdir -p cmd/pipeline
```

```
solution/go/
├── go.mod
├── workerpool/
│   ├── pool.go
│   └── pool_test.go
├── pipeline/
│   ├── pipeline.go
│   └── pipeline_test.go
└── cmd/
    ├── workerpool/
    │   └── main.go
    └── pipeline/
        └── main.go
```

## 3단계: Job, Result 타입 정의 (workerpool/pool.go)

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
```

## 4단계: Pool 구조체 및 NewPool

```go
type Pool struct {
    ctx     context.Context
    cancel  context.CancelFunc
    jobs    chan Job
    results chan Result
    handler func(Job) Result
    wg      sync.WaitGroup
}
```

`NewPool`에서 worker goroutine을 즉시 시작한다.

## 5단계: worker 루프 구현

이중 select 패턴:
- 바깥: job 수신 또는 context 취소
- 안쪽: result 전송 또는 context 취소

## 6단계: Submit, Stop, Cancel 구현

- `Submit`: jobs 채널에 전송 (back-pressure)
- `Stop`: close(jobs) → wg.Wait
- `Cancel`: cancel() 호출

## 7단계: Pipeline 함수 구현 (pipeline/pipeline.go)

순서:
1. `Generate` — start~end 정수 생성, 채널 반환
2. `Filter` — predicate 만족하는 값만 통과
3. `Sink` — 채널의 모든 값을 슬라이스로 수집
4. `FanOut` — n개의 goroutine으로 병렬 처리

## 8단계: CMD 예제 작성

### Worker Pool 데모

```bash
go run ./cmd/workerpool
```

20개의 Job(1~20의 제곱)을 4 worker로 처리:

```
Job 1: result = 1
Job 2: result = 4
...
All jobs completed.
```

### Pipeline 데모

```bash
go run ./cmd/pipeline
```

1~50에서 소수만 필터링:

```
Primes from 1 to 50: [2 3 5 7 11 13 17 19 23 29 31 37 41 43 47]
Count: 15
```

## 9단계: 테스트 작성

```bash
go test ./workerpool/...
go test ./pipeline/...
```

Worker Pool 테스트:
- 모든 Job이 처리됨 확인
- Stop 후 goroutine 누수 없음 확인
- context cancellation으로 즉시 종료

Pipeline 테스트:
- Generate 범위 정확성
- Filter 조건 적용 확인
- Sink 수집 완전성
- context 취소 시 부분 결과

## 10단계: 벤치마크

```bash
go test -bench=. ./workerpool/...
go test -bench=. ./pipeline/...
```

## 11단계: Race detector

```bash
go test -race ./...
```

모든 채널 접근이 안전한지 확인.

## Makefile 빌드 명령어

```bash
make -C problem run-workerpool
make -C problem run-pipeline
make -C problem test
make -C problem bench
```

## 파일 목록

| 순서 | 파일 | 설명 |
|------|------|------|
| 1 | `go.mod` | 모듈 정의, 외부 의존성 없음 |
| 2 | `workerpool/pool.go` | Pool, Job, Result, worker, Submit, Stop, Cancel |
| 3 | `workerpool/pool_test.go` | 처리 완전성, goroutine 누수, cancellation 테스트 |
| 4 | `pipeline/pipeline.go` | Generate, Filter, Sink, FanOut |
| 5 | `pipeline/pipeline_test.go` | 범위, 필터, 수집, 취소 테스트 |
| 6 | `cmd/workerpool/main.go` | Pool 데모 (4 workers, 20 jobs) |
| 7 | `cmd/pipeline/main.go` | Pipeline 데모 (1-50 소수 필터) |
