# References

## 1. Go Testing Package

- Title: Package testing
- URL: https://pkg.go.dev/testing
- Checked date: 2026-03-07
- Why: benchmark와 subtest 작성 규칙을 다시 확인했다.
- Learned: benchmark는 일반 테스트와 구조가 거의 같아서 입문자도 빠르게 도입할 수 있다.
- Effect: `BenchmarkSummarize`와 subtest 기반 파서 검증을 같이 넣었다.

## 2. Go Data Race Detector

- Title: Data Race Detector
- URL: https://go.dev/doc/articles/race_detector
- Checked date: 2026-03-07
- Why: recorder 설계가 race detector 기준으로 안전한지 확인했다.
- Learned: 락 범위가 작아도 snapshot 복사를 빠뜨리면 경쟁 상태가 남는다.
- Effect: `Snapshot()`에서 복사본을 반환하도록 했다.

