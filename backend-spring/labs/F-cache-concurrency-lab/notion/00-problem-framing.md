# Problem Framing — 동시에 밀려드는 요청 앞에서

## 이 랩이 존재하는 이유

서비스가 성장하면 반드시 마주치는 두 가지 문제가 있다. 첫째, 같은 데이터를 반복해서 조회하는 비용을 어떻게 줄일 것인가(캐시). 둘째, 같은 자원을 동시에 수정하려는 요청들을 어떻게 안전하게 처리할 것인가(동시성). F-cache-concurrency-lab은 이 두 문제를 재고 예약(inventory reservation)이라는 하나의 시나리오로 묶어서 다룬다.

재고 10개인 상품에 두 명이 동시에 3개씩 예약하려 하면 어떤 일이 벌어지는가? 네트워크 재시도로 같은 예약 요청이 두 번 들어오면 재고가 중복 차감되지 않으려면 어떻게 해야 하는가? 자주 조회되는 재고 상태를 매번 원본에서 읽지 않고 캐시에 둘 때, 재고가 변한 후에도 캐시가 이전 값을 돌려주면 어떻게 하는가?

이 랩은 이 질문들에 코드로 답한다.

## 구체적으로 무엇을 다루는가

**Idempotency Key를 통한 중복 요청 방지**. 예약 요청에 `Idempotency-Key` 헤더를 포함시킨다. 같은 키로 두 번 요청이 들어오면, 첫 번째 결과를 그대로 반환하고 재고를 중복 차감하지 않는다.

**synchronized 메서드를 통한 in-process 동시성 제어**. `reserve()` 메서드에 `synchronized` 키워드를 붙여서, 같은 JVM 안에서 동시에 실행되는 예약 요청들이 재고를 안전하게 차감하도록 했다.

**@Cacheable을 통한 캐시 읽기 경로**. `inventoryStatus()` 메서드에 `@Cacheable("inventory-status")`를 붙여서, 같은 SKU에 대한 재고 조회가 반복될 때 캐시된 값을 반환한다.

## 의도적으로 다루지 않는 것들

- **Redis 실제 캐시**: `CacheConfig`에서 `ConcurrentMapCacheManager`를 사용한다. Redis TTL, eviction 정책은 다루지 않는다.
- **분산 락(Distributed Lock)**: `synchronized`는 단일 JVM에서만 동작한다. Redisson이나 Redis SETNX 같은 분산 락은 다음 단계이다.
- **캐시 무효화(Cache Invalidation)**: `@CacheEvict`가 구현되어 있지 않다.
- **영속성**: 재고와 idempotency 데이터가 모두 ConcurrentHashMap에 있다. 서버 재시작 시 사라진다.

## 기술 스택과 제약 조건

| 항목 | 선택 |
|------|------|
| 언어 | Java 21 |
| 프레임워크 | Spring Boot 3.4.x |
| 캐시 | ConcurrentMapCacheManager (in-memory) |
| 동시성 제어 | synchronized (in-process) |
| 중복 방지 | ConcurrentHashMap |
| 인프라 | Redis 7 (Compose에 포함, 코드에서 미사용) |

## 성공 기준

1. 같은 Idempotency-Key로 두 번 예약해도 재고가 한 번만 차감되어야 한다
2. 재고 조회에서 `@Cacheable`이 동작해야 한다
3. `make test`와 `make smoke`가 통과해야 한다
4. 분산 락과 Redis 실제 캐시가 미구현임이 문서에 명시되어야 한다

## 남아 있는 불확실성

in-memory CacheManager가 실제 Redis 동작을 대표하지는 않는다. 그래도 "캐시가 무엇이고 왜 필요한가"를 먼저 체험하고 이후에 Redis로 전환하는 것이 학습 순서상 맞다고 판단했다.

