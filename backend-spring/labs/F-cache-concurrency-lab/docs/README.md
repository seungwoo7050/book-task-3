# F-cache-concurrency-lab 설계 메모

이 문서는 cache/concurrency 랩의 현재 baseline과 다음 확장 방향을 정리한다.

## 현재 구현 범위

- inventory lookup endpoint
- reservation endpoint와 idempotency-key 처리
- `@Cacheable` 기반 inventory status 경로

## 의도적 단순화

- 테스트는 real Redis 대신 in-memory `CacheManager`를 사용한다
- reservation logic은 distributed lock이 아니라 in-process `synchronized`에 머문다
- Redisson은 다음 단계 후보로만 남겼다

## 다음 개선 후보

- Redis-backed cache assertion 추가
- distributed lock implementation과 conflict test
- idempotency persistence 분리
