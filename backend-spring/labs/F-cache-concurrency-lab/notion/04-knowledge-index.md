# Knowledge Index

## Reusable concepts

- Idempotency key:
  - 같은 write 요청의 중복 처리를 막는 식별자다.
- Cacheable read path:
  - 자주 조회되는 값을 캐시에 저장해 응답 비용을 줄이는 패턴이다.
- Reservation concurrency:
  - 한정된 재고나 자원을 동시에 잡으려는 요청 충돌 문제다.

## Glossary

- invalidation:
  - 캐시에 저장된 값을 더 이상 신뢰하지 않도록 비우거나 갱신하는 과정이다.
- distributed lock:
  - 여러 프로세스/인스턴스 사이에서 동시에 같은 자원을 수정하지 못하게 하는 잠금이다.

## References

- title:
  - F-cache-concurrency-lab Notes README
  - URL or local path: `/Users/woopinbell/work/web-pong/study2/labs/F-cache-concurrency-lab/docs/README.md`
  - checked date: `2026-03-09`
  - why it was consulted: simplification과 next step을 맞추기 위해 확인했다
  - what was learned: test는 in-memory cache, distributed lock은 future step이다
  - what changed: 디버그 로그에서 label과 implementation depth 간극을 핵심 이슈로 적었다

