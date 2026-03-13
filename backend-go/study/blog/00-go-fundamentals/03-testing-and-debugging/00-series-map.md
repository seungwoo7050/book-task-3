# 03 Testing And Debugging Series Map

`00-go-fundamentals/03-testing-and-debugging`는 table-driven test, subtest, benchmark, race detector를 로그 파서와 recorder 구현으로 익히는 입문 심화 과제다.

## 이 시리즈가 복원하는 것

- 시작점: table-driven test와 subtest를 실제 도메인 로직에 적용해야 한다.
- 구현 축: 로그 라인 파서, category 요약기, race-safe recorder를 `solution/go`에 구현했다.
- 검증 축: 2026-03-07 기준 `go run ./cmd/debugdemo`가 정상 실행됐다.
- 글 수: 2편

## 읽는 순서

- [10-analyzer-test-surface.md](10-analyzer-test-surface.md)
- [20-bench-race-and-debug-loop.md](20-bench-race-and-debug-loop.md)

## 근거 기준

- 소스코드, README, docs, 테스트, CLI만 입력 근거로 사용했다.
- 기존 blog 초안과 `_legacy` 본문은 입력 근거로 사용하지 않았다.
