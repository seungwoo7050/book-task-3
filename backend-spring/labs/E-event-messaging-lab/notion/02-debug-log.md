# Debug Log

## Current recorded issue

이 랩의 핵심 문제는 runtime crash보다 “Kafka를 쓴다”는 표현이 실제 구현보다 더 크게 들리는 것이다.

- failing command or request:
  - none recorded as a blocking defect in the current pass
- exact symptom:
  - outbox와 topic naming만 있어도 fully event-driven system처럼 보일 수 있다
- first incorrect assumption:
  - broker가 Compose에 있으면 consumer reliability까지 충분히 설명된다고 생각하기 쉽다
- evidence collected:
  - docs는 long-running publisher와 DLQ/retry가 아직 conceptual이라고 적는다

## Root cause

messaging 랩은 keyword가 강해서 과장되기 쉽다. durable outbox와 real consumer contract 사이의 거리를 분명히 적어야 한다.

## Fix and verification

- code or config change made:
  - tracked docs에서 현재 구현과 다음 개선점을 분리했다
- why that change addresses the cause:
  - 독자가 scaffold를 production messaging example로 오해하지 않는다
- command, test, or log line that proved the fix:
  - `make test`
  - `docker compose up --build`

## Follow-up debt

- scheduled publisher와 real consume test를 붙여야 한다
- delivery failure metadata 저장이 필요하다

