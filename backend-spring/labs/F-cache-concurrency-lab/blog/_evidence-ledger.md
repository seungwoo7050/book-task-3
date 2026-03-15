# F-cache-concurrency-lab evidence ledger

- 작성 기준일: 2026-03-14
- 복원 원칙: 기존 blog 본문은 입력 근거에서 제외하고, source, tests, 재실행 결과만 사용했다.
- 핵심 근거: `problem/README.md`, `docs/README.md`, `spring/Makefile`, `Study2Application.java`, `CacheConcurrencyController.java`, `CacheConcurrencyDemoService.java`, `CacheConfig.java`, `CacheConcurrencyApiTest.java`, `HealthApiTest.java`, `LabInfoApiSmokeTest.java`

## Phase 1. 테스트 contract와 실제 질문 확인

- 목표: 이 lab이 무엇을 baseline으로 증명하는지 먼저 확인한다.
- 확인 파일:
  - `spring/src/test/java/com/webpong/study2/app/CacheConcurrencyApiTest.java`
  - `spring/src/main/java/com/webpong/study2/app/cache/api/CacheConcurrencyController.java`
- 확인 결과:
  - 테스트는 same key replay와 final inventory value만 본다.
  - cache warm-up 이후 stale read 여부는 테스트하지 않는다.
  - `Idempotency-Key` header는 필수지만 request body validation은 `@Valid` 없이 선언만 돼 있다.

## Phase 2. reservation과 cache path 확인

- 목표: 현재 concurrency/caching 구현이 실제로 무엇을 보장하는지 확인한다.
- 확인 파일:
  - `spring/src/main/java/com/webpong/study2/app/cache/application/CacheConcurrencyDemoService.java`
  - `spring/src/main/java/com/webpong/study2/app/global/config/CacheConfig.java`
  - `spring/src/main/java/com/webpong/study2/app/Study2Application.java`
- 확인 결과:
  - `reserve()`는 service 전체에 대한 `synchronized`
  - idempotency map은 key만 기준으로 result를 재사용
  - `inventoryStatus()`는 `@Cacheable("inventory-status")`
  - cache eviction path가 없다
- 핵심 앵커:

```java
if (idempotency.containsKey(idempotencyKey)) {
  return idempotency.get(idempotencyKey);
}
```

```java
@Cacheable("inventory-status")
public InventoryStatus inventoryStatus(String sku) { ... }
```

- 메모:
  - per-SKU lock이 아니라 global method lock이다.
  - stale cache를 직접 재현할 수 있다.

## Phase 3. 2026-03-14 재실행 검증

- lint:

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/F-cache-concurrency-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'
```

- 결과: `BUILD SUCCESSFUL in 1m 23s`

- test:

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/F-cache-concurrency-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test'
```

- 결과: `BUILD SUCCESSFUL in 1m 20s`

- smoke:

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/F-cache-concurrency-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test --tests "*SmokeTest"'
```

- 결과: `BUILD SUCCESSFUL in 1m 15s`

- manual boot run:

```bash
docker run --rm -u $(id -u):$(id -g) -p 18085:8080 \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/F-cache-concurrency-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew bootRun'
```

- manual HTTP checks:
  - first `GET /api/v1/inventory/SKU-1` -> `{"available":10}`
  - reservation with `reserve-1`, `SKU-1`, `quantity=2` -> `remaining: 8`
  - second `GET /api/v1/inventory/SKU-1` -> still `{"available":10}` because stale cache
  - same `reserve-1` key with different request body for `SKU-2` -> original `SKU-1` result 재반환
  - insufficient inventory -> `400 problem+json`, `detail="Not enough inventory"`
  - missing `Idempotency-Key` header -> Spring default `400` JSON, custom problem detail 아님
  - `GET /api/v1/health/live` -> `200`, `X-Trace-Id` 확인

## 이번 Todo의 결론

- 이 lab은 inventory reservation baseline을 보여 주지만, 지금 상태 그대로를 "좋은 cache/idempotency 설계"로 읽으면 안 된다.
- 문서에 반드시 남겨야 할 현재 한계:
  - stale cache after reservation
  - idempotency key가 request fingerprint와 묶이지 않음
  - 전역 `synchronized` lock
  - error response 형식 불일치
