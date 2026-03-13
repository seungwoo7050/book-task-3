# 13 Distributed Log Core Series Map

`02-distributed-systems/13-distributed-log-core`는 append-only store, mmap index, segment rotation, log abstraction을 직접 구현해 commit log 핵심을 익히는 대표 과제다.

## 이 시리즈가 복원하는 것

- 시작점: length-prefixed store와 fixed-width index를 직접 구현해야 한다.
- 구현 축: store, index, segment, log core를 `solution/go`에 구현했다.
- 검증 축: 2026-03-07 기준 `make -C problem test`가 통과했다.
- 글 수: 3편

## 읽는 순서

- [10-store-index-and-segment-core.md](10-store-index-and-segment-core.md)
- [20-log-abstraction-and-rotation.md](20-log-abstraction-and-rotation.md)
- [30-tests-and-bench-evidence.md](30-tests-and-bench-evidence.md)

## 근거 기준

- 소스코드, README, docs, 테스트, CLI만 입력 근거로 사용했다.
- 기존 blog 초안과 `_legacy` 본문은 입력 근거로 사용하지 않았다.
