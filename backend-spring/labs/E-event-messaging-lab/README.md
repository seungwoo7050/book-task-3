# E-event-messaging-lab

request-response만으로 끝나지 않는 백엔드에서 이벤트 경계를 어떻게 설명할지 정리하는 랩입니다.

- 상태: `verified scaffold`
- 실행 진입점: [spring/README.md](spring/README.md)

## 문제 요약

- 도메인 변경 사실을 다른 처리 경로로 넘길 때, DB와 메시지 브로커 사이의 경계를 설명해야 합니다.
- 하지만 곧바로 거대한 분산 시스템으로 점프하지 않고, 작은 랩에서 outbox 사고방식을 보여줄 필요가 있습니다.
- 상세 성공 기준과 제약은 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- outbox table과 JPA entity를 두고, pending-to-published lifecycle을 보여주는 랩을 만들었습니다.
- order event 생성과 publish boundary를 분리해 "이벤트를 만든다"와 "브로커로 넘긴다"를 다른 문제로 다뤘습니다.
- Kafka/Redpanda가 등장하는 이유를 outbox handoff 관점에서 설명할 수 있게 했습니다.

## 핵심 설계 선택

- event sourcing보다 outbox를 먼저 다뤄 학습 곡선을 낮췄습니다.
- long-running worker보다 이벤트 경계와 persistence 사실을 먼저 고정했습니다.
- DLQ와 retry는 개념과 문서로 남기고, runtime 과시는 뒤로 미뤘습니다.

## 검증

```bash
cd spring
make lint
make test
make smoke
docker compose up --build
```

마지막 기록된 실제 검증 결과는 [../../docs/verification-report.md](../../docs/verification-report.md)에 있습니다.

## 이번 단계에서 일부러 남긴 것

- production-grade publisher worker
- real Kafka consumer contract 검증
- failure metadata와 replay policy의 심화

## 다음에 읽을 문서

- canonical problem statement: [problem/README.md](problem/README.md)
- 실행과 검증: [spring/README.md](spring/README.md)
- 현재 구현 범위와 단순화: [docs/README.md](docs/README.md)
- 학습 로그와 재현 기록: [notion/README.md](notion/README.md)
