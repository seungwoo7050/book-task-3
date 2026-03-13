# workspace-backend 시리즈 지도

이 시리즈는 A~G 랩에서 따로 읽었던 인증, 인가, 데이터, 비동기, 실시간, 운영성을 단일 FastAPI 제품형 구조로 다시 합치는 과정을 source-first로 다시 읽습니다.

## 이 시리즈가 보는 문제

- 로컬 로그인과 Google 스타일 로그인이 같은 사용자 모델 안에서 함께 설명되어야 합니다.
- workspace, project, task, comment, notification, websocket이 한 서비스 안에서 어떻게 연결되는지 보여 줄 기준선이 필요합니다.

## 실제 구현 표면

- `/api/v1/auth/*`, `/api/v1/platform/*`
- workspace invite와 accept
- project, task, comment 생성
- `/api/v1/platform/notifications/drain`
- `/api/v1/platform/ws/notifications`

## 대표 검증 엔트리

- `pytest tests/integration/test_capstone.py -q`
- `make smoke`
- `docker compose up --build`

## 읽는 순서

1. [프로젝트 README](../../../capstone/workspace-backend/README.md)
2. [문제 정의](../../../capstone/workspace-backend/problem/README.md)
3. [실행 진입점](../../../capstone/workspace-backend/fastapi/README.md)
4. [대표 통합 테스트](../../../capstone/workspace-backend/fastapi/tests/integration/test_capstone.py)
5. [플랫폼 서비스](../../../capstone/workspace-backend/fastapi/app/domain/services/platform.py)
6. [platform route](../../../capstone/workspace-backend/fastapi/app/api/v1/routes/platform.py)
7. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../capstone/workspace-backend/README.md)
- [problem/README.md](../../../capstone/workspace-backend/problem/README.md)
- [fastapi/README.md](../../../capstone/workspace-backend/fastapi/README.md)
- [tests/integration/test_capstone.py](../../../capstone/workspace-backend/fastapi/tests/integration/test_capstone.py)
- [app/domain/services/platform.py](../../../capstone/workspace-backend/fastapi/app/domain/services/platform.py)
- [app/api/v1/routes/platform.py](../../../capstone/workspace-backend/fastapi/app/api/v1/routes/platform.py)
- [docs/verification-report.md](../../../docs/verification-report.md)
