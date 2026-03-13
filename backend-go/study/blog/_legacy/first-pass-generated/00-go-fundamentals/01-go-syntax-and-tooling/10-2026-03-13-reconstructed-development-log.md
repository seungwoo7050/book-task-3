# 01 Go Syntax And Tooling 재구성 개발 로그

01 Go Syntax And Tooling는 Go 문법과 `go run` / `go test` 루프를 가장 작은 문자열 처리 과제로 익히는 시작점이다.

이 글은 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 쓴 버전이다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다. 세밀한 shell history가 남아 있지 않아 시간 표지는 `Phase 1/2/3`처럼 재구성했고, 근거는 README, 살아 있는 소스코드, docs, 테스트, 현재 CLI 재실행 결과만 사용했다.

## 구현 순서 요약

- Phase 1: NormalizeWords와 CountWords로 문자열 정규화 규칙을 먼저 고정한다 - `solution/go/lesson/lesson.go`의 `NormalizeWords`
- Phase 2: BuildSummary와 toolingdemo CLI로 사람이 읽는 출력 표면을 만든다 - `solution/go/lesson/lesson.go`의 `BuildSummary`
- Phase 3: lesson_test와 `go test` 루프로 입문형 문자열 로직을 잠근다 - `solution/go/lesson/lesson_test.go`의 `TestBuildSummary`

                ## Phase 1. NormalizeWords와 CountWords로 문자열 정규화 규칙을 먼저 고정한다

        - 당시 목표: NormalizeWords와 CountWords로 문자열 정규화 규칙을 먼저 고정한다
        - 변경 단위: `solution/go/lesson/lesson.go`의 `NormalizeWords`
        - 처음 가설: `NormalizeWords`를 먼저 고정하면 I/O보다 데이터 규칙을 더 선명하게 설명할 수 있다고 봤다.
        - 실제 진행: `solution/go/lesson/lesson.go`의 `NormalizeWords`를 중심으로 입력을 쪼개고, 계산 규칙을 작은 함수 단위로 고정했다.
        - CLI: `cd solution/go && go run ./cmd/toolingdemo`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `total=11 unique=9 top=go`였다.

        핵심 코드:

        ```go
        func NormalizeWords(text string) []string {
	fields := strings.FieldsFunc(strings.ToLower(text), func(r rune) bool {
		return !unicode.IsLetter(r) && !unicode.IsNumber(r)
	})
	words := make([]string, 0, len(fields))
	for _, field := range fields {
		if field == "" {
			continue
		}
        ```

        왜 이 코드가 중요했는가: `NormalizeWords`는 `solution/go/lesson/lesson.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: strings.FieldsFunc`는 텍스트를 직접 루프 돌며 자르지 않아도 되는 표준 라이브러리 선택지다.
        - 다음: BuildSummary와 toolingdemo CLI로 사람이 읽는 출력 표면을 만든다
        ## Phase 2. BuildSummary와 toolingdemo CLI로 사람이 읽는 출력 표면을 만든다

        - 당시 목표: BuildSummary와 toolingdemo CLI로 사람이 읽는 출력 표면을 만든다
        - 변경 단위: `solution/go/lesson/lesson.go`의 `BuildSummary`
        - 처음 가설: `BuildSummary`를 중심에 두면 demo entrypoint는 얇은 연결층으로 남길 수 있다고 판단했다.
        - 실제 진행: `solution/go/lesson/lesson.go`의 `BuildSummary`와 demo entrypoint를 연결해 사람이 읽는 출력 surface를 만들었다.
        - CLI: `cd solution/go && go test ./...`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `?   	github.com/woopinbell/go-backend/study/00-go-fundamentals/01-go-syntax-and-tooling/cmd/toolingdemo	[no test files]`였다.

        핵심 코드:

        ```go
        func BuildSummary(text string) Summary {
	words := NormalizeWords(text)
	counts := CountWords(words)
	return Summary{
		TotalWords:  len(words),
		UniqueWords: len(counts),
		TopWord:     topWord(counts),
	}
}
        ```

        왜 이 코드가 중요했는가: `BuildSummary`는 `solution/go/lesson/lesson.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: 정렬은 `topWord` 결정의 안정성을 높여 주지만, 입력이 매우 크면 비용이 추가된다.
        - 다음: lesson_test와 `go test` 루프로 입문형 문자열 로직을 잠근다
        ## Phase 3. lesson_test와 `go test` 루프로 입문형 문자열 로직을 잠근다

        - 당시 목표: lesson_test와 `go test` 루프로 입문형 문자열 로직을 잠근다
        - 변경 단위: `solution/go/lesson/lesson_test.go`의 `TestBuildSummary`
        - 처음 가설: 테스트 이름 `TestBuildSummary`처럼 계약을 먼저 못 박아야 구현이 흔들리지 않는다고 봤다.
        - 실제 진행: `solution/go/lesson/lesson_test.go`의 `TestBuildSummary`를 통해 regression or benchmark loop를 남겨 다음 단계 실험이 가능하게 했다.
        - CLI: `cd solution/go && go test ./...`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `?   	github.com/woopinbell/go-backend/study/00-go-fundamentals/01-go-syntax-and-tooling/cmd/toolingdemo	[no test files]`였다.

        핵심 코드:

        ```go
        func TestBuildSummary(t *testing.T) {
	t.Parallel()

	summary := BuildSummary("Go makes Go tooling approachable, and Go tests stay fast.")
	if summary.TotalWords != 10 {
		t.Fatalf("total words = %d, want 10", summary.TotalWords)
	}
	if summary.UniqueWords != 8 {
		t.Fatalf("unique words = %d, want 8", summary.UniqueWords)
        ```

        왜 이 코드가 중요했는가: `TestBuildSummary`는 `solution/go/lesson/lesson_test.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: 구두점 제거 기준을 너무 넓게 잡으면 숫자나 영문자가 잘못 분리된다.
        - 다음: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

                ## CLI 1. 현재 저장소에서 다시 돌린 검증

        ```bash
(cd /Users/woopinbell/work/book-task-3/study/00-go-fundamentals/01-go-syntax-and-tooling && cd solution/go && go run ./cmd/toolingdemo)
```

```text
total=11 unique=9 top=go
```
        ## CLI 2. 현재 저장소에서 다시 돌린 검증

                ```bash
(cd /Users/woopinbell/work/book-task-3/study/00-go-fundamentals/01-go-syntax-and-tooling && cd solution/go && go test ./...)
```

```text
?   	github.com/woopinbell/go-backend/study/00-go-fundamentals/01-go-syntax-and-tooling/cmd/toolingdemo	[no test files]
ok  	github.com/woopinbell/go-backend/study/00-go-fundamentals/01-go-syntax-and-tooling/lesson	(cached)
```

## 이번 재작성에서 남은 것

- 이번 글을 지탱한 개념 축: strings.FieldsFunc`는 텍스트를 직접 루프 돌며 자르지 않아도 되는 표준 라이브러리 선택지다., map[string]int`는 가장 단순한 빈도 계산 구조다., 결과를 `Summary` struct로 묶으면 함수 반환값이 늘어나도 호출부가 덜 흔들린다.
- 최신 검증 메모: 현재 저장소에서 다시 실행한 명령은 모두 exit 0으로 끝났다.
- 다음 질문: 문자열 정규화와 단어 빈도 계산을 CLI보다 먼저 고정한 뒤, 가장 작은 `go run` / `go test` 루프를 닫는다.
