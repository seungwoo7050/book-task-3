# F-cache-concurrency-lab — Notion 문서 가이드

이 디렉토리는 Cache & Concurrency Lab의 학습 과정을 기록한 문서들을 담고 있다.

## 문서 구성

| 순서 | 파일 | 내용 |
|------|------|------|
| 0 | [00-problem-framing.md](./00-problem-framing.md) | 왜 캐시와 동시성을 하나의 시나리오로 묶었는지, 범위와 제약 조건 |
| 1 | [01-approach-log.md](./01-approach-log.md) | 세 가지 설계 방향 비교, inventory 시나리오 선택 근거 |
| 2 | [02-debug-log.md](./02-debug-log.md) | @Cacheable이 실제로 증명하는 것 vs 증명하지 못하는 것 |
| 3 | [03-retrospective.md](./03-retrospective.md) | 잘한 것(시나리오 통합), 약한 것(Redis 미사용, 분산 락 미구현), 개선 방향 |
| 4 | [04-knowledge-index.md](./04-knowledge-index.md) | Idempotency Key, @Cacheable, synchronized, 캐시 무효화, 분산 락 개념 정리 |
| 5 | [05-timeline.md](./05-timeline.md) | Docker Compose, Makefile, 테스트 실행 등 소스코드에 없는 작업 기록 |

## 읽는 순서

처음이라면 **00 → 01 → 03** 순서로 읽으면 "왜 이렇게 만들었고, 무엇이 부족한지"를 빠르게 파악할 수 있다.

특정 개념이 궁금하면 **04-knowledge-index.md**에서 Idempotency Key, @Cacheable, synchronized, 캐시 무효화, 분산 락의 정의와 코드 예시를 확인한다.

## 이 랩의 핵심 포인트

- **재고 시나리오 하나로 세 문제(캐시, 동시성, 멱등성)를 통합**했다
- **in-memory 구현**(ConcurrentMapCacheManager + synchronized)으로 개념을 먼저 보여주고, Redis + Redisson은 다음 단계로 남겼다
- **키워드 인플레이션 주의**: "Cache Lab"이라는 이름이 Redis 경험을 의미하지 않음을 인지해야 한다

## 관련 문서

- [docs/README.md](../docs/README.md) — 기술 검증 범위와 simplification 목록
- [problem/README.md](../problem/README.md) — 랩 출제 의도
