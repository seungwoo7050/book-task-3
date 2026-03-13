# 03 Testing And Debugging — Analyzer Test Surface

`00-go-fundamentals/03-testing-and-debugging`는 table-driven test, subtest, benchmark, race detector를 로그 파서와 recorder 구현으로 익히는 입문 심화 과제다. 이 글에서는 Phase 1: 프로젝트 뼈대 만들기 -> Phase 2: 파싱 로직 구현 -> Phase 3: Recorder 구현 (동시성) 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- Phase 1: 프로젝트 뼈대 만들기
- Phase 2: 파싱 로직 구현
- Phase 3: Recorder 구현 (동시성)

## Day 1
### Session 1

- 당시 목표: table-driven test와 subtest를 실제 도메인 로직에 적용해야 한다.
- 변경 단위: `analyzer/`, `solution/go/analyzer/analyzer.go`
- 처음 가설: pprof 같은 도구 학습 이전에 테스트 습관과 data race 감지를 먼저 익히게 했다.
- 실제 진행: 디렉터리 구조 생성 도메인 로직 패키지 이름을 `analyzer/`로 정했다. 로그를 분석하는 게 이 패키지의 역할이니까. Event struct와 ParseLine 함수 (`solution/go/analyzer/analyzer.go`) `Event` struct: Category(string)와 DurationMS(int).

CLI:

```bash
mkdir -p 00-go-fundamentals/03-testing-and-debugging/{solution/go/cmd/debugdemo,solution/go/analyzer,docs/concepts,docs/references,problem}

cd 00-go-fundamentals/03-testing-and-debugging/go
go mod init github.com/woopinbell/go-backend/study/00-go-fundamentals/03-testing-and-debugging
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/analyzer/analyzer.go`

```go
type Event struct {
	Category   string
	DurationMS int
}

type Summary struct {
	Count     int
	TotalMS   int
	AverageMS int
}

type Recorder struct {
	mu     sync.Mutex
	events []Event
}

func ParseLine(line string) (Event, error) {
	parts := strings.Split(line, ",")
```

왜 이 코드가 중요했는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

새로 배운 것:

- table-driven test는 입력과 기대값을 나란히 놓아 케이스 확장을 쉽게 만든다.

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

- 다음 글에서는 `20-bench-race-and-debug-loop.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/analyzer/analyzer.go` 같은 결정적인 코드와 `cd 00-go-fundamentals/03-testing-and-debugging/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
