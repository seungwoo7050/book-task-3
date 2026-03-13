# I-event-integration-lab 시리즈 지도

이 시리즈는 서비스 분리 이후의 첫 비동기 경계, 즉 `workspace-service` outbox와 `notification-service` consumer를 실제 코드 기준으로 다시 읽습니다.

## 이 시리즈가 보는 문제

- 댓글 저장과 알림 생성이 같은 성공으로 묶이지 않아도 되는지 설명할 수 있어야 합니다.
- relay와 consume가 분리되어도 중복 알림을 막을 수 있어야 합니다.

## 실제 구현 표면

- `workspace-service`의 `/api/v1/internal/*`
- `/api/v1/internal/events/relay`
- `/api/v1/internal/debug/outbox/pending`
- `notification-service`의 `/api/v1/internal/notifications/consume`

## 대표 검증 엔트리

- `python -m pytest tests/test_system.py -q`
- `make smoke`
- `docker compose up --build`

## 읽는 순서

1. [프로젝트 README](../../../labs/I-event-integration-lab/README.md)
2. [문제 정의](../../../labs/I-event-integration-lab/problem/README.md)
3. [실행 진입점](../../../labs/I-event-integration-lab/fastapi/README.md)
4. [workspace-service README](../../../labs/I-event-integration-lab/fastapi/services/workspace-service/README.md)
5. [notification-service README](../../../labs/I-event-integration-lab/fastapi/services/notification-service/README.md)
6. [대표 system test](../../../labs/I-event-integration-lab/fastapi/tests/test_system.py)
7. [workspace-service route](../../../labs/I-event-integration-lab/fastapi/services/workspace-service/app/api/v1/routes/platform.py)
8. [notification-service route](../../../labs/I-event-integration-lab/fastapi/services/notification-service/app/api/v1/routes/notifications.py)
9. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../labs/I-event-integration-lab/README.md)
- [problem/README.md](../../../labs/I-event-integration-lab/problem/README.md)
- [fastapi/README.md](../../../labs/I-event-integration-lab/fastapi/README.md)
- [services/workspace-service/README.md](../../../labs/I-event-integration-lab/fastapi/services/workspace-service/README.md)
- [services/notification-service/README.md](../../../labs/I-event-integration-lab/fastapi/services/notification-service/README.md)
- [tests/test_system.py](../../../labs/I-event-integration-lab/fastapi/tests/test_system.py)
- [services/workspace-service/app/api/v1/routes/platform.py](../../../labs/I-event-integration-lab/fastapi/services/workspace-service/app/api/v1/routes/platform.py)
- [services/notification-service/app/api/v1/routes/notifications.py](../../../labs/I-event-integration-lab/fastapi/services/notification-service/app/api/v1/routes/notifications.py)
- [docs/verification-report.md](../../../docs/verification-report.md)
