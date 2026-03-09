# 접근 과정 — 구현 방향을 잡기까지

## 모듈 초기화에서 시작

Go 프로젝트는 `go mod init`으로 시작한다. 이 과제의 모듈 경로는 `github.com/woopinbell/go-backend/study/00-go-fundamentals/01-go-syntax-and-tooling`이다. workspace 전체가 `go.work`로 묶여 있기 때문에, 이 모듈도 상위 workspace에 등록돼야 했다.

처음에 가장 먼저 결정한 건 패키지 구조였다. Go에서는 하나의 디렉터리가 하나의 패키지가 된다. 이 과제는 두 가지만 있으면 됐다:

1. **`lesson/`** — 문자열 정규화, 빈도 계산 로직을 담는 라이브러리 패키지
2. **`cmd/toolingdemo/`** — 실행 가능한 CLI 바이너리

이 두 패키지 분리는 Go의 관례를 따른 것이다. 라이브러리와 실행 진입점을 분리하면, 테스트할 때 `lesson/` 패키지만 독립적으로 검증할 수 있다.

## 정규화 로직의 선택

텍스트를 단어로 쪼개는 방법은 여러 가지가 있다. `strings.Split`으로 공백 기준으로 자를 수도 있고, 정규식을 쓸 수도 있다. 그런데 `strings.FieldsFunc`를 쓰면 "문자나 숫자가 아닌 모든 것"을 구분자로 지정할 수 있어서, 구두점 처리까지 한 번에 해결됐다.

```go
strings.FieldsFunc(strings.ToLower(text), func(r rune) bool {
    return !unicode.IsLetter(r) && !unicode.IsNumber(r)
})
```

이 한 줄이 소문자 변환과 구분자 분리를 동시에 처리한다. 정규식보다 코드가 짧고, 외부 패키지도 필요 없었다.

## 빈도 계산은 map으로

`map[string]int`는 Go에서 빈도 계산의 가장 기본적인 패턴이다. 특별할 것 없이 단어를 순회하면서 카운트를 올리면 된다. 다만 "가장 많이 나온 단어"를 고를 때 한 가지 결정이 필요했다. map 순회 순서는 Go에서 비결정적이다. 같은 빈도의 단어가 여러 개일 때 결과가 실행마다 달라질 수 있다.

그래서 `SortedKeys`를 만들어 키를 알파벳순으로 정렬한 뒤 순회하도록 했다. 이렇게 하면 같은 빈도의 단어들 중 알파벳순으로 앞에 있는 것이 항상 선택된다. 테스트의 기대값이 안정적으로 유지된다.

## struct로 결과 묶기

`BuildSummary` 함수는 `Summary` struct를 반환한다. 처음에는 `totalWords, uniqueWords, topWord`를 각각 반환하는 방식도 생각했다. 하지만 나중에 필드가 추가되면 호출부를 전부 고쳐야 한다는 걸 의식하고, struct로 묶는 쪽을 택했다.

```go
type Summary struct {
    TotalWords  int
    UniqueWords int
    TopWord     string
}
```

이 구조는 이 과제에서는 과할 수도 있지만, Go에서 여러 값을 반환할 때 struct를 쓰는 습관을 일찍 들이는 것이 목적이었다.

## CLI 진입점

`cmd/toolingdemo/main.go`는 최소한의 코드만 가진다. 기본 입력 문자열이 하드코딩돼 있고, `os.Args`로 인자를 받으면 그걸 사용한다. `flag` 패키지는 의도적으로 제외했다—이 단계에서는 `go run`과 `go test`만 경험하면 충분했다.
