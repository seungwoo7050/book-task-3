# 개발 타임라인 — 처음부터 끝까지

이 문서는 프로젝트 01을 처음부터 완성까지 만드는 전체 과정을 시간순으로 기록한다. 소스코드를 읽는 것만으로는 알 수 없는 CLI 명령, 디렉터리 생성 순서, 도구 사용을 포함한다.

---

## Phase 1: 프로젝트 뼈대 만들기

### 1-1. 디렉터리 구조 생성

```bash
mkdir -p 00-go-fundamentals/01-go-syntax-and-tooling/{go/cmd/toolingdemo,go/lesson,docs/concepts,docs/references,problem}
```

이 프로젝트는 study 디렉터리 아래에 위치한다. Go 소스는 `go/` 하위에, 과제 명세는 `problem/`에, 학습 문서는 `docs/`에 분리했다.

### 1-2. Go 모듈 초기화

```bash
cd 00-go-fundamentals/01-go-syntax-and-tooling/go
go mod init github.com/woopinbell/go-backend/study/00-go-fundamentals/01-go-syntax-and-tooling
```

Go 1.22를 사용했다. 외부 의존성이 없으므로 `go.sum` 파일은 생성되지 않는다.

### 1-3. Workspace 등록

상위 `study/` 디렉터리에 `go.work` 파일이 있다. 새 모듈을 workspace에 추가해야 다른 모듈에서 참조할 수 있다.

```bash
cd study
go work use 00-go-fundamentals/01-go-syntax-and-tooling/go
```

---

## Phase 2: 핵심 로직 구현

### 2-1. lesson 패키지 작성 (`go/lesson/lesson.go`)

가장 먼저 `Summary` struct를 정의했다. 함수의 반환값을 struct로 묶는 Go 관용구를 입문 단계부터 익히기 위한 선택이었다.

그 다음 세 함수를 순서대로 작성했다:

1. **`NormalizeWords(text string) []string`** — `strings.ToLower`로 소문자 변환, `strings.FieldsFunc`로 토큰화. 문자/숫자가 아닌 모든 rune을 구분자로 처리했다.

2. **`CountWords(words []string) map[string]int`** — 단어 슬라이스를 순회하면서 map에 카운트.

3. **`BuildSummary(text string) Summary`** — 위 두 함수를 조합해서 `Summary`를 만드는 진입 함수.

### 2-2. 정렬 보조 함수 추가 (`SortedKeys`, `topWord`)

map 순회의 비결정성 문제를 해결하기 위해 `SortedKeys` 함수를 추가했다. `topWord`는 정렬된 키를 순회하면서 최고 빈도 단어를 고른다. 이 함수는 비공개(소문자 첫 글자)로 두었다.

---

## Phase 3: CLI 바이너리 작성

### 3-1. main.go 작성 (`go/cmd/toolingdemo/main.go`)

```bash
# 파일 생성
touch go/cmd/toolingdemo/main.go
```

`main` 함수는 기본 입력 문자열을 가지고 있고, `os.Args`에 인자가 있으면 그걸 사용한다. `lesson.BuildSummary`를 호출하고 결과를 `fmt.Printf`로 출력한다.

### 3-2. 첫 실행

```bash
cd go
go run ./cmd/toolingdemo
# 출력: total=10 unique=8 top=go
```

```bash
go run ./cmd/toolingdemo "hello world hello"
# 출력: total=3 unique=2 top=hello
```

---

## Phase 4: 테스트 작성 및 검증

### 4-1. 테스트 파일 작성 (`go/lesson/lesson_test.go`)

두 개의 테스트 함수를 작성했다:

- **`TestBuildSummary`**: 전체 파이프라인을 한 번에 검증. 입력 문장에서 총 단어 수, 고유 단어 수, 최빈 단어를 확인한다.
- **`TestCountWords`**: `CountWords` 함수만 독립적으로 검증.

두 테스트 모두 `t.Parallel()`을 사용해 병렬 실행 가능하게 했다.

### 4-2. 테스트 실행

```bash
cd go
go test ./...
# ok   github.com/woopinbell/go-backend/study/00-go-fundamentals/01-go-syntax-and-tooling/lesson

go test -v ./...
# === RUN   TestBuildSummary
# --- PASS: TestBuildSummary (0.00s)
# === RUN   TestCountWords
# --- PASS: TestCountWords (0.00s)
```

### 4-3. 특정 테스트만 실행해 보기

```bash
go test -run TestBuildSummary ./lesson/
```

이 방식은 테스트가 많아졌을 때 특정 함수만 빠르게 확인하는 데 유용하다.

---

## Phase 5: 문서 작성

### 5-1. 소스코드 외 문서들

다음 파일들을 순서대로 작성했다:

| 파일 | 내용 |
|------|------|
| `problem/README.md` | 과제 명세: 요구사항 4개 |
| `go/README.md` | 구현 모듈의 빌드/테스트/상태 요약 |
| `docs/README.md` | 문서 폴더 개요와 링크 |
| `docs/concepts/core-concepts.md` | 핵심 개념 3개, 트레이드오프, 실패하기 쉬운 지점 |
| `docs/references/README.md` | 참고 자료 2개 (Go Tour, strings 패키지) |
| `docs/verification.md` | 검증 명령과 결과 기록 |
| `README.md` | 프로젝트 루트 README (상태, 빌드, 테스트, 검증 방법) |

### 5-2. 검증 확인

```bash
cd study
make check-docs
# (에러 없으면 성공)
```

---

## Phase 6: 최종 검증

### 6-1. Makefile을 통한 전체 테스트

```bash
cd study
make test-new
# ==> 00-go-fundamentals/01-go-syntax-and-tooling/go
# ok   ...
```

### 6-2. 상태 변경

모든 빌드와 테스트가 통과한 뒤, README의 Status를 `verified`로 변경했다.

---

## 사용한 도구 요약

| 도구 | 버전/비고 | 용도 |
|------|-----------|------|
| Go | 1.22+ | 컴파일, 실행, 테스트 |
| `go mod init` | — | 모듈 초기화 |
| `go work use` | — | workspace에 모듈 등록 |
| `go run` | — | CLI 실행 |
| `go test` | — | 단위 테스트 |
| `make` | — | 전체 테스트, 문서 검증 |

외부 패키지나 Docker, 데이터베이스 등의 인프라 의존성은 없다. 순수 Go 표준 라이브러리만으로 완결되는 프로젝트다.
