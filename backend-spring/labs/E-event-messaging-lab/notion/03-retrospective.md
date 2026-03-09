# Retrospective

## What improved

- outbox를 먼저 배우는 방향이 맞았다.
- Kafka를 기술 이름이 아니라 handoff boundary 관점으로 설명할 수 있게 되었다.
- Compose에 Redpanda를 두니 로컬 실험 그림이 분명해졌다.

## What is still weak

- long-running publisher가 없다.
- DLQ와 retry policy는 아직 개념 수준이다.
- consumer contract 검증이 약하다.

## What to revisit

- scheduled publisher job을 실제로 추가할 수 있다.
- Kafka consumer integration test를 더 강하게 붙일 수 있다.
- capstone의 order-paid flow와 비교 노트를 만들 수 있다.

