# J-edge-gateway-lab

이 글은 브라우저에 보이는 public API shape를 gateway 하나에 남기고 내부 서비스 계약은 더 단순하게 만들 수 있는가를 묻는다. J 랩은 MSA 외부의 얼굴과 내부 연결 방식을 구분해서 보는 단계다.

## 이 글이 붙잡는 질문
쿠키, CSRF, WebSocket edge, public `/api/v1` 경로를 gateway에 모아 두면서도 내부 서비스 계약을 지나치게 복잡하게 만들지 않을 수 있는가가 핵심 질문이다.

## 왜 이 프로젝트를 따로 읽어야 하나
README와 docs는 gateway를 단순 reverse proxy가 아니라 edge contract로 설명하고, system test는 public 경로만으로 협업 흐름을 끝까지 검증한다. 이 랩을 따로 읽어야 gateway 도입의 비용과 이익이 동시에 보인다.

## 이번 글에서 따라갈 흐름
1. gateway를 단순 중계가 아니라 edge 계약으로 정의한다.
2. cookie와 bearer translation, 내부 fan-out 경로를 본다.
3. public `/api/v1`만으로 invite와 websocket 알림이 이어지는지 확인한다.
4. 재검증 기록으로 edge runtime을 닫는다.

## 마지막에 확인할 근거
- 코드: `labs/J-edge-gateway-lab/fastapi/gateway/app/api/v1/routes/platform.py::_auth_headers`
- 테스트/런타임: `labs/J-edge-gateway-lab/fastapi/tests/test_system.py::test_v2_system_flow_and_notification_recovery`
- CLI: `make test`, `python -m pytest tests/test_system.py -q`, `python -m tests.smoke`, `docker compose up --build`

## 이 글을 다 읽고 나면
- 브라우저용 인증 규칙을 왜 gateway에 남겨 두는지 이해하게 된다.
- 내부 서비스가 단순한 계약을 유지하려면 edge에서 무엇을 흡수해야 하는지 보게 된다.
- public path 안정성이 시스템 구조를 어떻게 바꾸는지 감이 잡힌다.
- 검증 기록: 2026-03-10에 gateway/identity/workspace/notification unit test, system test, smoke가 모두 통과했다.
- 다음으로 이어 볼 대상: K-distributed-ops-lab
