# Problem Framing

## Goal

`study2/labs/F-cache-concurrency-lab`의 목표는 Redis, cache invalidation, idempotency, reservation concurrency를 한 문제군으로 묶어 보는 것이다. inventory lookup, reservation endpoint, idempotency-key handling, Redisson-style lock boundary는 모두 “동시에 들어오는 요청을 어떻게 다룰 것인가”에 연결된다. 최소 성공 조건은 현재 scaffold가 cacheable path와 duplicate protection을 설명하고, real Redis assertion과 distributed lock이 아직 다음 단계라는 점을 명확히 남기는 것이다.

## Inputs and constraints

- Java/Spring:
  - Java 21
  - Spring Boot 3.4.x
- Services:
  - Redis
  - in-memory CacheManager for tests
- Correctness requirements:
  - idempotency key handling
  - reservation flow modeling
  - cache-aware read path
- Repository givens:
  - distributed locking is not yet implemented
- Decisions still needed:
  - cache와 concurrency를 한 랩에 같이 둘지

## Success criteria

- inventory lookup과 reservation flow가 cache/concurrency 예제로 읽혀야 한다.
- idempotency path가 드러나야 한다.
- documented commands가 통과해야 한다.
- Redis-heavy behavior와 Redisson lock이 아직 후속 개선임을 숨기지 않아야 한다.

## Uncertainty log

- in-memory CacheManager가 real Redis behavior를 충분히 대표하지는 않는다.
- 그래도 scaffold 단계에서는 cache와 idempotency 개념을 먼저 묶는 것이 낫다고 가정했다.
- distributed lock은 다음 확장으로 확인해야 한다.

