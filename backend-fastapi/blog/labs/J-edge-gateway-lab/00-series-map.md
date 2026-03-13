# J-edge-gateway-lab 시리즈 지도

이 시리즈는 public API shape를 유지한 채 내부 서비스를 fan-out 하는 gateway가 어떤 책임을 맡는지, 실제 source tree 기준으로 다시 읽습니다.

## 이 시리즈가 보는 문제

- 외부 클라이언트는 하나의 `/api/v1/*`만 보는데 내부는 여러 서비스로 분리된 상태를 어떻게 설명할 것인가
- cookie와 CSRF를 edge에만 남기고도 내부 서비스 호출을 이어 갈 수 있는가

## 실제 구현 표면

- gateway의 `/api/v1/auth/*`, `/api/v1/platform/*`
- 내부 호출용 `ServiceClient`
- `X-Request-ID` 생성과 전파
- websocket edge와 notification recovery 시나리오

## 대표 검증 엔트리

- `python -m pytest tests/test_system.py -q`
- `make smoke`
- `docker compose up --build`

## 읽는 순서

1. [프로젝트 README](../../../labs/J-edge-gateway-lab/README.md)
2. [문제 정의](../../../labs/J-edge-gateway-lab/problem/README.md)
3. [실행 진입점](../../../labs/J-edge-gateway-lab/fastapi/README.md)
4. [gateway README](../../../labs/J-edge-gateway-lab/fastapi/gateway/README.md)
5. [대표 system test](../../../labs/J-edge-gateway-lab/fastapi/tests/test_system.py)
6. [gateway main](../../../labs/J-edge-gateway-lab/fastapi/gateway/app/main.py)
7. [gateway runtime](../../../labs/J-edge-gateway-lab/fastapi/gateway/app/runtime.py)
8. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../labs/J-edge-gateway-lab/README.md)
- [problem/README.md](../../../labs/J-edge-gateway-lab/problem/README.md)
- [fastapi/README.md](../../../labs/J-edge-gateway-lab/fastapi/README.md)
- [gateway/README.md](../../../labs/J-edge-gateway-lab/fastapi/gateway/README.md)
- [tests/test_system.py](../../../labs/J-edge-gateway-lab/fastapi/tests/test_system.py)
- [gateway/app/main.py](../../../labs/J-edge-gateway-lab/fastapi/gateway/app/main.py)
- [gateway/app/runtime.py](../../../labs/J-edge-gateway-lab/fastapi/gateway/app/runtime.py)
- [docs/verification-report.md](../../../docs/verification-report.md)
