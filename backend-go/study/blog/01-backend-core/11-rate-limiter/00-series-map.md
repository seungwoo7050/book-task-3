# 11 Rate Limiter Series Map

`01-backend-core/11-rate-limiter`는 Token Bucket과 per-client limiter를 HTTP middleware까지 연결해 백엔드 보호 기초를 익히는 과제다.

## 이 시리즈가 복원하는 것

- 시작점: Token Bucket 알고리즘을 직접 구현해야 한다.
- 구현 축: token bucket limiter와 per-client limiter를 `solution/go`에 구현했다.
- 검증 축: 2026-03-07 기준 `make -C problem test`가 통과했다.
- 글 수: 2편

## 읽는 순서

- [10-token-bucket-core.md](10-token-bucket-core.md)
- [20-http-middleware-and-bench.md](20-http-middleware-and-bench.md)

## 근거 기준

- 소스코드, README, docs, 테스트, CLI만 입력 근거로 사용했다.
- 기존 blog 초안과 `_legacy` 본문은 입력 근거로 사용하지 않았다.
