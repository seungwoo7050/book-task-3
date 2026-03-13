# H-service-boundary-lab 시리즈 지도

이 시리즈는 단일 백엔드에서 처음으로 인증과 워크스페이스 도메인을 분리하는 순간을, gateway와 서비스 코드, system test를 기준으로 다시 읽습니다.

## 이 시리즈가 보는 문제

- `identity-service`와 `workspace-service`를 나눈 뒤에도 토큰 발급과 workspace 생성이 이어져야 합니다.
- 서비스가 서로의 DB를 읽지 않고 claims만으로 협력할 수 있어야 합니다.

## 실제 구현 표면

- `identity-service`의 `/api/v1/internal/auth/*`
- `workspace-service`의 `/api/v1/internal/workspaces`
- gateway의 request id 전파와 공통 health/metrics surface
- Compose 기반 system test

## 대표 검증 엔트리

- `python -m pytest tests/test_system.py -q`
- `make smoke`
- `docker compose up --build`

## 읽는 순서

1. [프로젝트 README](../../../labs/H-service-boundary-lab/README.md)
2. [문제 정의](../../../labs/H-service-boundary-lab/problem/README.md)
3. [실행 진입점](../../../labs/H-service-boundary-lab/fastapi/README.md)
4. [gateway README](../../../labs/H-service-boundary-lab/fastapi/gateway/README.md)
5. [identity-service README](../../../labs/H-service-boundary-lab/fastapi/services/identity-service/README.md)
6. [workspace-service README](../../../labs/H-service-boundary-lab/fastapi/services/workspace-service/README.md)
7. [대표 system test](../../../labs/H-service-boundary-lab/fastapi/tests/test_system.py)
8. [gateway main](../../../labs/H-service-boundary-lab/fastapi/gateway/app/main.py)
9. [gateway runtime](../../../labs/H-service-boundary-lab/fastapi/gateway/app/runtime.py)
10. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../labs/H-service-boundary-lab/README.md)
- [problem/README.md](../../../labs/H-service-boundary-lab/problem/README.md)
- [fastapi/README.md](../../../labs/H-service-boundary-lab/fastapi/README.md)
- [gateway/README.md](../../../labs/H-service-boundary-lab/fastapi/gateway/README.md)
- [services/identity-service/README.md](../../../labs/H-service-boundary-lab/fastapi/services/identity-service/README.md)
- [services/workspace-service/README.md](../../../labs/H-service-boundary-lab/fastapi/services/workspace-service/README.md)
- [tests/test_system.py](../../../labs/H-service-boundary-lab/fastapi/tests/test_system.py)
- [gateway/app/main.py](../../../labs/H-service-boundary-lab/fastapi/gateway/app/main.py)
- [gateway/app/runtime.py](../../../labs/H-service-boundary-lab/fastapi/gateway/app/runtime.py)
- [docs/verification-report.md](../../../docs/verification-report.md)
