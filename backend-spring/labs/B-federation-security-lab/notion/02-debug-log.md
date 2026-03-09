# Debug Log

## Current recorded issue

이 랩에서 가장 중요한 디버깅 포인트는 “security 기능 이름”과 “실제 구현 깊이”를 혼동하지 않게 만드는 것이다.

- failing command or request:
  - none recorded as a blocking runtime defect in the current pass
- exact symptom:
  - Google, TOTP, throttling 같은 단어가 들어가면 저장소가 실제 hardening을 모두 끝낸 것처럼 읽히기 쉽다
- first incorrect assumption:
  - 용어만 맞으면 scaffold도 충분히 오해 없이 읽힐 것이라고 생각하기 쉽다
- evidence collected:
  - docs는 Google integration이 mocked contract이고 throttling이 documented concern에 가깝다고 분명히 적는다

## Root cause

보안 랩은 특히 과장되기 쉽다. simulated flow와 real integration을 구분하지 않으면 학습 저장소가 reference implementation처럼 오해된다.

## Fix and verification

- code or config change made:
  - README와 notes에 simplification을 명시했다
- why that change addresses the cause:
  - 독자가 현재 scaffold가 보여 주는 범위와 남은 작업을 구분할 수 있다
- command, test, or log line that proved the fix:
  - `make lint`
  - `make test`

## Follow-up debt

- Redis-backed throttling enforcement와 persisted audit trail은 더 강화할 수 있다
- real provider callback validation은 후속 과제다

