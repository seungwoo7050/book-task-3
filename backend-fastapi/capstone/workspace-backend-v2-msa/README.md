# workspace-backend-v2-msa

이 프로젝트는 capstone v2입니다. `workspace-backend` v1을 기준선으로 남겨 둔 채, 같은 협업형 도메인을 `gateway + identity-service + workspace-service + notification-service`로 다시 분해한 MSA 학습 버전입니다.

## 문제 요약

- `workspace-backend` v1은 인증, 워크스페이스 도메인, 알림 전달을 한 프로세스 안에서 통합했다. v2의 목표는 같은 협업형 도메인을 MSA로 다시 분해해, public API를 유지한 채 내부 경계와 분산 복잡성이 어떻게 바뀌는지 설명 가능한 상태로 만드는 것이다.
- `gateway`가 public `/api/v1/auth/*`, `/api/v1/platform/*` 경로를 유지해야 한다.
- `identity-service`, `workspace-service`, `notification-service`는 각자 자기 DB만 읽어야 한다.
- 상세 성공 기준과 제외 범위는 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- public `/api/v1/auth/*`, `/api/v1/platform/*` route shape는 gateway가 유지합니다.
- `identity-service`, `workspace-service`, `notification-service`가 각자 자기 DB를 소유하도록 분리했습니다.
- 댓글 생성 뒤에는 outbox, Redis Streams consumer, websocket fan-out으로 이어지는 비동기 전달 경로를 구성했습니다.
- v1과 v2의 차이를 문서와 노트만 읽고도 비교할 수 있도록 비교 학습 구조를 유지했습니다.

## 핵심 설계 선택

- 브라우저 쿠키와 CSRF는 gateway에만 두고 내부 서비스는 bearer claims만 읽도록 경계를 나눴습니다.
- 서비스별 DB ownership을 지키고 사용자 정보는 claims와 event payload로만 전달합니다.
- notification-service 장애가 댓글 생성 성공을 막지 않도록 eventual consistency를 전제로 설계했습니다.

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

- Kubernetes, service mesh, service discovery
- 실제 클라우드 배포 자동화와 IaC
- front-end 렌더링과 정적 자산
- saga orchestration과 다단계 보상 흐름

## 다음 랩 또는 비교 대상

- 비교 기준선은 [workspace-backend](../workspace-backend/README.md)입니다.
- 심화 랩의 분해 이유를 다시 보려면 [H-service-boundary-lab](../../labs/H-service-boundary-lab/README.md)부터 [K-distributed-ops-lab](../../labs/K-distributed-ops-lab/README.md)까지를 함께 읽습니다.
- 설계 설명은 [docs/README.md](docs/README.md), 학습 로그는 [notion/README.md](notion/README.md), 실행 진입점은 [fastapi/README.md](fastapi/README.md)에서 읽습니다.
