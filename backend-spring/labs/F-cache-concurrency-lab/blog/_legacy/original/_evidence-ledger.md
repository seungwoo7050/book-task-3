# F-cache-concurrency-lab Evidence Ledger

- 복원 기준:
  - `problem/README.md`, `docs/README.md`, cache/idempotency 서비스 코드, 테스트, `2026-03-13` 재실행 CLI를 바탕으로 chronology를 복원했다.
- 기존 blog 처리:
  - 기존 `blog/`가 없어 격리 단계는 필요하지 않았다.

## Phase 1

- 시간 표지: Phase 1
- 당시 목표:
  - 캐시, idempotency, 재고 경합을 왜 같은 inventory 시나리오로 묶는지 먼저 정리한다.
- 변경 단위:
  - `problem/README.md`
  - `docs/README.md`
  - `spring/README.md`
- 처음 가설:
  - 캐시 문제와 동시성 문제를 따로 떼면 실제 서비스에서 겹쳐 오는 실패 패턴이 사라진다.
- 실제 조치:
  - inventory 조회, reservation, idempotency key, in-process concurrency를 current scope로 고정했다.
  - Redis와 distributed lock은 다음 단계로 남겼다.
- CLI:

```bash
cp .env.example .env
make run
```

- 검증 신호:
  - `spring/README.md`가 VSCode 터미널 진입점을 고정했고, docs는 in-memory `CacheManager`와 `synchronized` 기반 baseline이라는 현재 위치를 설명한다.
- 핵심 코드 앵커:
  - `CacheConcurrencyDemoService`, `CacheConcurrencyController`, `CacheConcurrencyApiTest`가 이 랩의 중심이다.
- 새로 배운 것:
  - idempotency와 locking은 같은 문제를 푸는 기술이 아니라, 서로 다른 실패 모드를 담당하는 규칙이다.
- 다음:
  - read path의 cache와 write path의 idempotency/concurrency를 각각 구현한다.

## Phase 2

- 시간 표지: Phase 2
- 당시 목표:
  - reservation write path와 inventory read path에 서로 다른 안정장치를 둔다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/cache/application/CacheConcurrencyDemoService.java`
  - `spring/src/main/java/com/webpong/study2/app/cache/api/CacheConcurrencyController.java`
  - `spring/src/main/java/com/webpong/study2/app/global/config/CacheConfig.java`
- 처음 가설:
  - duplicate request는 idempotency key로, 같은 JVM 안의 stock decrement는 `synchronized`로 먼저 막는 것이 baseline 설명에 가장 적합하다.
- 실제 조치:
  - `reserve()`에 `synchronized`를 걸고, idempotency map을 먼저 조회한 뒤 재고 차감 여부를 결정하게 했다.
  - `inventoryStatus()`에는 `@Cacheable("inventory-status")`를 붙여 read path를 분리했다.
- CLI:

```bash
make test
```

- 검증 신호:
  - `2026-03-13` 재실행에서 `make test`가 `BUILD SUCCESSFUL`로 끝났다.
- 핵심 코드 앵커:

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
  ReservationResult result =
      new ReservationResult(sku, quantity, inventory.get(sku), idempotencyKey);
  idempotency.put(idempotencyKey, result);
  return result;
}
```

- 새로 배운 것:
  - 같은 요청의 재실행을 막는 것과 동시에 들어온 다른 요청 사이의 경합을 막는 것은 전혀 다른 층위의 문제다.
- 다음:
  - duplicate reservation과 inventory read path가 실제 응답에서 어떻게 보이는지 확인한다.

## Phase 3

- 시간 표지: Phase 3
- 당시 목표:
  - idempotent reservation과 cached inventory read가 같은 시나리오에서 보이게 한다.
- 변경 단위:
  - `spring/src/test/java/com/webpong/study2/app/CacheConcurrencyApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`
- 처음 가설:
  - 같은 `Idempotency-Key`로 두 번 reserve를 호출하고 마지막에 inventory를 읽으면 baseline 목적은 충분히 증명된다.
- 실제 조치:
  - 동일한 key로 reservation을 두 번 보내도 남은 수량이 한 번만 줄어드는지 확인했다.
  - 이어서 `/api/v1/inventory/SKU-1` 조회가 8을 반환하는지 검증했다.
- CLI:

```bash
make test
make smoke
docker compose up --build
```

- 검증 신호:
  - `2026-03-13` 재실행 뒤 XML 리포트 4개, `failures=0`이 확인됐다.
  - `2026-03-09` 검증 기록에는 test 시 in-memory `CacheManager` 사용과 lint/test/smoke/Compose health 통과가 남아 있다.
- 핵심 코드 앵커:

```java
@Cacheable("inventory-status")
public InventoryStatus inventoryStatus(String sku) {
  return new InventoryStatus(sku, inventory.getOrDefault(sku, 0));
}
```

- 새로 배운 것:
  - 캐시는 읽기 비용을 줄이는 규칙이고, idempotency는 중복 side effect를 막는 규칙이며, lock은 경쟁 쓰기 자체를 막는 규칙이다. 세 문제를 한 랩에 묶어야 차이가 잘 보인다.
- 다음:
  - Redis-backed cache assertion, distributed lock, idempotency persistence 분리는 다음 단계로 넘긴다.
