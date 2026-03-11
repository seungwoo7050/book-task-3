# I-event-integration-lab

동기 API 경계를 서비스 간 이벤트 통합으로 확장하는 랩입니다. `workspace-service`의 outbox와 `notification-service`의 idempotent consumer를 붙여 eventual consistency를 설명하는 데 집중합니다.

## 문제 요약

- 동기 API와 비동기 알림 전달을 서비스 간 통합으로 확장한다. 댓글 저장과 알림 생성이 같은 시점에 끝나지 않아도 되는 구조를 설명하는 것이 목표다.
- 댓글 생성이 outbox에 기록된다.
- relay 후 `notification-service`가 stream을 consume한다.
- 상세 성공 기준과 제외 범위는 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- workspace outbox 적재
- Redis Streams relay
- notification consume와 dedupe

## 핵심 설계 선택

- outbox handoff를 서비스 경계로 옮기는 방법
- Redis Streams 기반 이벤트 전달
- idempotent consumer와 중복 흡수
- consumer group 대신 단순 consumer 흐름으로 제한합니다.
- dead-letter queue와 재처리 UI는 범위 밖입니다.

## 검증

```bash
make lint
make test
make smoke
docker compose up --build
```

- 실행과 환경 설명은 [fastapi/README.md](fastapi/README.md)에서 다룹니다.
- 마지막 기록된 실제 검증 결과는 [../../docs/verification-report.md](../../docs/verification-report.md)에 있습니다.

## 제외 범위

- consumer group
- dead-letter queue
- replay UI

## 다음 랩 또는 비교 대상

- 다음 단계는 [J-edge-gateway-lab](../J-edge-gateway-lab/README.md)입니다.
- 설계 설명은 [docs/README.md](docs/README.md), 학습 로그는 [notion/README.md](notion/README.md), 실행 진입점은 [fastapi/README.md](fastapi/README.md)에서 읽습니다.
