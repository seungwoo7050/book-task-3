# 01 Go Syntax And Tooling

## 한 줄 요약

Go 문법과 `go run` / `go test` 루프를 가장 작은 문자열 처리 과제로 익히는 시작점이다.

## 이 프로젝트가 푸는 문제

- 변수, 함수, 제어 흐름을 실제 코드로 익혀야 한다.
- slice와 map을 사용해 문자열을 정규화하고 빈도를 계산해야 한다.
- `go run`, `go test` 기본 루프를 스스로 반복할 수 있어야 한다.

## 내가 만든 답

- 문자열을 단어 단위로 정규화하는 라이브러리와 요약 CLI를 `solution/go`에 구현했다.
- 핵심 로직을 작은 함수로 나눠 REPL 없이도 `go test`로 바로 검증할 수 있게 했다.
- 문자열 처리와 빈도 계산을 입문형 표준 라이브러리 사용 범위 안에서 끝낸다.

## 핵심 설계 선택

- CLI보다 문자열 처리 핵심 로직을 먼저 분리해 문법 학습이 I/O 처리에 묻히지 않게 했다.
- 복잡한 입력 파싱을 뒤로 미뤄 문법, 함수 분해, 테스트 루프에 집중하게 했다.

## 검증

- `cd solution/go && go run ./cmd/toolingdemo`
- `cd solution/go && go test ./...`

## 제외 범위

- 파일 I/O와 CLI 플래그 파싱
- 외부 패키지 사용

## 읽는 순서

1. [problem/README.md](problem/README.md)에서 canonical 문제 정의와 성공 기준을 읽는다.
2. [solution/README.md](solution/README.md)에서 구현 범위와 검증 진입점을 확인한다.
3. [docs/README.md](docs/README.md)에서 개념 설명과 참고 문서를 따라간다.
4. [notion/README.md](notion/README.md)에서 접근 로그, 디버그 기록, 회고를 확인한다.

## 상태

- 상태: `verified`
- 제공 자료와 provenance: `study`에서 새로 추가한 입문 과제
