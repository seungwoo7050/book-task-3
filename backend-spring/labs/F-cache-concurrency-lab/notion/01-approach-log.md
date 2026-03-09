# Approach Log

## Options considered

- cache와 concurrency를 분리하는 방식은 각각 더 선명하지만, inventory 시나리오의 결합을 보기 어렵다.
- Redis real cache assertion까지 첫 scaffold에 넣는 방식은 현실적이지만 무겁다.
- in-process synchronization은 한계가 있지만 기본 경쟁 문제를 설명하기 쉽다.

## Chosen direction

- package structure:
  - inventory lookup, reservation, idempotency 중심
- persistence choice:
  - cache와 idempotency persistence를 초기에는 단순하게 둔다
- security boundary:
  - auth보다 duplicate request와 concurrent update에 집중한다
- integration style:
  - test는 in-memory CacheManager, docs는 Redis/Redisson next step
- why this is the right choice:
  - junior 수준에서 cache invalidation과 duplicate protection을 같이 말하기 좋다

## Rejected ideas

- distributed lock full implementation을 scaffold 필수로 두는 방식은 폐기했다
- cache를 completely omitted하는 방식은 폐기했다. lab identity가 약해진다

## Evidence

- `/Users/woopinbell/work/web-pong/study2/labs/F-cache-concurrency-lab/spring/README.md`
- `/Users/woopinbell/work/web-pong/study2/labs/F-cache-concurrency-lab/docs/README.md`

