# 03 Testing And Debugging Evidence Ledger

## 10 analyzer-test-surface

- 시간 표지: Phase 1: 프로젝트 뼈대 만들기 -> Phase 2: 파싱 로직 구현 -> Phase 3: Recorder 구현 (동시성)
- 당시 목표: table-driven test와 subtest를 실제 도메인 로직에 적용해야 한다.
- 변경 단위: `analyzer/`, `solution/go/analyzer/analyzer.go`
- 처음 가설: pprof 같은 도구 학습 이전에 테스트 습관과 data race 감지를 먼저 익히게 했다.
- 실제 조치: 디렉터리 구조 생성 도메인 로직 패키지 이름을 `analyzer/`로 정했다. 로그를 분석하는 게 이 패키지의 역할이니까. Event struct와 ParseLine 함수 (`solution/go/analyzer/analyzer.go`) `Event` struct: Category(string)와 DurationMS(int).

CLI:

```bash
mkdir -p 00-go-fundamentals/03-testing-and-debugging/{solution/go/cmd/debugdemo,solution/go/analyzer,docs/concepts,docs/references,problem}

cd 00-go-fundamentals/03-testing-and-debugging/go
go mod init github.com/woopinbell/go-backend/study/00-go-fundamentals/03-testing-and-debugging
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/analyzer/analyzer.go`
- 새로 배운 것: table-driven test는 입력과 기대값을 나란히 놓아 케이스 확장을 쉽게 만든다.
- 다음: 다음 글에서는 `20-bench-race-and-debug-loop.md`에서 이어지는 경계를 다룬다.
