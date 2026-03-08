# Problem

간단한 로그 라인을 파싱하고 category별 요약을 만들며, race-safe recorder를 구현한다.

## Requirements

- `"category,duration_ms"` 형식의 라인을 파싱한다.
- category별 평균 지연 시간을 계산한다.
- concurrent append가 가능한 recorder를 만든다.
- benchmark와 subtest를 포함한다.

