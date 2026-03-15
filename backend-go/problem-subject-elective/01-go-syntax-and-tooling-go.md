# 01-go-syntax-and-tooling-go 문제지

## 왜 중요한가

문자열을 단어 단위로 정규화하고 빈도를 계산하는 작은 라이브러리와 CLI를 만든다.

## 목표

시작 위치의 구현을 완성해 입력 문자열을 소문자 단어 목록으로 정규화한다, 단어 빈도를 계산한다, 가장 많이 나온 단어를 찾는다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/00-go-fundamentals/01-go-syntax-and-tooling/solution/go/cmd/toolingdemo/main.go`
- `../study/00-go-fundamentals/01-go-syntax-and-tooling/solution/go/lesson/lesson.go`
- `../study/00-go-fundamentals/01-go-syntax-and-tooling/solution/go/lesson/lesson_test.go`
- `../study/00-go-fundamentals/01-go-syntax-and-tooling/solution/go/go.mod`

## starter code / 입력 계약

- `../study/00-go-fundamentals/01-go-syntax-and-tooling/solution/go/cmd/toolingdemo/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 입력 문자열을 소문자 단어 목록으로 정규화한다.
- 단어 빈도를 계산한다.
- 가장 많이 나온 단어를 찾는다.
- go test로 검증 가능해야 한다.

## 제외 범위

- 파일 기반 입력 처리
- 실제 CLI 플래그 UX
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `NormalizeWords`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestBuildSummary`와 `TestCountWords`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/backend-go/study/00-go-fundamentals/01-go-syntax-and-tooling/solution/go && GOWORK=off go test ./...`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-go/study/00-go-fundamentals/01-go-syntax-and-tooling/solution/go && GOWORK=off go test ./...
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`01-go-syntax-and-tooling-go_answer.md`](01-go-syntax-and-tooling-go_answer.md)에서 확인한다.
