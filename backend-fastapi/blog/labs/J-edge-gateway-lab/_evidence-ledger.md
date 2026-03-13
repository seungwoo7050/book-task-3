# J-edge-gateway-lab Evidence Ledger

## 독립 프로젝트 판정
- 판정: 처리 대상
- 이유: README와 docs가 gateway를 public shape 유지 장치로 정의하고, `compose.yaml`, gateway route, `tests/test_system.py`가 브라우저 흐름과 내부 fan-out을 함께 검증한다.
- 프로젝트 질문: 서비스가 나뉘어도 브라우저는 하나의 API만 보게 하려면, cookie와 CSRF를 어디에 두고 내부 계약을 어떻게 단순화해야 하는가.
- 주의: finer-grained 구현 순서는 commit granularity가 거칠어서 README, docs, code surface, tests 의존 순서를 바탕으로 복원했다. 실제 날짜가 확인되는 부분은 git log와 검증 보고서에만 한정했다.

## 소스 인벤토리
- `labs/J-edge-gateway-lab/README.md`
- `labs/J-edge-gateway-lab/problem/README.md`
- `labs/J-edge-gateway-lab/docs/README.md`
- `labs/J-edge-gateway-lab/fastapi/README.md`
- `labs/J-edge-gateway-lab/fastapi/Makefile`
- `labs/J-edge-gateway-lab/fastapi/compose.yaml`
- `backend-fastapi/.github/workflows/labs-fastapi.yml`
- `backend-fastapi/docs/verification-report.md`
- `backend-fastapi/labs/J-edge-gateway-lab/fastapi/gateway/app/api/v1/routes/platform.py`
- `backend-fastapi/labs/J-edge-gateway-lab/fastapi/tests/test_system.py`
- `git log -- backend-fastapi/labs/J-edge-gateway-lab`

## 프로젝트 표면 요약
- 문제 요약: 서비스가 분리된 뒤에도 외부 클라이언트는 하나의 API만 보고 싶다. 이 랩은 gateway가 public API shape를 유지하고, cookie와 CSRF를 edge에만 두며, 내부 서비스에는 request id와 bearer token만 전달하는 구조를 연습한다. gateway가 `/api/v1/auth/*`, `/api/v1/platform/*` 경로를 유지한다. 로그인 후 쿠키가 gateway에서만 설정된다. 상세 성공 기준과 제외 범위는 problem/README.md에 둡니다.
- 성공 기준: gateway가 `/api/v1/auth/*`, `/api/v1/platform/*` 경로를 유지한다. 로그인 후 쿠키가 gateway에서만 설정된다. 내부 호출에 `X-Request-ID`가 전달된다.
- 설계 질문: 왜 public API를 gateway가 유지해야 하는가 왜 쿠키와 CSRF를 내부 서비스에 넘기지 않는가 request id는 어떤 경로로 전파되는가 upstream 오류는 어디서 어떤 HTTP 상태로 번역해야 하는가
- 실제 검증 surface: make lint make test make smoke docker compose up --build 실행과 환경 설명은 fastapi/README.md에서 다룹니다. 마지막 기록된 실제 검증 결과는 ../../docs/verification-report.md에 있습니다.

## 시간 표지
- 2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료
- 2026-03-11 89dc218 feat: add new project in fastapi (MSA)

## Chronology Ledger
| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1, 2026-03-11 add project commit 89dc218을 기준으로 복원 | 브라우저가 하나의 API만 보게 하는 edge 역할 정의 | README.md, problem/README.md, docs/README.md | 서비스를 나누면 클라이언트도 여러 서비스를 직접 호출해야 할 것 | gateway가 `/api/v1/auth/*`, `/api/v1/platform/*`를 유지하고 cookie/CSRF를 edge에만 두도록 문제를 재정의 | README의 `docker compose up --build` | 성공 기준이 public route shape, gateway cookie 설정, `X-Request-ID` 전파를 직접 명시 | problem/README.md 성공 기준 | gateway의 역할은 새 기능을 더하는 게 아니라 브라우저와 내부 서비스 계약을 다시 나누는 일이다 | edge가 어떤 헤더만 내부로 넘길지 구현 |
| 2 | Phase 2, gateway route를 중심으로 복원 | cookie 기반 브라우저 상태를 bearer 기반 내부 호출로 번역 | gateway/app/api/v1/routes/auth.py, gateway/app/api/v1/routes/platform.py, gateway/app/runtime.py | 내부 서비스도 cookie와 CSRF를 직접 읽게 두면 더 단순할 것 | `_auth_headers`로 access token cookie를 bearer header로 바꾸고, gateway `client.request(...)`가 workspace/notification으로 fan-out 하게 구성 | `make test` | `_auth_headers`가 cookie에서 access token을 읽어 `Authorization` header로 바꿈 | gateway/app/api/v1/routes/platform.py::_auth_headers | edge에 cookie를 모으면 내부 서비스 계약은 bearer claims로 훨씬 단순해진다 | public `/api/v1`만 호출하는 system flow 고정 |
| 3 | Phase 3, system test가 edge/public surface를 증명 | owner와 collaborator가 gateway만 호출해 invite/comment/websocket 알림까지 끝내는지 확인 | tests/test_system.py | 서비스별 unit test만 있어도 gateway 역할이 충분히 보일 것 | owner와 collaborator HTTP client가 모두 `http://127.0.0.1:8013`의 public `/api/v1/*`만 호출하고, websocket도 gateway 경로로 연결되는 시나리오를 테스트화 | `python -m pytest tests/test_system.py -q` | public platform comment 후 websocket이 gateway 경로에서 notification을 수신 | tests/test_system.py::test_v2_system_flow_and_notification_recovery | gateway 글에서는 내부 호출보다 외부 클라이언트가 무엇을 몰라도 되는지가 더 중요하다 | 실제 재검증 결과 연결 |
| 4 | 2026-03-10 재검증 + 2026-03-11 track polish | gateway/identity/workspace/notification 전체가 실제로 검증됐다는 사실 남기기 | docs/verification-report.md, fastapi/README.md | gateway는 문서상 구조만 설명해도 충분할 것 | service unit tests, `python -m pytest tests/test_system.py -q`, `python -m tests.smoke` 결과를 남김 | `make test`의 service unit test 구간, `python -m pytest tests/test_system.py -q`, `python -m tests.smoke` | 2026-03-10 기준 gateway/identity/workspace/notification unit test, system test, smoke 통과 | docs/verification-report.md J-edge-gateway-lab 항목 | edge layer도 결국 서비스별 unit test와 end-to-end public flow 둘 다 필요하다 | 분산 운영성 surface 확장 |
