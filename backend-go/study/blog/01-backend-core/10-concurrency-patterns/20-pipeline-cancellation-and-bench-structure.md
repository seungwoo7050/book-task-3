# 10 Concurrency Patterns Structure

## 이 글이 답할 질문

- 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- goroutine leak 방지를 핵심 검증 기준으로 잡아 단순 병렬 처리 예제와 구분했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `01-backend-core/10-concurrency-patterns` 안에서 `20-pipeline-cancellation-and-bench.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 7단계: Pipeline 함수 구현 (pipeline/pipeline.go) -> 8단계: CMD 예제 작성 -> 9단계: 테스트 작성 -> 10단계: 벤치마크 -> 11단계: Race detector
- 세션 본문: `solution/go/pipeline/pipeline.go, solution/go/pipeline/pipeline_test.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/pipeline/pipeline.go`
- 코드 앵커 2: `solution/go/pipeline/pipeline_test.go`
- 코드 설명 초점: 이 블록은 병렬성과 보호 정책을 아이디어가 아니라 코드 invariant로 바꾼다. goroutine, channel, token을 어떤 경계로 묶었는지가 여기서 드러난다.
- 개념 설명: pipeline은 단계별 channel 연결로 데이터 흐름을 분리한다.
- 마지막 단락: 실서비스 queue/backpressure 정책은 별도 과제로 남겼다.
