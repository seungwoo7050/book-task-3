# Retrospective — 단순함이 남긴 것과 못 남긴 것

## 잘한 것: 세 문제를 하나의 시나리오로 묶기

캐시, 동시성, 중복 요청 방지 — 이 세 가지는 개별적으로 설명하면 추상적인 개념에 머무르기 쉽다. 하지만 "SKU-1의 재고 10개를 여러 요청이 동시에 예약한다"는 시나리오 안에 놓으면 세 문제가 왜 함께 발생하는지 자연스럽게 보인다.

캐시된 재고가 8개인데 실제로는 6개까지 줄었을 수 있다 → 캐시 무효화 문제.
두 스레드가 동시에 마지막 1개를 예약하려 한다 → 동시성 제어 문제.
네트워크 타임아웃으로 클라이언트가 같은 요청을 다시 보낸다 → 멱등성 문제.

하나의 inventory에 세 가지 질문이 모두 연결된다. 이 설계 판단은 맞았다.

idempotency key를 HTTP 헤더로 다룬 것도 좋았다. Stripe/PayPal의 실제 결제 API 패턴과 동일하므로, `capstone/commerce-backend`의 결제 flow를 설계할 때 자연스럽게 연결된다.

## 여전히 약한 것: 라벨과 깊이의 괴리

### Redis — 이름만 있고 코드는 없다

`compose.yaml`에 Redis 7 서비스가 정의되어 있고, `spring-boot-starter-data-redis` 의존성도 있다. 하지만 실제 코드에서 `RedisTemplate`이나 `RedisCacheManager`를 사용하는 곳은 없다. `CacheConfig`에서 `ConcurrentMapCacheManager`를 `@Primary`로 등록해서 Redis auto-configuration을 무시한다.

면접에서 "Redis 캐시를 사용해보셨나요?"라는 질문에 "네, 하지만 실제로는 in-memory CacheManager로 Spring 캐시 추상화만 검증했습니다"라고 답해야 정직하다.

### synchronized — 단일 서버의 한계

`synchronized`는 같은 JVM 안에서만 작동한다. 서버가 두 대 이상이면 — EC2 두 대, ECS 컨테이너 두 개 — 각 서버의 `synchronized`는 독립적이므로 재고 초과 차감이 발생할 수 있다. Redisson의 `RLock`이나 DB의 `SELECT ... FOR UPDATE`가 필요한 시점이다.

### 캐시 무효화의 부재

`@Cacheable`로 재고 상태를 캐시하지만, `reserve()`에서 재고를 차감한 뒤 캐시를 무효화하지 않는다. 즉, 예약 후에도 이전 캐시 값이 남아 있을 수 있다. `@CacheEvict`나 `@CachePut`을 추가해야 하는데, 현재 scaffold에서는 이 문제를 의도적으로 남겨두었다.

## 다시 볼 것

1. **Redisson 분산 락 추가**: `synchronized`를 `RLock`으로 교체하고, Testcontainers로 Redis를 띄워서 락 경합 테스트를 작성한다. `tryLock(waitTime, leaseTime, TimeUnit)` 패턴이 면접에서 자주 묻는다.

2. **@CacheEvict 추가**: `reserve()` 호출 후 해당 SKU의 캐시를 제거한다. 또는 `@CachePut`으로 갱신된 값을 바로 캐시에 넣는 방식도 고려한다. 두 전략의 차이(invalidation vs refresh)를 비교하는 테스트를 만들 수 있다.

3. **idempotency 영속화 분리**: 현재 `ConcurrentHashMap`에 저장된 idempotency 결과는 서버 재시작 시 사라진다. DB 테이블이나 Redis SET으로 옮기면, 서버 재배포 중에도 중복 방지가 유지된다.

4. **capstone 결제 flow 연계**: `capstone/commerce-backend`의 결제 API에서 idempotency key를 어떻게 다루는지 비교한다. lab의 단순한 구현이 실제 결제 시나리오에서 어떻게 확장되는지 확인하는 좋은 학습 경로이다.

