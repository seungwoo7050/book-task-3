# 03 Testing And Debugging Evidence Ledger

이 문서는 기존 `blog/` 초안을 입력으로 읽지 않고, 살아 있는 근거만으로 chronology를 복원한 ledger다.

## 근거 묶음

- 프로젝트 요약: table-driven test, subtest, benchmark, race detector를 로그 파서와 recorder 구현으로 익히는 입문 심화 과제다.
- 구현 디렉터리: `solution/go`
- 주요 구현 파일: `solution/go/analyzer/analyzer.go`, `solution/go/analyzer/analyzer_test.go`
- 대표 검증 명령: `cd solution/go && go run ./cmd/debugdemo`, `cd solution/go && go test ./... -bench=.`
- 핵심 개념 축: `table-driven test는 입력과 기대값을 나란히 놓아 케이스 확장을 쉽게 만든다.`, `subtest는 실패 지점을 이름으로 드러내 준다.`, `benchmark는 “더 빠르다”는 감각을 숫자로 바꾸는 최소 도구다.`, sync.Mutex`로 감싼 recorder는 race detector를 통과시키는 가장 단순한 구조다.
- chronology 복원 주석: 이 경로의 git 이력은 대체로 큰 source drop과 문서 보강 위주라 세밀한 시각 정보를 주지 못한다. 그래서 chronology는 README, 살아 있는 소스코드, 테스트, 현재 CLI 재실행 결과를 기준으로 Phase 1/2/3 형태로 복원했다.

## Git History Anchor

- `2026-03-08 46051f3 A large commit`
- `2026-03-09 69364e2 docs(notion): backend-go`
- `2026-03-12 0e12fb8 Track 3에 대한 전반적인 개선 완료 (backend go/node/spring, front react )`

## Chronology Ledger

                ### 1. Phase 1 - ParseLine과 Recorder로 로그 파싱 경계를 먼저 나눈다

        - 당시 목표: ParseLine과 Recorder로 로그 파싱 경계를 먼저 나눈다
        - 변경 단위: `solution/go/analyzer/analyzer.go`의 `ParseLine`
        - 처음 가설: `ParseLine`를 먼저 고정하면 I/O보다 데이터 규칙을 더 선명하게 설명할 수 있다고 봤다.
        - 실제 조치: `solution/go/analyzer/analyzer.go`의 `ParseLine`를 중심으로 입력을 쪼개고, 계산 규칙을 작은 함수 단위로 고정했다.
        - CLI: `cd solution/go && go run ./cmd/debugdemo`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `search count=2 avg_ms=100`였다.
        - 핵심 코드 앵커:
        - `ParseLine`: `solution/go/analyzer/analyzer.go`

        ```go
        func ParseLine(line string) (Event, error) {
	parts := strings.Split(line, ",")
	if len(parts) != 2 {
		return Event{}, fmt.Errorf("invalid line %q", line)
	}
	duration, err := strconv.Atoi(strings.TrimSpace(parts[1]))
	if err != nil {
		return Event{}, fmt.Errorf("invalid duration: %w", err)
	}
        ```

        - 새로 배운 것: table-driven test는 입력과 기대값을 나란히 놓아 케이스 확장을 쉽게 만든다.
        - 다음: Summarize와 debugdemo CLI로 요약 표면을 만든다
        ### 2. Phase 2 - Summarize와 debugdemo CLI로 요약 표면을 만든다

        - 당시 목표: Summarize와 debugdemo CLI로 요약 표면을 만든다
        - 변경 단위: `solution/go/analyzer/analyzer.go`의 `Summarize`
        - 처음 가설: `Summarize`를 중심에 두면 demo entrypoint는 얇은 연결층으로 남길 수 있다고 판단했다.
        - 실제 조치: `solution/go/analyzer/analyzer.go`의 `Summarize`와 demo entrypoint를 연결해 사람이 읽는 출력 surface를 만들었다.
        - CLI: `cd solution/go && go test ./... -bench=.`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `goos: darwin`였다.
        - 핵심 코드 앵커:
        - `Summarize`: `solution/go/analyzer/analyzer.go`

        ```go
        func Summarize(lines []string) (map[string]Summary, error) {
	summaries := make(map[string]Summary)
	for _, line := range lines {
		event, err := ParseLine(line)
		if err != nil {
			return nil, err
		}
		summary := summaries[event.Category]
		summary.Count++
        ```

        - 새로 배운 것: benchmark 수치만 보고 설계를 바꾸면 실제 서비스 병목과 어긋날 수 있다.
        - 다음: table-driven test와 benchmark로 디버깅 루프를 고정한다
        ### 3. Phase 3 - table-driven test와 benchmark로 디버깅 루프를 고정한다

        - 당시 목표: table-driven test와 benchmark로 디버깅 루프를 고정한다
        - 변경 단위: `solution/go/analyzer/analyzer_test.go`의 `BenchmarkSummarize`
        - 처음 가설: 테스트 이름 `BenchmarkSummarize`처럼 계약을 먼저 못 박아야 구현이 흔들리지 않는다고 봤다.
        - 실제 조치: `solution/go/analyzer/analyzer_test.go`의 `BenchmarkSummarize`를 통해 regression or benchmark loop를 남겨 다음 단계 실험이 가능하게 했다.
        - CLI: `cd solution/go && go test ./... -bench=.`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `goos: darwin`였다.
        - 핵심 코드 앵커:
        - `BenchmarkSummarize`: `solution/go/analyzer/analyzer_test.go`

        ```go
        func BenchmarkSummarize(b *testing.B) {
	lines := make([]string, 0, 1000)
	for i := 0; i < 1000; i++ {
		lines = append(lines, fmt.Sprintf("search,%d", i%300))
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		if _, err := Summarize(lines); err != nil {
        ```

        - 새로 배운 것: 파싱 에러를 너무 넓게 뭉개면 디버깅 신호가 약해진다.
        - 다음: 최종 글은 이 세 phase를 같은 순서로 묶어 development log로 다시 쓴다.

## Latest CLI Excerpt

        ```bash
(cd /Users/woopinbell/work/book-task-3/study/00-go-fundamentals/03-testing-and-debugging && cd solution/go && go run ./cmd/debugdemo)
```

```text
search count=2 avg_ms=100
checkout count=1 avg_ms=150
```

```bash
(cd /Users/woopinbell/work/book-task-3/study/00-go-fundamentals/03-testing-and-debugging && cd solution/go && go test ./... -bench=.)
```

```text
goos: darwin
goarch: arm64
pkg: github.com/woopinbell/go-backend/study/00-go-fundamentals/03-testing-and-debugging/analyzer
cpu: Apple M1
BenchmarkSummarize-8   	   21090	     54910 ns/op
PASS
ok  	github.com/woopinbell/go-backend/study/00-go-fundamentals/03-testing-and-debugging/analyzer	1.965s
?   	github.com/woopinbell/go-backend/study/00-go-fundamentals/03-testing-and-debugging/cmd/debugdemo	[no test files]
```
