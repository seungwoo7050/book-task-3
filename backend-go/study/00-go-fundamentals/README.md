# 00 Go Fundamentals

## 이 트랙이 푸는 문제

- Go 문법, 타입, 테스트 도구를 따로 정리하지 않으면 이후 API와 DB 과제가 전부 문법 디버깅으로 무너진다.

## 이 트랙의 답

- 문법/도구, 타입/오류, 테스트/디버깅을 3개 입문 과제로 분리해 학습 루프를 짧게 만들었다.

## 프로젝트 순서

1. [01-go-syntax-and-tooling](01-go-syntax-and-tooling/README.md) : Go 문법과 `go run` / `go test` 루프를 가장 작은 문자열 처리 과제로 익히는 시작점이다.
2. [02-types-errors-interfaces](02-types-errors-interfaces/README.md) : struct, method, interface, custom error를 작은 상품 카탈로그로 묶어 타입 감각을 붙이는 과제다.
3. [03-testing-and-debugging](03-testing-and-debugging/README.md) : table-driven test, subtest, benchmark, race detector를 로그 파서와 recorder 구현으로 익히는 입문 심화 과제다.

## 졸업 기준

- 작은 CLI 또는 라이브러리를 혼자 작성하고 `go run`, `go test` 루프를 설명할 수 있어야 한다.
- table-driven test, benchmark, race detector가 언제 필요한지 코드 기준으로 설명할 수 있어야 한다.

## 대표 프로젝트

- [03-testing-and-debugging](03-testing-and-debugging/README.md) : 테스트와 동시성 오류를 처음부터 같이 다루는 프로젝트다.
