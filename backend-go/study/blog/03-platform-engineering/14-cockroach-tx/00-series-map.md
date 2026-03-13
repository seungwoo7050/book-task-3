# 14 Cockroach TX Series Map

`03-platform-engineering/14-cockroach-tx`는 idempotency key, optimistic locking, transaction retry를 CockroachDB 호환 흐름으로 묶어 정합성 기초를 다지는 과제다.

## 이 시리즈가 복원하는 것

- 시작점: 중복 요청, 동시 요청, CockroachDB retry를 한 purchase 흐름에서 다뤄야 한다.
- 구현 축: repository, service, retry helper, HTTP purchase handler를 `solution/go`에 구현했다.
- 검증 축: 2026-03-08 기준 `make -C problem build`가 통과했다.
- 글 수: 3편

## 읽는 순서

- [10-schema-idempotency-and-retry.md](10-schema-idempotency-and-retry.md)
- [20-purchase-service-and-http-surface.md](20-purchase-service-and-http-surface.md)
- [30-repro-and-e2e-proof.md](30-repro-and-e2e-proof.md)

## 근거 기준

- 소스코드, README, docs, 테스트, CLI만 입력 근거로 사용했다.
- 기존 blog 초안과 `_legacy` 본문은 입력 근거로 사용하지 않았다.
