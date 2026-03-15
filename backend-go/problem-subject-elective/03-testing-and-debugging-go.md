# 03-testing-and-debugging-go 문제지

## 왜 중요한가

간단한 로그 라인을 파싱하고 category별 요약을 만들며, race-safe recorder를 구현한다.

## 목표

시작 위치의 구현을 완성해 "category,duration_ms" 형식의 라인을 파싱한다, category별 평균 지연 시간을 계산한다, concurrent append가 가능한 recorder를 만든다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/00-go-fundamentals/03-testing-and-debugging/solution/go/cmd/debugdemo/main.go`
- `../study/00-go-fundamentals/03-testing-and-debugging/solution/go/analyzer/analyzer.go`
- `../study/00-go-fundamentals/03-testing-and-debugging/solution/go/analyzer/analyzer_test.go`
- `../study/00-go-fundamentals/03-testing-and-debugging/solution/go/go.mod`

## starter code / 입력 계약

- `../study/00-go-fundamentals/03-testing-and-debugging/solution/go/cmd/debugdemo/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- "category,duration_ms" 형식의 라인을 파싱한다.
- category별 평균 지연 시간을 계산한다.
- concurrent append가 가능한 recorder를 만든다.
- benchmark와 subtest를 포함한다.

## 제외 범위

- pprof/trace 심화
- 외부 observability 도구
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `ParseLine`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestParseLine`와 `TestSummarize`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/backend-go/study/00-go-fundamentals/03-testing-and-debugging/solution/go && GOWORK=off go test ./...`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-go/study/00-go-fundamentals/03-testing-and-debugging/solution/go && GOWORK=off go test ./...
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`03-testing-and-debugging-go_answer.md`](03-testing-and-debugging-go_answer.md)에서 확인한다.
