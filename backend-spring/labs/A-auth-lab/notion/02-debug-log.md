# Debug Log

## Current recorded issue

현재 기록된 가장 중요한 문제는 로직 버그라기보다 “scaffold를 실제로 검증 가능한 상태로 유지하는 것”이다.

- failing command or request:
  - documented run and validation commands
- exact symptom:
  - auth persistence와 mail lifecycle이 아직 얕기 때문에, README가 구현 범위를 과장하면 금방 모순이 생긴다
- first incorrect assumption:
  - scaffold라도 기능 이름만 있으면 충분히 설명될 것이라고 생각하기 쉽다
- evidence collected:
  - README와 docs는 현재 상태를 `verified scaffold`로 명시하고 next improvements를 분리한다

## Root cause

이 랩은 완성품이 아니라 구조 학습용 scaffold다. 구현된 것과 아직 모델 수준인 것을 구분하지 않으면 독자가 잘못된 기대를 갖게 된다.

## Fix and verification

- code or config change made:
  - tracked docs에서 범위와 known gaps를 명확히 나눴다
- why that change addresses the cause:
  - 검증 가능한 현재 상태와 미구현 영역이 섞이지 않는다
- command, test, or log line that proved the fix:
  - `make lint`
  - `make test`
  - `make smoke`

## Follow-up debt

- persisted verification/reset flow는 여전히 구현 보강이 필요하다
- actual response cookie assertions를 더 늘릴 수 있다

