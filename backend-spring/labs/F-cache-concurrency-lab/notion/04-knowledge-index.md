# Knowledge Index — 캐시와 동시성의 핵심 개념 사전

## 핵심 개념

### Idempotency Key

같은 요청이 여러 번 전달되어도 결과가 한 번만 적용되도록 보장하는 식별자이다.

이 랩에서는 `Idempotency-Key` HTTP 헤더로 전달된다. `CacheConcurrencyDemoService`의 `reserve()` 메서드는 먼저 `idempotency` 맵에서 이 키를 확인하고, 이미 존재하면 이전 결과를 즉시 반환한다. 핵심은 "재고 차감 + 결과 저장"이 하나의 synchronized 블록 안에서 이루어진다는 점이다. 키 확인과 결과 저장 사이에 다른 스레드가 끼어들 수 없다.

현재 구현에서의 한계: idempotency 맵이 JVM 메모리에 있으므로 서버 재시작 시 사라진다. 프로덕션에서는 DB 테이블(`idempotency_keys`)이나 Redis SET에 TTL과 함께 저장하는 것이 일반적이다. Stripe의 결제 API가 이 패턴의 대표적인 사례이다.

### @Cacheable과 캐시 추상화

Spring의 `@Cacheable`은 메서드 호출을 AOP 프록시로 감싸서, 캐시에 값이 있으면 메서드를 실행하지 않고 바로 반환한다. 캐시 키는 기본적으로 메서드 인자로 결정된다.

```java
@Cacheable("inventory-status")
public InventoryStatus inventoryStatus(String sku) { ... }
```

여기서 `sku`가 캐시 키가 된다. `inventoryStatus("SKU-1")` 첫 호출에서 결과가 캐시에 저장되고, 이후 같은 인자로 호출하면 메서드 본문이 실행되지 않는다.

중요한 구분: `@Cacheable`은 캐시 **추상화**이지 캐시 **구현**이 아니다. 실제 저장소가 `ConcurrentMapCacheManager`인지 `RedisCacheManager`인지에 따라 동작이 달라진다. 이 랩에서는 전자를 사용하므로 네트워크 캐시가 아닌 JVM 메모리 캐시이다.

관련 어노테이션:
- `@CacheEvict`: 캐시에서 특정 키를 제거한다 (무효화)
- `@CachePut`: 메서드를 항상 실행하고 결과를 캐시에 넣는다 (갱신)
- `@Caching`: 여러 캐시 어노테이션을 조합한다

### synchronized와 모니터 락

Java의 `synchronized` 키워드는 메서드나 블록에 대해 JVM 레벨의 모니터 락을 건다. 같은 객체에 대해 두 스레드가 동시에 synchronized 메서드에 진입할 수 없다.

```java
public synchronized ReservationResult reserve(...) { ... }
```

이 코드에서 `this` (서비스 인스턴스)가 모니터 객체이다. Spring의 기본 빈 스코프가 싱글톤이므로 모든 요청이 같은 인스턴스를 공유한다. 따라서 동시 요청이 들어와도 한 번에 하나만 `reserve()`를 실행한다.

단일 서버에서는 충분하지만, 서버가 두 대 이상이면 각 JVM의 `synchronized`는 독립적이다. 이때 필요한 것이 **분산 락**이다.

### 캐시 무효화 (Cache Invalidation)

"컴퓨터 과학에서 어려운 두 가지 문제: 캐시 무효화와 이름 짓기" — Phil Karlton

캐시에 저장된 값이 원본 데이터와 달라지는 순간이 무효화가 필요한 시점이다. 이 랩에서는 `reserve()`가 재고를 차감하지만 `@CacheEvict`가 없어서 `inventoryStatus()`의 캐시는 이전 값을 계속 반환할 수 있다. 이 불일치가 캐시 무효화 문제의 핵심이다.

일반적인 전략:
- **TTL 기반**: 일정 시간 후 캐시가 자동 만료. 단순하지만 만료 전까지 stale data를 반환한다
- **이벤트 기반**: 데이터 변경 시 캐시를 즉시 무효화. 정확하지만 무효화 로직을 빠뜨리면 버그가 된다
- **Write-through**: 쓰기 시 캐시도 함께 갱신. 일관성이 높지만 쓰기 비용이 증가한다

### 분산 락 (Distributed Lock)

여러 서버(프로세스)가 동시에 같은 자원을 수정하지 못하도록 하는 잠금 메커니즘이다. Redis의 `SET NX EX` 명령어를 기반으로 구현하거나, Redisson 라이브러리의 `RLock`을 사용하는 것이 일반적이다.

```java
// Redisson 예시 (이 랩에서는 아직 미구현)
RLock lock = redisson.getLock("inventory:" + sku);
lock.tryLock(3, 10, TimeUnit.SECONDS);
try {
    // 재고 차감
} finally {
    lock.unlock();
}
```

`tryLock(waitTime, leaseTime, unit)`에서 waitTime은 락 획득 대기 시간, leaseTime은 락 자동 해제 시간이다. leaseTime이 필요한 이유는 락을 잡은 서버가 죽으면 영원히 락이 풀리지 않는 문제(deadlock)를 방지하기 위해서이다.

## 참고 자료

| 출처 | 확인 내용 | 날짜 |
|------|----------|------|
| docs/README.md | 테스트는 in-memory CacheManager 사용, Redisson은 next step | 작성 시점 |
| problem/README.md | "cache invalidation과 concurrent update를 inventory 시나리오로 구체화" | 작성 시점 |
| Spring Framework Docs — Cache Abstraction | @Cacheable, @CacheEvict, CacheManager 계층 구조 | 작성 시점 |
| Redisson Wiki — Distributed Locks | RLock API, tryLock 파라미터, watchdog 메커니즘 | 작성 시점 |

