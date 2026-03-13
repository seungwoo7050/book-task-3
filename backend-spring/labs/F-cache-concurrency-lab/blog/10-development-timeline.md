# F-cache-concurrency-lab: 분산 도구보다 inventory 규칙을 먼저 고정한 과정

`F-cache-concurrency-lab`은 cache, idempotency, concurrency를 각각 따로 다루지 않는다. 이 랩이 먼저 보여 주는 건, 세 문제가 실제 서비스에서는 inventory reservation이라는 하나의 시나리오 안에서 겹쳐 온다는 사실이다.

구현 순서도 그 방향을 따른다. `problem/README.md`에서 inventory lookup과 reservation을 같은 시나리오로 묶고, `CacheConcurrencyApiTest`로 중복 요청 재생과 남은 재고 조회를 먼저 테스트했다. 이후 `CacheConcurrencyDemoService`에서 `synchronized`, idempotency map, `@Cacheable`을 연결하고, 마지막에 docs와 검증 기록으로 real Redis와 distributed lock을 아직 다음 단계로 남겼다.

## Phase 1. reservation을 두 번 보내도 같은 결과가 나와야 했다

이 주제를 잡을 때 가장 쉬운 유혹은 Redis나 Redisson부터 붙이는 일이다. 하지만 [`CacheConcurrencyApiTest`](../spring/src/test/java/com/webpong/study2/app/CacheConcurrencyApiTest.java)는 훨씬 작은 질문부터 고정한다. 같은 `Idempotency-Key`로 reservation을 두 번 보내면 남은 재고가 다시 줄어들지 않고, 이어지는 inventory 조회도 같은 값을 보여야 한다는 점이다.

```java
mockMvc.perform(
        post("/api/v1/inventory/reservations")
            .header("Idempotency-Key", "reserve-1")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"sku\":\"SKU-1\",\"quantity\":2}"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.remaining").value(8));

mockMvc.perform(get("/api/v1/inventory/SKU-1"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.available").value(8));
```

왜 이 코드가 중요했는가. concurrency 문제를 큰 인프라 용어로 풀기 전에, 같은 요청이 다시 왔을 때 무엇을 재사용하고 무엇을 다시 계산하지 않을지부터 정해야 하기 때문이다.

CLI도 그래서 단순하다.

```bash
cd spring
make test
```

`2026-03-13` 테스트 XML 기준으로 `CacheConcurrencyApiTest` 1개 테스트와 `HealthApiTest` 2개 테스트가 모두 통과했다. inventory reservation과 app health가 함께 baseline에 들어왔다는 뜻이다.

여기서 새로 보인 개념은 idempotency의 역할이었다. 중복 요청을 무시하는 것이 아니라, 이전 결과를 재사용해 상태를 다시 계산하지 않게 만드는 규칙이었다.

## Phase 2. `synchronized`, idempotency map, `@Cacheable`을 한 서비스에 묶었다

테스트 표면이 고정되고 나면 실제 규칙이 놓일 자리가 보인다. [`CacheConcurrencyDemoService`](../spring/src/main/java/com/webpong/study2/app/cache/application/CacheConcurrencyDemoService.java)는 `reserve()`를 `synchronized`로 감싸고, 같은 key면 이전 결과를 바로 돌려준다. 읽기 경로는 `@Cacheable("inventory-status")`로 분리한다.

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

@Cacheable("inventory-status")
public InventoryStatus inventoryStatus(String sku) {
  return new InventoryStatus(sku, inventory.getOrDefault(sku, 0));
}
```

cache 구현도 [`CacheConfig`](../spring/src/main/java/com/webpong/study2/app/global/config/CacheConfig.java)에서 baseline답게 단순하다.

```java
@Bean
@Primary
CacheManager cacheManager() {
  return new ConcurrentMapCacheManager("inventory-status");
}
```

왜 이 코드가 중요했는가. 여기서 처음으로 cache와 concurrency가 같은 business rule 안에 들어온다. reservation은 쓰기 경쟁과 중복 요청을 같이 다루고, 조회는 cacheable read path를 가진다. Redis 없이도 실제 문제 모양이 먼저 보이게 된다.

이 단계의 CLI는 smoke와 Compose까지 이어진다.

```bash
cd spring
make smoke
docker compose up --build
```

`docs/verification-report.md`는 `2026-03-09`에 F 랩이 in-memory `CacheManager`로 test를 통과했다고 별도로 적고 있다. `LabInfoApiSmokeTest` XML도 1개 테스트가 실패 없이 끝났다.

여기서 배운 건 baseline의 가치였다. 분산 락을 바로 붙이지 않았기 때문에, 언제 재고를 차감하고 언제 이전 결과를 재사용하는지가 훨씬 선명하게 보였다.

## Phase 3. real Redis를 미루면서도 확장 포인트를 잃지 않았다

cache/concurrency 글은 최종 해답만 남기기 쉽다. 하지만 [`docs/README.md`](../docs/README.md)는 Redis-backed cache assertion, distributed lock, idempotency persistence 분리를 아직 다음 단계로 남긴다고 분명히 적는다. 이 덕분에 현재 랩의 주제가 흐려지지 않는다.

```bash
cd spring
make lint
make test
make smoke
```

검증 신호는 아래처럼 정리된다.

- `2026-03-13` 기준 테스트 XML 4개 suite, 총 5개 테스트, 실패 0
- `2026-03-09` 검증 보고서 기준 lint, test, smoke, Compose health 확인 통과
- docs에 Redis-backed cache, distributed lock, idempotency persistence가 다음 단계로 명시돼 있음

이 랩이 남긴 가장 큰 배움은 concurrency에도 비교 기준점이 필요하다는 점이었다. baseline이 있어야 나중에 Redis나 distributed lock을 붙였을 때 무엇이 달라졌는지 설명할 수 있다. 다음 프로젝트인 `G-ops-observability-lab`은 이런 기능 랩들을 운영 관점에서 어떻게 관찰 가능한 상태로 만들지 따로 다룬다.
