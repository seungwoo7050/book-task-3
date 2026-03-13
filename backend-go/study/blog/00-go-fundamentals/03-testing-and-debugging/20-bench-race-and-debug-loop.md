# 03 Testing And Debugging — Bench Race And Debug Loop

`00-go-fundamentals/03-testing-and-debugging`는 table-driven test, subtest, benchmark, race detector를 로그 파서와 recorder 구현으로 익히는 입문 심화 과제다. 이 글에서는 Phase 4: 테스트 작성 -> Phase 5: CLI 바이너리 작성 -> Phase 6: 전체 검증 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- Phase 4: 테스트 작성
- Phase 5: CLI 바이너리 작성
- Phase 6: 전체 검증

## Day 1
### Session 1

- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/cmd/debugdemo/main.go`
- 처음 가설: parser, summarizer, recorder를 분리해 각 단위별 테스트 의도를 선명하게 만들었다.
- 실제 진행: TestParseLine — table-driven test + subtest 세 케이스(valid, missing comma, empty category)를 struct 슬라이스로 정의. `t.Run`으로 각 케이스에 이름을 붙여 subtest로 실행. main.go 작성 (`solution/go/cmd/debugdemo/main.go`) 세 줄의 샘플 로그를 Summarize에 넣고 결과를 출력.

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

검증 신호:

- 세 줄의 샘플 로그를 Summarize에 넣고 결과를 출력.
- ok   .../analyzer  0.XXXs
- ok   .../analyzer (race 경고 없음)
- 2026-03-07 기준 `go run ./cmd/debugdemo`가 정상 실행됐다.
- 2026-03-07 기준 `go test ./... -bench=.`가 통과했다.

핵심 코드: `solution/go/analyzer/analyzer_test.go`

```go
func TestParseLine(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name    string
		line    string
		wantErr bool
	}{
		{name: "valid", line: "search,120"},
		{name: "missing comma", line: "search", wantErr: true},
		{name: "empty category", line: ",10", wantErr: true},
	}

	for _, tc := range tests {
		tc := tc
		t.Run(tc.name, func(t *testing.T) {
			t.Parallel()
			_, err := ParseLine(tc.line)
```

왜 이 코드가 중요했는가:

이 테스트나 재현 스크립트는 프로젝트의 공개 표면을 말이 아니라 입력과 결과로 고정한다. 최종 글에서 이 증거를 빼면 구현은 보여도 완료 기준은 흐려진다.

새로 배운 것:

- subtest는 실패 지점을 이름으로 드러내 준다.

보조 코드: `solution/go/cmd/debugdemo/main.go`

```go
func main() {
	lines := []string{"search,120", "search,80", "checkout,150"}
	summaries, err := analyzer.Summarize(lines)
	if err != nil {
		log.Fatal(err)
	}

	for category, summary := range summaries {
		fmt.Printf("%s count=%d avg_ms=%d\n", category, summary.Count, summary.AverageMS)
	}
}
```

왜 이 코드도 같이 봐야 하는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

CLI:

```bash
cd 00-go-fundamentals/03-testing-and-debugging/go
go run ./cmd/debugdemo
go test ./... -bench=.
```

검증 신호:

- 2026-03-07 기준 `go run ./cmd/debugdemo`가 정상 실행됐다.
- 2026-03-07 기준 `go test ./... -bench=.`가 통과했다.

다음:

- pprof나 execution trace는 이 과제 범위에 넣지 않았다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/analyzer/analyzer_test.go` 같은 결정적인 코드와 `cd 00-go-fundamentals/03-testing-and-debugging/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
