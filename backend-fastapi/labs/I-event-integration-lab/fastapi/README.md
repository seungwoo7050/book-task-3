# I-event-integration-lab FastAPI

이 문서는 I-event-integration-lab의 실행과 검증 진입점입니다. 문제 정의나 설계 해설보다 먼저 손을 움직여 보고 싶을 때 여기서 시작합니다.

## 이 워크스페이스가 제공하는 답

- `workspace-service`의 outbox 적재와 relay
- Redis Streams 기반 `notification-service` consume
- 알림 중복 방지와 debug 조회

## 빠른 실행

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

## 런타임 구성

- `workspace-service`: 호스트 `8012`
- `notification-service`: 호스트 `8112`
- `redis`: 호스트 `6392`

## 실행 전에 알아둘 점


## 역할이 다른 관련 문서

- 문제 요약과 답안 인덱스: [상위 README](../README.md)
- canonical problem statement: [problem/README.md](../problem/README.md)
- 설계 설명: [docs/README.md](../docs/README.md)
- 학습 로그: [notion/README.md](../notion/README.md)
