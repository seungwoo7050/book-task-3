# F-cache-concurrency-lab structure outline

## 글 목표

- cache, idempotency, concurrency를 inventory 시나리오 하나로 복원한다.
- macOS + VSCode 통합 터미널 기준의 테스트와 Compose 흐름을 유지한다.

## 글 순서

1. idempotent reservation 시나리오를 먼저 고정한 단계
2. `synchronized`, idempotency map, `@Cacheable`을 묶은 단계
3. Redis와 distributed lock을 뒤로 미룬 이유를 닫는 단계

## 반드시 넣을 코드 앵커

- `CacheConcurrencyApiTest.idempotentReservationReturnsSameResult()`
- `CacheConcurrencyDemoService.reserve()`
- `CacheConfig.cacheManager()`

## 반드시 넣을 CLI

```bash
cd spring
make test
make smoke
docker compose up --build
```

## 핵심 개념

- cache와 concurrency는 실제 서비스에서 같이 온다.
- idempotency는 이전 결과를 재사용하는 규칙이다.
