# workspace-backend-v2-msa FastAPI

## 이 구현이 다루는 범위

- `gateway + identity-service + workspace-service + notification-service` 오케스트레이션
- public API는 gateway가 유지하고 내부 서비스는 `/internal/*`로 분리
- `workspace-service` outbox, Redis Streams consumer, Redis pub/sub 기반 websocket fan-out
- 서비스별 `/api/v1/health/live`, `/api/v1/health/ready`, `/api/v1/ops/metrics`

## 빠른 시작

가장 빠른 로컬 확인:

```bash
cp .env.example .env
docker compose up --build
```

개별 서비스 테스트:

```bash
make install
make test
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

- `gateway`: 호스트 `8015` 포트로 public API와 websocket을 노출합니다.
- `identity-service`: 호스트 `8115` 포트로 내부 인증 API를 노출합니다.
- `workspace-service`: 호스트 `8116` 포트로 내부 워크스페이스 API를 노출합니다.
- `notification-service`: 호스트 `8117` 포트로 consumer와 debug API를 노출합니다.
- `redis`: `6395` 포트로 Streams와 pub/sub를 제공합니다.

## 이 워크스페이스에서 확인할 점

- 브라우저 쿠키와 CSRF는 gateway만 처리합니다.
- 내부 서비스는 bearer claims만 사용하고 서로의 DB를 직접 읽지 않습니다.
- 댓글 생성은 notification-service 장애와 분리되어 성공해야 합니다.
- public route shape는 v1을 최대한 유지하고 내부 계약만 달라집니다.

## 함께 읽을 문서

- [상위 README](../README.md)
- [문제 정의](../problem/README.md)
- [문서 지도](../docs/README.md)
- [이벤트 계약](contracts/README.md)
