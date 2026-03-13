# 같은 inventory 시나리오 안에서 세 문제가 분리된다

`F-cache-concurrency-lab`의 재미있는 점은 서로 자주 같이 거론되지만 사실은 다른 문제인 세 가지를 한 흐름에서 분리해 보여 준다는 데 있다. duplicate request를 막는 idempotency key, 같은 JVM 안의 stock decrement 경쟁을 막는 `synchronized`, 읽기 비용을 줄이는 `@Cacheable`은 모두 inventory 시나리오 안에 있지만 서로 다른 역할을 맡는다. macOS + VSCode 통합 터미널에서 `make test`를 다시 돌리면 그 차이가 더 또렷해진다.

## 구현 순서 요약

- `problem/README.md`와 `docs/README.md`가 inventory 시나리오를 cache/idempotency/concurrency의 공통 문제로 잡는다.
- `CacheConcurrencyDemoService`가 write path와 read path를 다른 규칙으로 나눈다.
- `CacheConcurrencyController`가 reservation과 inventory 조회 endpoint를 만든다.
- `CacheConcurrencyApiTest`가 duplicate reservation과 최종 inventory를 같이 검증한다.

## Phase 1

### Session 1

- 당시 목표:
  - 세 문제를 왜 inventory 시나리오 하나로 묶는지 먼저 고정한다.
- 변경 단위:
  - `problem/README.md`
  - `docs/README.md`
  - `spring/README.md`
- 처음 가설:
  - 캐시와 동시성을 따로 떼면 실제 서비스에서 겹쳐 오는 실패 패턴을 설명하기 어렵다.
- 실제 진행:
  - inventory 조회, reservation, idempotency key, `synchronized` 기반 제어를 current scope로 정했다.
  - Redis-backed cache와 distributed lock은 다음 단계로 미뤘다.

CLI:

```bash
cp .env.example .env
make run
```

검증 신호:

- `spring/README.md`가 VSCode 통합 터미널 기준 명령을 고정했고, docs는 in-memory `CacheManager`와 `synchronized`를 의도적 단순화로 설명한다.

핵심 코드:

```java
@RequestMapping("/api/v1/inventory")
public class CacheConcurrencyController {
```

왜 이 코드가 중요했는가:

- 모든 논점이 inventory 아래에 모여 있기 때문에, 읽기 캐시와 reservation write가 같은 문제 공간에 속한다는 사실이 컨트롤러 경로에서부터 드러난다.

새로 배운 것:

- "관련 있는 문제들"을 한 시나리오에 묶어 두면 기술 선택의 역할 차이가 훨씬 또렷하게 보인다.

다음:

- write path와 read path에 서로 다른 규칙을 넣는다.

## Phase 2

### Session 1

- 당시 목표:
  - duplicate request, stock decrement 경쟁, cached read를 각기 다른 코드 경계로 나눈다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/cache/application/CacheConcurrencyDemoService.java`
  - `spring/src/main/java/com/webpong/study2/app/cache/api/CacheConcurrencyController.java`
- 처음 가설:
  - 같은 key로 들어온 예약 요청은 이전 결과를 그대로 돌려주고, 서로 다른 요청 사이의 경쟁은 `synchronized`로 막는 것이 baseline 설명에 가장 적합하다.
- 실제 진행:
  - `reserve()`는 idempotency map을 먼저 확인한 뒤 재고 차감을 진행한다.
  - inventory 조회는 `@Cacheable("inventory-status")`로 read path를 분리한다.

CLI:

```bash
make test
```

검증 신호:

- `2026-03-13` macOS + VSCode 통합 터미널 재실행에서 `make test`가 `BUILD SUCCESSFUL`로 끝났다.

핵심 코드:

```java
if (idempotency.containsKey(idempotencyKey)) {
  return idempotency.get(idempotencyKey);
}
```

왜 이 코드가 중요했는가:

- duplicate request 문제는 lock으로 풀지 않는다. 이미 처리한 요청의 결과를 식별해서 그대로 돌려주는 규칙이 먼저다.

새로 배운 것:

- idempotency는 "한 번만 실행"이 아니라 "같은 요청이면 같은 결과를 돌려준다"는 계약이다.

다음:

- 이 계약과 캐시 read path를 실제 응답에서 확인한다.

## Phase 3

### Session 1

- 당시 목표:
  - duplicate reservation이 한 번만 반영되고, inventory read path는 최종 수량을 보여 주는지 검증한다.
- 변경 단위:
  - `spring/src/test/java/com/webpong/study2/app/CacheConcurrencyApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`
- 처음 가설:
  - 같은 `Idempotency-Key`로 두 번 예약하고 마지막에 inventory를 조회하면 세 규칙의 역할 차이를 설명하기 충분하다.
- 실제 진행:
  - `reserve-1`로 두 번 reservation을 보내도 remaining이 둘 다 8인지 확인했다.
  - 마지막에 `/api/v1/inventory/SKU-1` 조회가 8을 반환하는지 확인했다.

CLI:

```bash
make test
make smoke
docker compose up --build
```

검증 신호:

- `2026-03-13` 재실행 뒤 XML 리포트 4개, `failures=0`이 확인됐다.
- `2026-03-09` 검증 기록에는 in-memory `CacheManager` 기반 test 통과와 lint/test/smoke/Compose health 확인이 남아 있다.

핵심 코드:

```java
mockMvc
    .perform(get("/api/v1/inventory/SKU-1"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.available").value(8));
```

왜 이 코드가 중요했는가:

- reservation의 중복 방지 결과가 결국 read path에서 어떻게 보이는지까지 이어져야 cache와 concurrency 이야기가 한 시나리오로 닫힌다.

새로 배운 것:

- 캐시와 동시성을 같이 다룬다고 해서 같은 도구를 쓰는 것은 아니다. read path, duplicate request, shared mutable state는 서로 다른 규칙을 요구한다.

다음:

- Redis-backed cache, distributed lock, idempotency persistence는 이후 단계에서 보강한다.
