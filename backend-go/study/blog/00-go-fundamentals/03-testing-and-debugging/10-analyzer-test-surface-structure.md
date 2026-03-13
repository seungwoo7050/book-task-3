# 03 Testing And Debugging Structure

## 이 글이 답할 질문

- table-driven test와 subtest를 실제 도메인 로직에 적용해야 한다.
- pprof 같은 도구 학습 이전에 테스트 습관과 data race 감지를 먼저 익히게 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `00-go-fundamentals/03-testing-and-debugging` 안에서 `10-analyzer-test-surface.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: Phase 1: 프로젝트 뼈대 만들기 -> Phase 2: 파싱 로직 구현 -> Phase 3: Recorder 구현 (동시성)
- 세션 본문: `analyzer/, solution/go/analyzer/analyzer.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/analyzer/analyzer.go`
- 코드 앵커 2: `solution/go/cmd/debugdemo/main.go`
- 코드 설명 초점: 이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.
- 개념 설명: table-driven test는 입력과 기대값을 나란히 놓아 케이스 확장을 쉽게 만든다.
- 마지막 단락: 다음 글에서는 `20-bench-race-and-debug-loop.md`에서 이어지는 경계를 다룬다.
