# I-event-integration-lab FastAPI

## 이 구현이 다루는 범위

- `workspace-service`의 outbox 적재와 relay
- Redis Streams 기반 `notification-service` consume
- 알림 중복 방지와 debug 조회

## 빠른 시작

```bash
cp .env.example .env
docker compose up --build
```

## 검증 명령

```bash
make install
make lint
make test
make smoke
docker compose up --build
```

## Compose 구성

- `workspace-service`: 호스트 `8012`
- `notification-service`: 호스트 `8112`
- `redis`: 호스트 `6392`

## 함께 읽을 문서

- [상위 README](../README.md)
- [문제 정의](../problem/README.md)
- [문서 지도](../docs/README.md)
