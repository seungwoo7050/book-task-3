# workspace-backend-v2-msa

이 프로젝트는 capstone v2입니다. `workspace-backend` v1을 기준선으로 남겨 둔 채, 같은 협업형 도메인을 `gateway + identity-service + workspace-service + notification-service`로 다시 분해한 MSA 학습 버전입니다.

## 이 랩에서 배우는 것

- public API를 유지한 채 내부 서비스를 분리하는 방법
- bearer claims, outbox, Redis Streams, websocket fan-out을 서비스 경계로 재배치하는 방법
- 단일 백엔드 v1과 MSA v2를 같은 문제 정의 안에서 비교하는 방법

## 비교 포인트

| 항목 | v1 | v2 |
| --- | --- | --- |
| public API | 단일 FastAPI 앱 | gateway가 유지 |
| 인증 | 같은 프로세스 안에서 처리 | `identity-service` 분리 |
| 워크스페이스 도메인 | 같은 DB와 서비스 계층 | `workspace-service` 분리 |
| 알림 전달 | 앱 내부 큐 + websocket | outbox + stream + consumer + pub/sub |
| 운영성 | 단일 앱 기준 | 서비스별 health, metrics, request id |

## 실행 방법

1. [problem/README.md](problem/README.md)에서 왜 v2가 필요한지 읽습니다.
2. [fastapi/README.md](fastapi/README.md)에서 전체 스택을 실행합니다.
3. [docs/README.md](docs/README.md)와 [notion/README.md](notion/README.md)로 경계 선택과 비용을 복습합니다.

## 검증 방법

- `cd fastapi && make lint`
- `cd fastapi && make test`
- `cd fastapi && make smoke`
- `cd fastapi && docker compose up --build`

## 포트폴리오로 확장하려면

- 서비스 수를 늘리기보다 경계의 타당성과 새 복잡성을 먼저 설명합니다.
- Saga, retry policy, service discovery, trace backend는 후속 실험으로 분리하는 편이 좋습니다.
