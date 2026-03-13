# 03 Testing And Debugging Evidence Ledger

## 20 bench-race-and-debug-loop

- 시간 표지: Phase 4: 테스트 작성 -> Phase 5: CLI 바이너리 작성 -> Phase 6: 전체 검증
- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/cmd/debugdemo/main.go`
- 처음 가설: parser, summarizer, recorder를 분리해 각 단위별 테스트 의도를 선명하게 만들었다.
- 실제 조치: TestParseLine — table-driven test + subtest 세 케이스(valid, missing comma, empty category)를 struct 슬라이스로 정의. `t.Run`으로 각 케이스에 이름을 붙여 subtest로 실행. main.go 작성 (`solution/go/cmd/debugdemo/main.go`) 세 줄의 샘플 로그를 Summarize에 넣고 결과를 출력.

CLI:

```bash
cd solution/go
go run ./cmd/debugdemo
# search count=2 avg_ms=100
# checkout count=1 avg_ms=150

cd solution/go
go test ./... -bench=.
# ok   .../analyzer  0.XXXs
# BenchmarkSummarize-8  XXXXX  XXXXX ns/op
```

- 검증 신호:
- 세 줄의 샘플 로그를 Summarize에 넣고 결과를 출력.
- ok   .../analyzer  0.XXXs
- ok   .../analyzer (race 경고 없음)
- 2026-03-07 기준 `go run ./cmd/debugdemo`가 정상 실행됐다.
- 2026-03-07 기준 `go test ./... -bench=.`가 통과했다.
- 핵심 코드 앵커: `solution/go/analyzer/analyzer_test.go`
- 새로 배운 것: subtest는 실패 지점을 이름으로 드러내 준다.
- 다음: pprof나 execution trace는 이 과제 범위에 넣지 않았다.
