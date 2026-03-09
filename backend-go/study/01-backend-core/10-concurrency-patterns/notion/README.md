# 10 — Concurrency Patterns notion/

이 폴더는 `10-concurrency-patterns` 프로젝트의 개발 과정과 학습 기록을 담은 블로그형 에세이 모음이다.

## 문서 가이드

| 파일 | 목적 | 언제 읽을까 |
|------|------|------------|
| [00-problem-framing.md](00-problem-framing.md) | 왜 이 프로젝트가 필요했는지 | 프로젝트를 처음 접할 때 |
| [01-approach-log.md](01-approach-log.md) | 어떻게 접근하고 구현했는지 | 구현 흐름을 따라가고 싶을 때 |
| [02-debug-log.md](02-debug-log.md) | 어떤 문제를 만났고 어떻게 해결했는지 | 비슷한 오류를 만났을 때 |
| [03-retrospective.md](03-retrospective.md) | 완성 후 돌아본 판단과 교훈 | 설계 결정의 이유가 궁금할 때 |
| [04-knowledge-index.md](04-knowledge-index.md) | 핵심 개념 정리 | 용어나 패턴을 빠르게 찾고 싶을 때 |
| [05-timeline.md](05-timeline.md) | CLI 명령어 포함 전체 개발 순서 | 프로젝트를 처음부터 재현하고 싶을 때 |

## 프로젝트 맥락

- **이전**: 09-cache-migrations-observability — 캐시, 메트릭, trace ID
- **현재**: 10-concurrency-patterns — Worker Pool, Pipeline, FanOut, context cancellation
- **다음**: 11-rate-limiter — 속도 제한기 구현
