# F-cache-concurrency-lab 시리즈 지도

`F-cache-concurrency-lab`은 캐시, 멱등성, 동시성을 각각 따로 설명하지 않고 inventory 시나리오 하나에 묶어 보여 준다. macOS + VSCode 통합 터미널에서 `make test`를 다시 돌려 보면, 이 랩의 핵심은 Redis나 분산 락을 과시하는 데 있지 않고 read path, duplicate request, stock decrement 경쟁을 어떤 순서로 다루는지 보여 주는 데 있다는 점이 드러난다.

## 이 프로젝트가 푸는 문제

- inventory 조회에 cacheable read path를 둔다.
- reservation write path에 idempotency key를 넣는다.
- 같은 JVM 안에서는 `synchronized`로 재고 차감 경쟁을 먼저 제어한다.

## 이 시리즈의 근거

- `problem/README.md`
- `docs/README.md`
- `spring/README.md`
- `CacheConcurrencyDemoService`, `CacheConcurrencyController`
- `CacheConcurrencyApiTest`
- `2026-03-13` `make test` 재실행, `2026-03-09` 검증 보고

## 읽는 순서

1. `10-development-timeline.md`
2. `_evidence-ledger.md`
3. `_structure-outline.md`

## 시리즈의 중심 질문

- idempotency와 lock은 어떻게 다른 실패를 막는가
- cache는 왜 read path에만 들어가야 하는가
- Redis와 distributed lock은 어디서부터 이어 붙이면 되는가
