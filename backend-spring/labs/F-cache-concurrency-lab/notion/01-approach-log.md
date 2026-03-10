# Approach Log — 캐시와 동시성을 하나로 묶은 이유

## 세 가지 선택지

캐시와 동시성을 어떻게 구성할 것인지 고민할 때, 세 가지 방향이 있었다.

**첫 번째 길: 캐시와 동시성을 별도 랩으로 분리하는 방식.** 각각의 주제를 더 깊이 다룰 수 있지만, 실제 서비스에서는 이 두 문제가 함께 등장한다. "재고를 캐시에 두었는데 동시에 예약이 들어왔다" — 이런 결합 시나리오를 보여줄 수 없다.

**두 번째 길: Redis 실제 커넥션과 Redisson 분산 락까지 첫 scaffold에 넣는 방식.** 가장 현실적이지만, Testcontainers로 Redis를 띄우고 Redisson 설정을 잡는 것만으로 상당한 분량이 된다. scaffold 단계에서는 "왜 캐시가 필요하고 왜 동시성 제어가 필요한가"라는 개념에 집중하는 것이 맞다.

**세 번째 길: in-process 동기화와 in-memory 캐시로 개념을 먼저 보여주는 방식.** 범위는 작지만, `synchronized`, `@Cacheable`, idempotency key라는 세 가지 핵심 개념이 하나의 시나리오에서 어떻게 맞물리는지 보여줄 수 있다.

세 번째 길을 택했다.

## 선택한 설계 방향

### Inventory 시나리오: 세 가지 문제를 하나로 묶기

재고 예약은 캐시, 동시성, 중복 방지를 동시에 다루기에 적합한 시나리오이다.

- **캐시**: 재고 상태를 자주 조회하므로 캐시에 둘 동기가 있다
- **동시성**: 여러 요청이 동시에 재고를 차감하려 하므로 동기화가 필요하다
- **중복 방지**: 네트워크 재시도로 같은 예약이 두 번 들어올 수 있으므로 idempotency가 필요하다

### 데이터 구조: ConcurrentHashMap 두 개

```java
private final Map<String, Integer> inventory = new ConcurrentHashMap<>();
private final Map<String, ReservationResult> idempotency = new ConcurrentHashMap<>();
```

`inventory`는 SKU별 재고 수량을 저장하고, `idempotency`는 idempotency key별 이전 결과를 저장한다. 둘 다 JVM 메모리에 있으므로 서버 재시작 시 사라진다. 이것은 DB나 Redis 영속성이 아니라 "개념의 가시성"을 위한 선택이다.

초기 재고: SKU-1 = 10개, SKU-2 = 5개. 생성자에서 하드코딩한다.

### 동시성 제어: synchronized

```java
public synchronized ReservationResult reserve(String sku, int quantity, String idempotencyKey) {
    if (idempotency.containsKey(idempotencyKey)) {
        return idempotency.get(idempotencyKey);
    }
    // ... 재고 확인, 차감, 결과 저장
}
```

`synchronized`는 이 메서드에 대해 JVM 레벨의 모니터 락을 건다. 같은 JVM에서 동시에 두 스레드가 이 메서드에 진입할 수 없다. 단순하지만 단일 서버에서는 충분히 동작한다. 분산 환경에서는 Redisson의 `RLock`이 대안이 된다.

### 캐시: ConcurrentMapCacheManager + @Cacheable

```java
@Cacheable("inventory-status")
public InventoryStatus inventoryStatus(String sku) {
    return new InventoryStatus(sku, inventory.getOrDefault(sku, 0));
}
```

`CacheConfig`에서 `ConcurrentMapCacheManager`를 `@Primary` `@Bean`으로 등록했다. Spring Boot의 auto-configured Redis cache 대신 이 in-memory 구현이 사용된다. `@Cacheable`의 동작 원리 — 메서드 호출 전에 캐시를 확인하고, 있으면 메서드를 실행하지 않고 캐시 값을 반환 — 를 보여주는 것이 목적이다.

### API 설계: Idempotency-Key 헤더

```
POST /api/v1/inventory/reservations
  Header: Idempotency-Key: reserve-1
  Body: {"sku":"SKU-1","quantity":2}

GET /api/v1/inventory/{sku}
```

Idempotency-Key를 `@RequestHeader`로 받는다. 이 패턴은 Stripe, PayPal 같은 결제 API에서 표준적으로 사용하는 방식이다.

## 폐기한 아이디어들

- **분산 락을 scaffold 필수로 두기**: Redisson 의존성 추가, Redis Testcontainers 설정, 락 timeout/retry 설정까지 포함하면 이 랩의 복잡도가 급격히 올라간다.
- **캐시를 완전히 생략하기**: 캐시 없이 동시성만 다루면 "F-cache-concurrency-lab"이라는 이름의 정체성이 약해진다. 캐시가 있어야 "캐시된 값과 실제 값의 불일치"라는 문제를 이야기할 수 있다.

## 근거 자료

docs/README.md에서 "test runs use an in-memory CacheManager instead of a real Redis cache"와 "Redisson locking is still a next step"이 현재 한계임을 확인했다. problem/README.md는 이 랩의 방향을 "cache invalidation과 concurrent update 문제를 inventory-style 시나리오로 구체화"로 정의하고 있다.

