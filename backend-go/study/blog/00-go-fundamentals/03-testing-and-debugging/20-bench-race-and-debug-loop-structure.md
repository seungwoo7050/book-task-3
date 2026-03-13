# 03 Testing And Debugging Structure

## 이 글이 답할 질문

- 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- parser, summarizer, recorder를 분리해 각 단위별 테스트 의도를 선명하게 만들었다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `00-go-fundamentals/03-testing-and-debugging` 안에서 `20-bench-race-and-debug-loop.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: Phase 4: 테스트 작성 -> Phase 5: CLI 바이너리 작성 -> Phase 6: 전체 검증
- 세션 본문: `solution/go/cmd/debugdemo/main.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/analyzer/analyzer_test.go`
- 코드 앵커 2: `solution/go/cmd/debugdemo/main.go`
- 코드 설명 초점: 이 테스트나 재현 스크립트는 프로젝트의 공개 표면을 말이 아니라 입력과 결과로 고정한다. 최종 글에서 이 증거를 빼면 구현은 보여도 완료 기준은 흐려진다.
- 개념 설명: subtest는 실패 지점을 이름으로 드러내 준다.
- 마지막 단락: pprof나 execution trace는 이 과제 범위에 넣지 않았다.
