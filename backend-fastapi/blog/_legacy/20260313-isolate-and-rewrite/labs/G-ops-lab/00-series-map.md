# G-ops-lab 시리즈 지도

이 시리즈는 기능 API보다 운영 surface를 먼저 드러내는 랩을, 실제 runtime 코드와 검증 경로 기준으로 다시 읽습니다.

## 이 시리즈가 보는 문제

- 단순한 백엔드라도 live/ready와 metrics를 분리해 설명할 수 있어야 합니다.
- 운영성은 거대한 observability stack보다, 지금 당장 무엇을 측정하고 무엇을 아직 측정하지 않는지 드러내는 문제여야 합니다.

## 실제 구현 표면

- `/api/v1/health/live`
- `/api/v1/ops/ready`
- `/api/v1/ops/metrics`
- request count 증가와 구조화 로그

## 대표 검증 엔트리

- `pytest tests/integration/test_ops.py -q`
- `make smoke`
- `docker compose up --build`

## 읽는 순서

1. [프로젝트 README](../../../labs/G-ops-lab/README.md)
2. [문제 정의](../../../labs/G-ops-lab/problem/README.md)
3. [실행 진입점](../../../labs/G-ops-lab/fastapi/README.md)
4. [대표 통합 테스트](../../../labs/G-ops-lab/fastapi/tests/integration/test_ops.py)
5. [핵심 구현 1](../../../labs/G-ops-lab/fastapi/app/main.py)
6. [핵심 구현 2](../../../labs/G-ops-lab/fastapi/app/api/v1/routes/ops.py)
7. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../labs/G-ops-lab/README.md)
- [problem/README.md](../../../labs/G-ops-lab/problem/README.md)
- [fastapi/README.md](../../../labs/G-ops-lab/fastapi/README.md)
- [tests/integration/test_ops.py](../../../labs/G-ops-lab/fastapi/tests/integration/test_ops.py)
- [app/main.py](../../../labs/G-ops-lab/fastapi/app/main.py)
- [app/api/v1/routes/ops.py](../../../labs/G-ops-lab/fastapi/app/api/v1/routes/ops.py)
- [docs/verification-report.md](../../../docs/verification-report.md)
