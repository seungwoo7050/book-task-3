# K-distributed-ops-lab FastAPI

이 문서는 K-distributed-ops-lab의 실행과 검증 진입점입니다. 문제 정의나 설계 해설보다 먼저 손을 움직여 보고 싶을 때 여기서 시작합니다.

## 이 워크스페이스가 제공하는 답

- 서비스별 health / metrics endpoint
- gateway 포함 Compose health matrix
- request id가 포함된 JSON 로그
- AWS target shape 문서

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

- `gateway`: 호스트 `8014` 포트로 public API와 health/metrics surface를 노출합니다.
- `identity-service`: 호스트 `8131` 포트로 내부 인증 API를 노출합니다.
- `workspace-service`: 호스트 `8132` 포트로 내부 워크스페이스 API를 노출합니다.
- `notification-service`: 호스트 `8133` 포트로 consumer와 debug API를 노출합니다.
- `redis`: `6394` 포트로 stream과 pub/sub를 제공합니다.

## 실행 전에 알아둘 점

- 모든 서비스는 `/health/live`, `/health/ready`, `/ops/metrics` 기준으로 설명됩니다.
- gateway public health와 내부 서비스 ready는 서로 다른 질문에 답합니다.
- JSON 로그는 `service_name`, `request_id` 중심 최소 correlation을 제공합니다.
- AWS 문서는 target shape이며 실제 배포 완료 선언이 아닙니다.

## 역할이 다른 관련 문서

- 문제 요약과 답안 인덱스: [상위 README](../README.md)
- canonical problem statement: [problem/README.md](../problem/README.md)
- 설계 설명: [docs/README.md](../docs/README.md)
- 학습 로그: [notion/README.md](../notion/README.md)
