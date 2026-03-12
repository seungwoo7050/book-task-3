# E-event-messaging-lab Spring 워크스페이스

- 상태: `verified scaffold`
- 현재 범위: outbox persistence와 Kafka-oriented message flow

## 실행과 검증 명령

```bash
cp .env.example .env
make run
make lint
make test
make smoke
docker compose up --build
```

## 현재 한계

- long-running publisher worker는 아직 없다
- Kafka runtime guarantee는 개념 설명이 중심이다
