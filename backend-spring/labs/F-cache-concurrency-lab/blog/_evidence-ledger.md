# F-cache-concurrency-lab evidence ledger

- 복원 방식: 세부 작업 로그 대신 `Phase 1 -> Phase 3`로 다시 구성했다.
- 근거: `README.md`, `problem/README.md`, `docs/README.md`, `spring/Makefile`, `CacheConcurrencyDemoService.java`, `CacheConfig.java`, `CacheConcurrencyApiTest.java`, `spring/build/test-results/test/*.xml`, `../../docs/verification-report.md`
- 작업 환경 전제: macOS + VSCode 통합 터미널 기준.

## Phase 1

- 당시 목표: cache, idempotency, inventory 경쟁을 하나의 시나리오로 묶는다.
- 변경 단위: `README.md`, `problem/README.md`, `CacheConcurrencyApiTest.java`
- 처음 가설: Redis나 distributed lock을 먼저 넣어야 concurrency 랩이 설득력을 가질 것 같았다.
- 실제 조치: 같은 `Idempotency-Key`로 reservation을 두 번 보내도 같은 결과가 나오는 흐름을 먼저 테스트로 고정했다.
- CLI:

```bash
cd spring
make test
```

- 검증 신호: `CacheConcurrencyApiTest` 1개 테스트 통과, `HealthApiTest` 2개 테스트 통과
- 핵심 코드 앵커: `CacheConcurrencyApiTest.idempotentReservationReturnsSameResult()`
- 새로 배운 것: cache와 concurrency는 실제 서비스에서 한 시나리오 안에 겹친다.
- 다음: `synchronized`, idempotency map, `@Cacheable`을 서비스 코드에 연결한다.

## Phase 2

- 당시 목표: 분산 락 없이도 baseline concurrency 경계를 드러낸다.
- 변경 단위: `CacheConcurrencyDemoService.java`, `CacheConfig.java`
- 처음 가설: in-memory 구현은 너무 약해 보일 수 있다고 생각했다.
- 실제 조치: `reserve()`를 `synchronized`로 보호하고, 같은 idempotency key면 이전 결과를 재사용하게 만들었다. 조회 경로는 `@Cacheable`과 `ConcurrentMapCacheManager`로 묶었다.
- CLI:

```bash
cd spring
make smoke
docker compose up --build
```

- 검증 신호: `LabInfoApiSmokeTest` 1개 테스트 통과, `2026-03-09` 검증 보고서 기준 in-memory `CacheManager`로 test 통과
- 핵심 코드 앵커: `CacheConcurrencyDemoService.reserve()`, `inventoryStatus()`, `CacheConfig.cacheManager()`
- 새로 배운 것: baseline concurrency의 핵심은 분산 도구 이름보다 재고 차감 규칙과 재시도 규칙을 먼저 고정하는 일이다.
- 다음: Redis, distributed lock, idempotency persistence 분리는 다음 단계로 남긴다.

## Phase 3

- 당시 목표: 현재 랩이 baseline이라는 점과 다음 확장 포인트를 분명히 남긴다.
- 변경 단위: `docs/README.md`, `spring/README.md`, `TEST-com.webpong.study2.app.CacheConcurrencyApiTest.xml`
- 처음 가설: `synchronized` 하나만 보이면 이후 확장도 자연스럽게 읽힐 줄 알았다.
- 실제 조치: real Redis assertion, distributed lock, idempotency persistence 분리를 docs에 다음 단계로 명시했다.
- CLI:

```bash
cd spring
make lint
make test
make smoke
```

- 검증 신호: `2026-03-13` 기준 4개 suite, 총 5개 테스트, 실패 0
- 핵심 코드 앵커: `docs/README.md`의 의도적 단순화, `verification-report.md`
- 새로 배운 것: 분산 도구를 빨리 붙이는 것보다 baseline 규칙을 먼저 고정하는 편이 비교와 설명에 유리하다.
- 다음: 운영성은 `G-ops-observability-lab`에서 따로 다룬다.
