# Debug Log

## Current recorded issue

이 랩의 가장 중요한 문제는 운영 키워드가 실제 검증 범위보다 커 보이는 것이다.

- failing command or request:
  - none recorded as a blocking runtime defect in the current pass
- exact symptom:
  - metrics, logs, AWS docs가 있으면 live deployment나 alerting까지 끝난 것처럼 읽히기 쉽다
- first incorrect assumption:
  - observability surface만 있으면 운영 역량이 충분히 증명된다고 생각하기 쉽다
- evidence collected:
  - docs는 alert rules, external log shipping, IaC가 아직 없다고 적는다

## Root cause

ops lab은 특히 이름이 강하다. 실제로 검증된 것은 health, logging shape, metrics exposure, CI wiring이고, 그 이상은 아니다.

## Fix and verification

- code or config change made:
  - tracked docs에서 current implementation과 next improvements를 구분했다
- why that change addresses the cause:
  - 현재 증명된 범위만 읽히게 된다
- command, test, or log line that proved the fix:
  - `make lint`
  - `make test`
  - `make smoke`

## Follow-up debt

- `/actuator/prometheus` smoke check를 더 명시적으로 넣을 수 있다
- IaC와 dashboard 예시를 추가할 수 있다

