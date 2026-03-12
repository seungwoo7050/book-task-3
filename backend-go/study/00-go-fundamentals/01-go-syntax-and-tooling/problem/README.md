# 문제 정의

문자열을 단어 단위로 정규화하고 빈도를 계산하는 작은 라이브러리와 CLI를 만든다.

## 성공 기준

- 입력 문자열을 소문자 단어 목록으로 정규화한다.
- 단어 빈도를 계산한다.
- 가장 많이 나온 단어를 찾는다.
- `go test`로 검증 가능해야 한다.

## 제공 자료와 출처

- `study`에서 새로 설계한 입문형 canonical 문제다.
- 외부 legacy 원문은 없고, 이 문서가 공개용 문제 정의다.
- 공개 구현은 [`solution/README.md`](../solution/README.md)와 `solution/go`에 둔다.

## 검증 기준

- `cd solution/go && go run ./cmd/toolingdemo`
- `cd solution/go && go test ./...`

## 제외 범위

- 파일 기반 입력 처리
- 실제 CLI 플래그 UX
