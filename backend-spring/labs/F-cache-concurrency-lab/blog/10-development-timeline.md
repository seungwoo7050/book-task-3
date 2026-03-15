# F-cache-concurrency-lab: 재고 차감을 막는 baseline은 있지만 cache와 idempotency 의미는 아직 거칠게 남아 있는 scaffold

`F-cache-concurrency-lab`을 다시 읽으면서 가장 먼저 수정해야 했던 인상은 이 랩이 "Redis 전 단계의 깔끔한 baseline"처럼만 보인다는 점이었다. 실제 코드는 그렇게 단순하지 않다. reservation 경로는 중복 차감 방지와 in-process serialization을 어느 정도 보여 주지만, 조회 캐시는 쓰기 후에 무효화되지 않고, idempotency key는 request payload와 묶이지 않으며, missing header 같은 오류는 우리가 만든 problem detail format에도 안 들어온다.

2026-03-14에는 기존 blog를 입력 근거에서 제외하고, `CacheConcurrencyController`, `CacheConcurrencyDemoService`, `CacheConfig`, `Study2Application`, 테스트, 실제 컨테이너 검증과 `curl` 재실행만으로 문서를 다시 썼다. 다시 보면 이 lab의 중심 질문은 "분산 락을 왜 아직 안 썼는가"보다 "현재 baseline이 정확히 무엇을 보장하고, 무엇은 아직 깨지는가"에 더 가깝다.

## Phase 1. 테스트는 중복 차감 방지를 보여 주지만 cache 일관성까지 검증하진 않는다

[`CacheConcurrencyApiTest`](../spring/src/test/java/com/webpong/study2/app/CacheConcurrencyApiTest.java)는 같은 `Idempotency-Key`로 reservation을 두 번 보내도 `remaining=8`이 유지되고, 마지막 inventory 조회에서 `available=8`이 보이면 성공이라고 본다.

```java
mockMvc
    .perform(
        post("/api/v1/inventory/reservations")
            .header("Idempotency-Key", "reserve-1")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"sku\":\"SKU-1\",\"quantity\":2}"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.remaining").value(8));
```

이 테스트는 중복 요청이 다시 inventory를 깎지 않는다는 사실은 보여 준다. 하지만 중요한 전제가 하나 숨어 있다. inventory GET을 reservation 이전에 먼저 호출하지 않는다는 점이다. 이 전제 덕분에 캐시가 stale read를 만드는지 여부는 테스트 밖에 남아 있었다.

실제 수동 재검증에서 이 빈틈은 바로 드러났다. 먼저 `GET /api/v1/inventory/SKU-1`을 호출해 `10`을 캐시한 뒤 reservation을 만들고 다시 GET을 치자, 응답은 여전히 `10`이었다.

```bash
curl -sS http://127.0.0.1:18085/api/v1/inventory/SKU-1
curl -sS -X POST http://127.0.0.1:18085/api/v1/inventory/reservations \
  -H 'Idempotency-Key: reserve-1' \
  -H 'Content-Type: application/json' \
  -d '{"sku":"SKU-1","quantity":2}'
curl -sS http://127.0.0.1:18085/api/v1/inventory/SKU-1
```

즉 이 lab의 cache path는 존재하지만, 아직 inventory mutation과 연결된 invalidation 전략은 없다.

## Phase 2. reservation 보호는 있지만 락 범위와 idempotency 의미는 꽤 거칠다

실제 규칙은 [`CacheConcurrencyDemoService`](../spring/src/main/java/com/webpong/study2/app/cache/application/CacheConcurrencyDemoService.java)에 있다. `reserve()`는 메서드 전체를 `synchronized`로 감싸고, idempotency map에 key가 있으면 이전 결과를 그대로 반환한다.

```java
public synchronized ReservationResult reserve(String sku, int quantity, String idempotencyKey) {
  if (idempotency.containsKey(idempotencyKey)) {
    return idempotency.get(idempotencyKey);
  }
  int available = inventory.getOrDefault(sku, 0);
  if (available < quantity) {
    throw new IllegalArgumentException("Not enough inventory");
  }
  inventory.put(sku, available - quantity);
  ...
}
```

이 구조가 보여 주는 건 분명하다. 같은 JVM 안에서는 동시에 두 쓰기 경로가 inventory map을 엇갈리게 건드리지 못한다. 하지만 이 메서드는 SKU별 lock이 아니라 서비스 인스턴스 전체 lock이다. `SKU-1`을 예약하든 `SKU-2`를 예약하든 모두 같은 monitor를 공유한다. 그래서 per-key concurrency control을 설명하는 단계는 아직 아니다.

idempotency semantics도 생각보다 느슨하다. key만 같으면 요청 내용이 달라도 이전 결과를 그대로 돌려준다. 2026-03-14 수동 재검증에서 이를 직접 확인했다.

```bash
curl -sS -X POST http://127.0.0.1:18085/api/v1/inventory/reservations \
  -H 'Idempotency-Key: reserve-1' \
  -H 'Content-Type: application/json' \
  -d '{"sku":"SKU-2","quantity":1}'
```

응답은 새로운 `SKU-2` 결과가 아니라 기존 `SKU-1` reservation 결과였다.

```json
{"sku":"SKU-1","quantity":2,"remaining":8,"idempotencyKey":"reserve-1"}
```

즉 현재 구현은 "같은 요청의 안전한 재실행"보다는 "같은 키면 무조건 첫 결과를 재사용"에 더 가깝다.

## Phase 3. 캐시는 실제로 켜져 있고, 그래서 stale read 문제가 더 분명하다

이 lab은 cache를 말로만 언급하는 게 아니다. [`Study2Application`](../spring/src/main/java/com/webpong/study2/app/Study2Application.java)에 `@EnableCaching`이 있고, [`CacheConfig`](../spring/src/main/java/com/webpong/study2/app/global/config/CacheConfig.java)는 `ConcurrentMapCacheManager("inventory-status")`를 primary cache manager로 등록한다.

```java
@EnableCaching
public class Study2Application { ... }
```

```java
@Bean
@Primary
CacheManager cacheManager() {
  return new ConcurrentMapCacheManager("inventory-status");
}
```

그리고 `inventoryStatus()`는 `@Cacheable("inventory-status")`를 단다.

```java
@Cacheable("inventory-status")
public InventoryStatus inventoryStatus(String sku) {
  return new InventoryStatus(sku, inventory.getOrDefault(sku, 0));
}
```

문제는 write path에 `@CacheEvict`나 explicit eviction이 전혀 없다는 점이다. 그래서 이 lab은 실제로 cacheable read path를 갖고 있지만, 동시에 stale read 재현도 가능하다. 단지 "real Redis가 아니라 in-memory cache manager를 쓴다"보다 더 중요한 사실은, 현재 cache contract 자체가 write-after-read consistency를 보장하지 않는다는 점이다.

## Phase 4. 에러 표면을 보면 어떤 오류는 custom problem detail, 어떤 오류는 Spring 기본 400으로 갈라진다

재고 부족은 service가 `IllegalArgumentException("Not enough inventory")`를 던지기 때문에 global handler를 거쳐 `application/problem+json`으로 내려온다.

```bash
curl -i -X POST http://127.0.0.1:18085/api/v1/inventory/reservations \
  -H 'Idempotency-Key: reserve-2' \
  -H 'Content-Type: application/json' \
  -d '{"sku":"SKU-2","quantity":6}'
```

응답은 `400`, `code="bad_request"`, `detail="Not enough inventory"`였다. 그런데 `Idempotency-Key` header를 아예 빼면 상황이 달라진다. 이 경우는 service까지 가지 못하고 Spring MVC argument resolution 단계에서 막히기 때문에, global handler가 아니라 Spring 기본 `400` JSON으로 떨어진다.

```bash
curl -i -X POST http://127.0.0.1:18085/api/v1/inventory/reservations \
  -H 'Content-Type: application/json' \
  -d '{"sku":"SKU-1","quantity":1}'
```

응답은 problem detail이 아니라 아래 형태였다.

```json
{"timestamp":"2026-03-14T04:30:49.250+00:00","status":400,"error":"Bad Request","path":"/api/v1/inventory/reservations"}
```

이 차이는 운영 문서에서 꽤 중요하다. 현재 API error surface는 단일 형식으로 정리돼 있지 않다.

## Phase 5. 이번 Todo는 테스트 통과와 실제 깨지는 지점을 같이 남겼다

이번 검증은 모두 2026-03-14에 다시 실행했다. 로컬 JRE가 없어서 host `make` 대신 `eclipse-temurin:21-jdk` 컨테이너를 사용했다.

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/F-cache-concurrency-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'

docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/F-cache-concurrency-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test'

docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/F-cache-concurrency-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test --tests "*SmokeTest"'
```

세 명령 모두 `BUILD SUCCESSFUL`이었다. 이후 `bootRun`을 18085 포트로 띄워 stale cache, repeated reservation, mismatched request with same idempotency key, insufficient inventory, missing header, `GET /api/v1/health/live`까지 직접 확인했다.

그래서 지금의 `F-cache-concurrency-lab`을 가장 정확하게 요약하면 이렇다. inventory reservation baseline은 존재한다. 중복 차감 방지와 in-process serialization도 보여 준다. 하지만 동시에 현재 구현은 stale read를 만들고, idempotency key를 payload 검증 없이 재사용하며, lock granularity는 전역이고, error response 형식도 통일되지 않았다. 이 상태를 숨기지 않고 적어 두는 편이 이후 Redis-backed cache나 distributed lock으로 확장할 때 비교 기준을 훨씬 선명하게 만들어 준다.
