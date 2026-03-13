# 10 Concurrency Patterns Evidence Ledger

## 10 worker-pool-core

- 시간 표지: 1단계: 프로젝트 초기화 -> 2단계: 디렉토리 구조 생성 -> 3단계: Job, Result 타입 정의 (workerpool/pool.go) -> 4단계: Pool 구조체 및 NewPool -> 5단계: worker 루프 구현 -> 6단계: Submit, Stop, Cancel 구현
- 당시 목표: worker pool과 pipeline을 각각 구현해야 한다.
- 변경 단위: `solution/go/workerpool/pool.go`, `solution/go/cmd/workerpool/main.go`
- 처음 가설: 분산 큐 같은 외부 시스템을 제거하고 순수 Go 동시성 패턴에만 집중하게 했다.
- 실제 조치: 외부 의존성 없음. Go 1.22+. `NewPool`에서 worker goroutine을 즉시 시작한다. 이중 select 패턴: 바깥: job 수신 또는 context 취소 안쪽: result 전송 또는 context 취소 `Submit`: jobs 채널에 전송 (back-pressure) `Stop`: close(jobs) → wg.Wait `Cancel`: cancel() 호출

CLI:

```bash
cd study/01-backend-core/10-concurrency-patterns/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/10-concurrency-patterns

mkdir -p workerpool
mkdir -p pipeline
mkdir -p cmd/workerpool
mkdir -p cmd/pipeline
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/workerpool/pool.go`
- 새로 배운 것: worker pool은 제한된 수의 goroutine으로 작업을 소비하는 패턴이다.
- 다음: 다음 글에서는 `20-pipeline-cancellation-and-bench.md`에서 이어지는 경계를 다룬다.
