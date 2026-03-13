# workspace-backend-v2-msa 시리즈 지도

이 시리즈는 `workspace-backend` 기준선을 유지한 채, 같은 협업형 도메인을 `gateway + identity-service + workspace-service + notification-service`로 다시 나눈 capstone을 source-first로 다시 읽습니다.

## 이 시리즈가 보는 문제

- public `/api/v1/auth/*`, `/api/v1/platform/*` shape를 유지하면서 내부 서비스 경계를 분리할 수 있는가
- 댓글 생성 성공과 notification delivery 성공을 분리해도, 복구 후 websocket 알림까지 다시 이어 붙일 수 있는가

## 실제 구현 표면

- gateway의 public auth / platform route와 websocket edge
- `identity-service`, `workspace-service`, `notification-service`의 DB ownership
- `comment.created.v1` 이벤트 계약과 Redis Streams relay
- notification-service 장애 후 recovery drain 시나리오

## 대표 검증 엔트리

- `python -m pytest tests/test_system.py -q`
- `make smoke`
- `docker compose up --build`

## 읽는 순서

1. [프로젝트 README](../../../capstone/workspace-backend-v2-msa/README.md)
2. [문제 정의](../../../capstone/workspace-backend-v2-msa/problem/README.md)
3. [실행 진입점](../../../capstone/workspace-backend-v2-msa/fastapi/README.md)
4. [gateway README](../../../capstone/workspace-backend-v2-msa/fastapi/gateway/README.md)
5. [계약 문서](../../../capstone/workspace-backend-v2-msa/fastapi/contracts/README.md)
6. [대표 system test](../../../capstone/workspace-backend-v2-msa/fastapi/tests/test_system.py)
7. [workspace-service route](../../../capstone/workspace-backend-v2-msa/fastapi/services/workspace-service/app/api/v1/routes/platform.py)
8. [notification-service route](../../../capstone/workspace-backend-v2-msa/fastapi/services/notification-service/app/api/v1/routes/notifications.py)
9. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../capstone/workspace-backend-v2-msa/README.md)
- [problem/README.md](../../../capstone/workspace-backend-v2-msa/problem/README.md)
- [fastapi/README.md](../../../capstone/workspace-backend-v2-msa/fastapi/README.md)
- [gateway/README.md](../../../capstone/workspace-backend-v2-msa/fastapi/gateway/README.md)
- [contracts/README.md](../../../capstone/workspace-backend-v2-msa/fastapi/contracts/README.md)
- [tests/test_system.py](../../../capstone/workspace-backend-v2-msa/fastapi/tests/test_system.py)
- [services/workspace-service/app/api/v1/routes/platform.py](../../../capstone/workspace-backend-v2-msa/fastapi/services/workspace-service/app/api/v1/routes/platform.py)
- [services/notification-service/app/api/v1/routes/notifications.py](../../../capstone/workspace-backend-v2-msa/fastapi/services/notification-service/app/api/v1/routes/notifications.py)
- [docs/verification-report.md](../../../docs/verification-report.md)
