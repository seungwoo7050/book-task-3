# References

## 1. Go Concurrency Patterns

- Title: Go Concurrency Patterns: Context
- URL: https://go.dev/blog/context
- Checked date: 2026-03-07
- Why: cancellation 전파 의미를 다시 고정했다.
- Learned: context는 값 보관함이 아니라 취소/시간 제한 전파 장치로 봐야 한다.
- Effect: pipeline과 worker pool 모두 context-aware 하게 유지했다.

## 2. Legacy Worker Pool Notes

- Title: legacy `worker-pool.md`
- Source workspace path (not included in this public repo): legacy/01-foundation/02-concurrency-patterns/docs/worker-pool.md
- Checked date: 2026-03-07
- Why: 기존 과제가 어떤 학습 포인트를 강조했는지 확인했다.
- Learned: 입문자는 처리량보다 “누가 goroutine을 닫는가”를 먼저 이해해야 한다.
- Effect: concepts 문서에서 종료 책임을 핵심 항목으로 남겼다.

