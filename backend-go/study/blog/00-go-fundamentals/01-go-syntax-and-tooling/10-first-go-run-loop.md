# 01 Go Syntax And Tooling — First Go Run Loop

`00-go-fundamentals/01-go-syntax-and-tooling`는 Go 문법과 `go run` / `go test` 루프를 가장 작은 문자열 처리 과제로 익히는 시작점이다. 이 글에서는 Phase 1: 프로젝트 뼈대 만들기 -> Phase 2: 핵심 로직 구현 -> Phase 3: CLI 바이너리 작성 -> Phase 4: 테스트 작성 및 검증 -> Phase 5: 문서 작성 -> Phase 6: 최종 검증 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- Phase 1: 프로젝트 뼈대 만들기
- Phase 2: 핵심 로직 구현
- Phase 3: CLI 바이너리 작성
- Phase 4: 테스트 작성 및 검증
- Phase 5: 문서 작성
- Phase 6: 최종 검증

## Day 1
### Session 1

- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/`, `problem/`, `docs/`, `study/`, `solution/go/lesson/lesson.go`, `solution/go/cmd/toolingdemo/main.go`
- 처음 가설: CLI보다 문자열 처리 핵심 로직을 먼저 분리해 문법 학습이 I/O 처리에 묻히지 않게 했다.
- 실제 진행: 디렉터리 구조 생성 이 프로젝트는 study 디렉터리 아래에 위치한다. Go 소스는 `solution/go/` 하위에, 과제 명세는 `problem/`에, 학습 문서는 `docs/`에 분리했다. lesson 패키지 작성 (`solution/go/lesson/lesson.go`) 가장 먼저 `Summary` struct를 정의했다. 함수의 반환값을 struct로 묶는 Go 관용구를 입문 단계부터 익히기 위한 선택이었다.

CLI:

```bash
mkdir -p 00-go-fundamentals/01-go-syntax-and-tooling/{solution/go/cmd/toolingdemo,solution/go/lesson,docs/concepts,docs/references,problem}

cd 00-go-fundamentals/01-go-syntax-and-tooling/go
go mod init github.com/woopinbell/go-backend/study/00-go-fundamentals/01-go-syntax-and-tooling
```

검증 신호:

- `main` 함수는 기본 입력 문자열을 가지고 있고, `os.Args`에 인자가 있으면 그걸 사용한다. `lesson.BuildSummary`를 호출하고 결과를 `fmt.Printf`로 출력한다.
- 출력: total=10 unique=8 top=go
- 출력: total=3 unique=2 top=hello
- ok   github.com/woopinbell/go-backend/study/00-go-fundamentals/01-go-syntax-and-tooling/lesson
- --- PASS: TestBuildSummary (0.00s)

핵심 코드: `solution/go/lesson/lesson.go`

```go
type Summary struct {
	TotalWords  int
	UniqueWords int
	TopWord     string
}

func NormalizeWords(text string) []string {
	fields := strings.FieldsFunc(strings.ToLower(text), func(r rune) bool {
		return !unicode.IsLetter(r) && !unicode.IsNumber(r)
	})
	words := make([]string, 0, len(fields))
	for _, field := range fields {
		if field == "" {
			continue
		}
		words = append(words, field)
	}
	return words
```

왜 이 코드가 중요했는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

새로 배운 것:

- `strings.FieldsFunc`는 텍스트를 직접 루프 돌며 자르지 않아도 되는 표준 라이브러리 선택지다.

보조 코드: `solution/go/cmd/toolingdemo/main.go`

```go
func main() {
	input := "Go is simple, and simple tools make Go easier to learn."
	if len(os.Args) > 1 {
		input = strings.Join(os.Args[1:], " ")
	}

	summary := lesson.BuildSummary(input)
	fmt.Printf("total=%d unique=%d top=%s\n", summary.TotalWords, summary.UniqueWords, summary.TopWord)
}
```

왜 이 코드도 같이 봐야 하는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

CLI:

```bash
cd 00-go-fundamentals/01-go-syntax-and-tooling/go
go run ./cmd/toolingdemo
go test ./...
```

검증 신호:

- 2026-03-07 기준 `go run ./cmd/toolingdemo`가 정상 실행됐다.
- 2026-03-07 기준 `go test ./...`가 통과했다.

다음:

- stdin 입력과 flag 파싱은 현재 범위 밖이라 별도 검증하지 않았다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/lesson/lesson.go` 같은 결정적인 코드와 `cd 00-go-fundamentals/01-go-syntax-and-tooling/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
