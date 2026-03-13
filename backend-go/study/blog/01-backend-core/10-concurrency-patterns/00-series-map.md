# 10 Concurrency Patterns Series Map

`01-backend-core/10-concurrency-patterns`는 worker pool과 pipeline을 통해 goroutine lifecycle, channel, cancellation을 직접 다루는 본선 과제다.

## 이 시리즈가 복원하는 것

- 시작점: worker pool과 pipeline을 각각 구현해야 한다.
- 구현 축: worker pool과 three-stage pipeline을 `solution/go`에 구현했다.
- 검증 축: 2026-03-07 기준 `make -C problem test`가 통과했다.
- 글 수: 2편

## 읽는 순서

- [10-worker-pool-core.md](10-worker-pool-core.md)
- [20-pipeline-cancellation-and-bench.md](20-pipeline-cancellation-and-bench.md)

## 근거 기준

- 소스코드, README, docs, 테스트, CLI만 입력 근거로 사용했다.
- 기존 blog 초안과 `_legacy` 본문은 입력 근거로 사용하지 않았다.
