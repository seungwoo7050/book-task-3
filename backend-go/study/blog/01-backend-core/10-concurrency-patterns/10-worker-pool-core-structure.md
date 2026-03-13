# 10 Concurrency Patterns Structure

## 이 글이 답할 질문

- worker pool과 pipeline을 각각 구현해야 한다.
- 분산 큐 같은 외부 시스템을 제거하고 순수 Go 동시성 패턴에만 집중하게 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `01-backend-core/10-concurrency-patterns` 안에서 `10-worker-pool-core.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 1단계: 프로젝트 초기화 -> 2단계: 디렉토리 구조 생성 -> 3단계: Job, Result 타입 정의 (workerpool/pool.go) -> 4단계: Pool 구조체 및 NewPool -> 5단계: worker 루프 구현 -> 6단계: Submit, Stop, Cancel 구현
- 세션 본문: `solution/go/workerpool/pool.go, solution/go/cmd/workerpool/main.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/workerpool/pool.go`
- 코드 앵커 2: `solution/go/cmd/workerpool/main.go`
- 코드 설명 초점: 이 블록은 동기 write path와 비동기 side effect를 분리하는 설계의 핵심 증거다. "나중에 처리한다"가 아니라 "어떻게 안전하게 넘긴다"를 설명하게 해 준다.
- 개념 설명: worker pool은 제한된 수의 goroutine으로 작업을 소비하는 패턴이다.
- 마지막 단락: 다음 글에서는 `20-pipeline-cancellation-and-bench.md`에서 이어지는 경계를 다룬다.
