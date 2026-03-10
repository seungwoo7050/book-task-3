# Debug Log — @Cacheable이 증명하는 것과 증명하지 못하는 것

## 장애 상황: 라벨과 실제의 괴리

"Cache & Concurrency Lab" — 이 이름을 들으면 Redis 캐시에 재고를 올리고, 동시 요청을 분산 락으로 제어하는 장면을 기대한다. 그런데 테스트를 실행하면 Redis 커넥션 없이 모든 테스트가 통과한다.

```
./gradlew test
> Task :test
CacheConcurrencyApiTest > idempotentReservationReturnsSameResult() PASSED
BUILD SUCCESSFUL
```

빌드가 성공하는 것은 문제가 아니다. 문제는 이 성공이 Redis 캐시 동작을 증명한 것인지, 아니면 in-memory ConcurrentHashMap의 동작을 증명한 것인지 구분이 안 된다는 점이다.

## 잘못된 첫 번째 가정

`@Cacheable` 어노테이션이 코드에 있으니까 캐시 동작이 증명되었다고 생각하기 쉽다. 하지만 `@Cacheable`은 Spring의 캐시 추상화가 제공하는 AOP 프록시일 뿐이고, 실제 캐시가 `ConcurrentMapCacheManager`인지 `RedisCacheManager`인지는 별개의 문제이다.

```java
// CacheConfig.java
@Bean
@Primary
public CacheManager cacheManager() {
    return new ConcurrentMapCacheManager("inventory-status");
}
```

`@Primary`로 등록했기 때문에 auto-configured Redis cache가 있더라도 이 in-memory 구현이 선택된다. 테스트에서 `@Cacheable`이 동작하는 것은 사실이지만, 그것이 증명하는 것은 "Spring 캐시 추상화가 메서드 호출을 가로채서 결과를 저장한다"는 것이지 "Redis에 TTL을 설정하고 네트워크를 통해 캐시를 공유한다"는 것이 아니다.

## 근본 원인

이 랩의 목적과 이름 사이에 키워드 인플레이션이 있었다. "Cache & Concurrency"라는 라벨이 암시하는 수준(Redis + 분산 락)과 실제 구현 수준(ConcurrentMapCacheManager + synchronized) 사이의 간극을 명확히 하지 않으면, 면접에서 "Redis 캐시를 다뤄보셨다"고 말하고 나서 구체적인 질문에 답하지 못하는 상황이 생길 수 있다.

## 해결 과정

코드 변경이 아닌 문서 변경으로 대응했다. 검증 문서에 다음을 명시했다:

1. **현재 증명된 것**: Spring 캐시 추상화(`@Cacheable`)가 동작한다, `synchronized`가 단일 JVM에서 동시성을 제어한다, idempotency key로 중복 요청을 막는다
2. **아직 증명되지 않은 것**: Redis 캐시 저장/만료, 분산 환경에서의 락, 캐시 무효화 전략

이 구분이 있어야 "이 랩에서 무엇을 배웠는가"라는 질문에 정직하게 답할 수 있다.

```bash
make test   # 모든 테스트 통과 — in-memory 캐시 기반
```

## 남은 부채

- `inventoryStatus()` 호출이 실제 Redis에 캐시되는지 검증하는 테스트 추가 (Testcontainers + GenericContainer로 Redis 6379 매핑)
- Redisson `RLock`으로 `synchronized`를 교체하고, 분산 환경에서의 동시성 테스트 작성
- 캐시 무효화: `reserve()` 호출 후 `@CacheEvict`로 해당 SKU의 캐시를 제거하는 로직 추가 — 현재는 재고가 차감되어도 캐시된 값이 남아 있을 수 있다

