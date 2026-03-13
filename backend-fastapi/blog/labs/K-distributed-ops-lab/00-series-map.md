# K-distributed-ops-lab 시리즈 지도

이 시리즈는 여러 서비스가 떠 있는 것만으로 끝내지 않고, health, metrics, request id, recovery 시나리오를 어떻게 함께 설명하는지 source-first로 다시 읽습니다.

## 이 시리즈가 보는 문제

- gateway와 내부 서비스가 각자 live/ready/metrics surface를 가져야 합니다.
- request id와 recovery flow가 test와 runtime 코드 둘 다에서 보일 정도로 분명해야 합니다.

## 실제 구현 표면

- gateway와 각 서비스의 `/api/v1/health/live`, `/ready`, `/ops/metrics`
- `X-Request-ID` 생성과 로그 문맥 유지
- Compose 기반 distributed recovery 시나리오
- `contracts/README.md`에 기록된 HTTP / event 계약

## 대표 검증 엔트리

- `python -m pytest tests/test_system.py -q`
- `make smoke`
- `docker compose up --build`

## 읽는 순서

1. [프로젝트 README](../../../labs/K-distributed-ops-lab/README.md)
2. [문제 정의](../../../labs/K-distributed-ops-lab/problem/README.md)
3. [실행 진입점](../../../labs/K-distributed-ops-lab/fastapi/README.md)
4. [계약 문서](../../../labs/K-distributed-ops-lab/fastapi/contracts/README.md)
5. [대표 system test](../../../labs/K-distributed-ops-lab/fastapi/tests/test_system.py)
6. [gateway main](../../../labs/K-distributed-ops-lab/fastapi/gateway/app/main.py)
7. [workspace-service route](../../../labs/K-distributed-ops-lab/fastapi/services/workspace-service/app/api/v1/routes/platform.py)
8. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../labs/K-distributed-ops-lab/README.md)
- [problem/README.md](../../../labs/K-distributed-ops-lab/problem/README.md)
- [fastapi/README.md](../../../labs/K-distributed-ops-lab/fastapi/README.md)
- [contracts/README.md](../../../labs/K-distributed-ops-lab/fastapi/contracts/README.md)
- [tests/test_system.py](../../../labs/K-distributed-ops-lab/fastapi/tests/test_system.py)
- [gateway/app/main.py](../../../labs/K-distributed-ops-lab/fastapi/gateway/app/main.py)
- [services/workspace-service/app/api/v1/routes/platform.py](../../../labs/K-distributed-ops-lab/fastapi/services/workspace-service/app/api/v1/routes/platform.py)
- [docs/verification-report.md](../../../docs/verification-report.md)
