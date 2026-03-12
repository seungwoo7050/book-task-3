# F-cache-concurrency-lab 학습 노트 가이드

이 폴더는 캐시, 동시성, 멱등성을 하나의 inventory 시나리오로 묶은 과정을 기록한 공개 학습 노트 세트다.

## 먼저 읽을 문서

1. [00-problem-framing.md](00-problem-framing.md): 왜 세 문제를 하나의 랩으로 묶었는지
2. [05-development-timeline.md](05-development-timeline.md): Compose, 캐시, 테스트를 어떤 순서로 쌓았는지
3. [01-approach-log.md](01-approach-log.md): in-memory baseline을 먼저 택한 이유

## 목적별 읽기

- `@Cacheable`이 실제로 무엇을 증명하는지 보려면 [02-debug-log.md](02-debug-log.md)
- idempotency key, cache invalidation, distributed lock 개념을 복습하려면 [04-knowledge-index.md](04-knowledge-index.md)
- 현재 약점과 다음 확장을 보려면 [03-retrospective.md](03-retrospective.md)

## 문서 목록

- `00-problem-framing.md`: 문제 정의와 성공 기준
- `01-approach-log.md`: 설계 선택지와 최종 결정
- `02-debug-log.md`: 실패와 수정 근거
- `03-retrospective.md`: 강점, 약점, 다음 단계
- `04-knowledge-index.md`: 재사용 개념과 용어
- `05-development-timeline.md`: 재현 가능한 개발 순서 기록
