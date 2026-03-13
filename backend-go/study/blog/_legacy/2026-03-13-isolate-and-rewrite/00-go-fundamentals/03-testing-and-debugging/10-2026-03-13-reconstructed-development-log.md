# 03 Testing And Debugging 재구성 개발 로그

03 Testing And Debugging는 table-driven test, subtest, benchmark, race detector를 로그 파서와 recorder 구현으로 익히는 입문 심화 과제다.

이 글은 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 쓴 버전이다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다. 세밀한 shell history가 남아 있지 않아 시간 표지는 `Phase 1/2/3`처럼 재구성했고, 근거는 README, 살아 있는 소스코드, docs, 테스트, 현재 CLI 재실행 결과만 사용했다.

## 구현 순서 요약

- Phase 1: ParseLine과 Recorder로 로그 파싱 경계를 먼저 나눈다 - `solution/go/analyzer/analyzer.go`의 `ParseLine`
- Phase 2: Summarize와 debugdemo CLI로 요약 표면을 만든다 - `solution/go/analyzer/analyzer.go`의 `Summarize`
- Phase 3: table-driven test와 benchmark로 디버깅 루프를 고정한다 - `solution/go/analyzer/analyzer_test.go`의 `BenchmarkSummarize`

## Phase 1. ParseLine과 Recorder로 로그 파싱 경계를 먼저 나눈다

- 당시 목표: ParseLine과 Recorder로 로그 파싱 경계를 먼저 나눈다
- 변경 단위: `solution/go/analyzer/analyzer.go`의 `ParseLine`
- 처음 가설: `ParseLine`를 먼저 고정하면 I/O보다 데이터 규칙을 더 선명하게 설명할 수 있다고 봤다.
- 실제 진행: `solution/go/analyzer/analyzer.go`의 `ParseLine`를 중심으로 입력을 쪼개고, 계산 규칙을 작은 함수 단위로 고정했다.
- CLI: `cd solution/go && go run ./cmd/debugdemo`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `search count=2 avg_ms=100`였다.

핵심 코드:

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

왜 이 코드가 중요했는가: `ParseLine`는 `solution/go/analyzer/analyzer.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

- 새로 배운 것: table-driven test는 입력과 기대값을 나란히 놓아 케이스 확장을 쉽게 만든다.
- 다음: Summarize와 debugdemo CLI로 요약 표면을 만든다
## Phase 2. Summarize와 debugdemo CLI로 요약 표면을 만든다

- 당시 목표: Summarize와 debugdemo CLI로 요약 표면을 만든다
- 변경 단위: `solution/go/analyzer/analyzer.go`의 `Summarize`
- 처음 가설: `Summarize`를 중심에 두면 demo entrypoint는 얇은 연결층으로 남길 수 있다고 판단했다.
- 실제 진행: `solution/go/analyzer/analyzer.go`의 `Summarize`와 demo entrypoint를 연결해 사람이 읽는 출력 surface를 만들었다.
- CLI: `cd solution/go && go test ./... -bench=.`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `goos: darwin`였다.

핵심 코드:

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

왜 이 코드가 중요했는가: `Summarize`는 `solution/go/analyzer/analyzer.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

- 새로 배운 것: benchmark 수치만 보고 설계를 바꾸면 실제 서비스 병목과 어긋날 수 있다.
- 다음: table-driven test와 benchmark로 디버깅 루프를 고정한다
## Phase 3. table-driven test와 benchmark로 디버깅 루프를 고정한다

- 당시 목표: table-driven test와 benchmark로 디버깅 루프를 고정한다
- 변경 단위: `solution/go/analyzer/analyzer_test.go`의 `BenchmarkSummarize`
- 처음 가설: 테스트 이름 `BenchmarkSummarize`처럼 계약을 먼저 못 박아야 구현이 흔들리지 않는다고 봤다.
- 실제 진행: `solution/go/analyzer/analyzer_test.go`의 `BenchmarkSummarize`를 통해 regression or benchmark loop를 남겨 다음 단계 실험이 가능하게 했다.
- CLI: `cd solution/go && go test ./... -bench=.`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `goos: darwin`였다.

핵심 코드:

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

왜 이 코드가 중요했는가: `BenchmarkSummarize`는 `solution/go/analyzer/analyzer_test.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

- 새로 배운 것: 파싱 에러를 너무 넓게 뭉개면 디버깅 신호가 약해진다.
- 다음: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## CLI 1. 현재 저장소에서 다시 돌린 검증

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/00-go-fundamentals/03-testing-and-debugging && cd solution/go && go run ./cmd/debugdemo)
```

```text
search count=2 avg_ms=100
checkout count=1 avg_ms=150
```
## CLI 2. 현재 저장소에서 다시 돌린 검증

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/00-go-fundamentals/03-testing-and-debugging && cd solution/go && go test ./... -bench=.)
```

```text
goos: darwin
goarch: arm64
pkg: github.com/woopinbell/go-backend/study/00-go-fundamentals/03-testing-and-debugging/analyzer
cpu: Apple M1
BenchmarkSummarize-8   	   21664	     54895 ns/op
PASS
ok  	github.com/woopinbell/go-backend/study/00-go-fundamentals/03-testing-and-debugging/analyzer	2.224s
?   	github.com/woopinbell/go-backend/study/00-go-fundamentals/03-testing-and-debugging/cmd/debugdemo	[no test files]
```

## 이번 재작성에서 남은 것

- 이번 글을 지탱한 개념 축: table-driven test는 입력과 기대값을 나란히 놓아 케이스 확장을 쉽게 만든다., subtest는 실패 지점을 이름으로 드러내 준다., benchmark는 “더 빠르다”는 감각을 숫자로 바꾸는 최소 도구다., `sync.Mutex`로 감싼 recorder는 race detector를 통과시키는 가장 단순한 구조다.
- 최신 검증 메모: 현재 저장소에서 다시 실행한 명령은 모두 exit 0으로 끝났다.
- 다음 질문: 로그 parser와 recorder를 쪼갠 뒤 table-driven test, benchmark, race detector를 같은 루프로 돌린다.
