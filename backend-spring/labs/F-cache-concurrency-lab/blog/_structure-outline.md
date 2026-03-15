# F-cache-concurrency-lab structure outline

## 글 목표

- 이 lab을 "분산 락 전 단계"라는 추상 표현보다, 현재 어떤 잘못된 동작까지 포함한 baseline인지로 다시 쓴다.
- stale cache와 loose idempotency semantics를 본문 중심에 둔다.
- 테스트 통과와 실제 운영상 한계를 동시에 보여 준다.

## 글 순서

1. 테스트가 무엇을 덮고 무엇을 놓치는지 먼저 정리한다.
2. `synchronized`, idempotency map, `@Cacheable`, `ConcurrentMapCacheManager`를 따라가며 현재 보장 범위를 설명한다.
3. manual HTTP로 stale read, same-key-different-request, missing-header error surface를 연결한다.
4. Redis-backed cache/distributed lock으로 넘어가기 전 현재 경계를 닫는다.

## 반드시 넣을 코드 앵커

- `CacheConcurrencyController.reserve()`
- `CacheConcurrencyDemoService.reserve()`
- `CacheConcurrencyDemoService.inventoryStatus()`
- `CacheConfig.cacheManager()`
- `Study2Application`의 `@EnableCaching`
- `CacheConcurrencyApiTest.idempotentReservationReturnsSameResult()`

## 반드시 넣을 검증 신호

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/F-cache-concurrency-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test'

docker run --rm -u $(id -u):$(id -g) -p 18085:8080 \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/F-cache-concurrency-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew bootRun'
```

## 반드시 남길 한계

- reservation 이후 stale cache가 남는 점
- same key + different payload를 막지 않는 점
- global lock granularity
- framework default 400과 custom problem detail이 섞여 있는 점
