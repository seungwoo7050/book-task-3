# 문제 정의

Token Bucket rate limiter를 구현하고 per-client HTTP middleware로 통합한다.

## 성공 기준

- Token Bucket이 refill rate와 burst를 지원한다.
- `Allow()`가 thread-safe하게 동작한다.
- per-client limiter가 IP 기준으로 분리된다.
- stale entry cleanup goroutine이 context cancellation을 존중한다.
- 초과 요청에 `429`와 `Retry-After`를 반환한다.

## 제공 자료와 출처

- legacy `01-foundation/03-rate-limiter` 문제를 한국어 canonical 형태로 다시 정리한 문서다.
- 원문 세부 요구사항은 provenance로만 유지한다.
- 공개 구현은 [`solution/README.md`](../solution/README.md)와 `solution/go`에 둔다.

## 검증 기준

- `make -C problem test`
- `make -C problem bench`

## 제외 범위

- shared distributed limiter
- global quota coordination
