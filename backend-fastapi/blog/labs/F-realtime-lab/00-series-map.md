# F-realtime-lab

이 글은 실시간 전달에서 연결 상태와 사용자 상태를 같은 것으로 다루지 않기 위해 어떤 모델이 필요한지를 따라간다. HTTP만으로는 설명되지 않는 WebSocket 연결, heartbeat, presence TTL, fan-out이 이 랩의 핵심 대상이다.

## 이 글이 붙잡는 질문
WebSocket connection lifecycle과 사용자 online 상태, 그리고 알림 fan-out을 어떤 식으로 나눠야 reconnect와 presence 만료를 설득력 있게 설명할 수 있는가가 이 글의 질문이다.

## 왜 이 프로젝트를 따로 읽어야 하나
README와 docs가 연결 인증, heartbeat, fan-out을 독립 문제로 정의하고, 통합 테스트는 잘못된 token disconnect와 presence 만료를 실제로 검증한다. 다른 랩 없이도 실시간 모델을 끝까지 따라갈 수 있다는 뜻이다.

## 이번 글에서 따라갈 흐름
1. 실시간 전달을 별도 상태 모델로 정의한다.
2. WebSocket connect와 heartbeat를 다른 surface로 분리한다.
3. presence 만료와 잘못된 token disconnect를 테스트로 고정한다.
4. 재검증 기록으로 health/probe surface를 닫는다.

## 마지막에 확인할 근거
- 코드: `labs/F-realtime-lab/fastapi/app/api/v1/routes/realtime.py::notifications_ws`
- 테스트/런타임: `labs/F-realtime-lab/fastapi/tests/integration/test_realtime.py::test_invalid_token_disconnects_and_presence_expires`
- CLI: `python3 -m compileall app tests`, `make lint`, `make test`, `make smoke`, `./tools/compose_probe.sh labs/F-realtime-lab/fastapi 8004`

## 이 글을 다 읽고 나면
- 연결 상태와 사용자 상태를 왜 구분해야 하는지 이해하게 된다.
- fan-out이 단순 broadcast가 아니라 연결 집합 관리 문제라는 점이 보인다.
- reconnect를 위한 HTTP 보조 surface가 왜 필요한지 감이 잡힌다.
- 검증 기록: 2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 모두 통과했다.
- 다음으로 이어 볼 대상: G-ops-lab
