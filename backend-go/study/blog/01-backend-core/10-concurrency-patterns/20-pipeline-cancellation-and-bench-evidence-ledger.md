# 10 Concurrency Patterns Evidence Ledger

## 20 pipeline-cancellation-and-bench

- 시간 표지: 7단계: Pipeline 함수 구현 (pipeline/pipeline.go) -> 8단계: CMD 예제 작성 -> 9단계: 테스트 작성 -> 10단계: 벤치마크 -> 11단계: Race detector
- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/pipeline/pipeline.go`, `solution/go/pipeline/pipeline_test.go`
- 처음 가설: goroutine leak 방지를 핵심 검증 기준으로 잡아 단순 병렬 처리 예제와 구분했다.
- 실제 조치: 순서: `Generate` — start~end 정수 생성, 채널 반환 `Filter` — predicate 만족하는 값만 통과 `Sink` — 채널의 모든 값을 슬라이스로 수집 `FanOut` — n개의 goroutine으로 병렬 처리 Worker Pool 데모 20개의 Job(1~20의 제곱)을 4 worker로 처리: Worker Pool 테스트: 모든 Job이 처리됨 확인 Stop 후 goroutine 누수 없음 확인 context cancellation으로 즉시 종료

CLI:

```bash
go run ./cmd/workerpool

go run ./cmd/pipeline
```

- 검증 신호:
- `Filter` — predicate 만족하는 값만 통과
- 2026-03-07 기준 `make -C problem test`가 통과했다.
- 2026-03-07 기준 `make -C problem bench`가 통과했다.
- 남은 선택 검증: 실서비스 queue/backpressure 정책은 별도 과제로 남겼다.
- 핵심 코드 앵커: `solution/go/pipeline/pipeline.go`
- 새로 배운 것: pipeline은 단계별 channel 연결로 데이터 흐름을 분리한다.
- 다음: 실서비스 queue/backpressure 정책은 별도 과제로 남겼다.
