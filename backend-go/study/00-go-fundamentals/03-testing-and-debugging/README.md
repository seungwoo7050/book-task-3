# 03 Testing And Debugging

## 한 줄 요약

table-driven test, subtest, benchmark, race detector를 로그 파서와 recorder 구현으로 익히는 입문 심화 과제다.

## 이 프로젝트가 푸는 문제

- table-driven test와 subtest를 실제 도메인 로직에 적용해야 한다.
- benchmark로 구현 선택의 차이를 체감해야 한다.
- race-safe recorder를 만들어 동시성 기초 디버깅을 경험해야 한다.

## 내가 만든 답

- 로그 라인 파서, category 요약기, race-safe recorder를 `solution/go`에 구현했다.
- 단위 테스트와 benchmark를 함께 두어 기능 정확성과 성능 관찰을 한 번에 연습하게 했다.
- race detector로 recorder의 동시성 안전성을 검증한다.

## 핵심 설계 선택

- pprof 같은 도구 학습 이전에 테스트 습관과 data race 감지를 먼저 익히게 했다.
- parser, summarizer, recorder를 분리해 각 단위별 테스트 의도를 선명하게 만들었다.

## 검증

- `cd solution/go && go run ./cmd/debugdemo`
- `cd solution/go && go test ./... -bench=.`

## 제외 범위

- 실제 debugger 사용법
- 분산 추적 도구

## 읽는 순서

1. [problem/README.md](problem/README.md)에서 canonical 문제 정의와 성공 기준을 읽는다.
2. [solution/README.md](solution/README.md)에서 구현 범위와 검증 진입점을 확인한다.
3. [docs/README.md](docs/README.md)에서 개념 설명과 참고 문서를 따라간다.
4. [notion/README.md](notion/README.md)에서 접근 로그, 디버그 기록, 회고를 확인한다.

## 상태

- 상태: `verified`
- 제공 자료와 provenance: `study`에서 새로 추가한 입문 과제
