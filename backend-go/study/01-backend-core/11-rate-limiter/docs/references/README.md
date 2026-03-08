# References

## 1. Legacy Token Bucket Notes

- Title: legacy `token-bucket.md`
- Source workspace path (not included in this public repo): legacy/01-foundation/03-rate-limiter/docs/token-bucket.md
- Checked date: 2026-03-07
- Why: token bucket 설명과 이 과제의 의도를 다시 확인했다.
- Learned: 이 과제의 핵심은 알고리즘 자체보다 thread-safe 구현과 HTTP 통합이다.
- Effect: docs에서 middleware와 cleanup을 같은 비중으로 다뤘다.

## 2. Go Time Package

- Title: Package time
- URL: https://pkg.go.dev/time
- Checked date: 2026-03-07
- Why: refill 계산에서 시간 처리 패턴을 다시 확인했다.
- Learned: rate limit 예제는 time abstraction을 고민하기 좋은 출발점이다.
- Effect: limiter 테스트가 시간 흐름을 전제로 읽히도록 유지했다.

