# F-realtime-lab structure plan

## 한 줄 약속

- 실시간 전달을 WebSocket 기술 소개가 아니라 connection lifecycle과 presence TTL이 보이는 상태 모델로 읽게 만든다.

## 독자 질문

- 왜 이 랩은 알림 payload보다 connection state와 user presence를 먼저 구분하는가
- WebSocket 인증이 현재 `token == user_id` 수준으로 단순화된 이유는 무엇인가
- fan-out을 메모리 소켓 집합으로 시작하는 현재 구조는 무엇을 보여 주고 무엇을 아직 하지 않는가
- reconnect 보조 HTTP surface는 현재 구현에서 어디까지 제공되는가
- 현재 문서에 적힌 검증 명령은 지금 셸에서 그대로 재현되는가

## 이번 Todo의 작성 원칙

- 다른 lab 문장이나 구조를 가져오지 않는다.
- 기존 `blog/` 본문은 사실 근거로 사용하지 않는다.
- `problem/README`, source code, tests, 실제 재실행 CLI만으로 서사를 복원한다.
- 메모리 기반 모델의 선명함과 현재 확장 한계를 둘 다 숨기지 않는다.

## 글 흐름

1. 문제 정의가 실시간 메시지보다 connection model을 먼저 묻는다는 점부터 고정한다.
2. WebSocket route와 presence HTTP surface를 나란히 두고 상태 갱신 표면 차이를 설명한다.
3. `app.state` runtime 객체와 TTL 계산으로 현재 fan-out/presence 모델을 읽는다.
4. invalid token disconnect, TTL expiry, WebSocket delivery를 테스트로 고정한다.
5. 오늘 다시 돌린 CLI 결과로 현재 재현 가능 상태를 닫는다.

## Evidence anchor

- 주 코드 앵커: [runtime.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/app/runtime.py)
- 보조 코드 앵커: [realtime.py route](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/app/api/v1/routes/realtime.py), [main.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/app/main.py), [config.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/app/core/config.py)
- 테스트 루프 앵커: [conftest.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/tests/conftest.py), [test_realtime.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/tests/integration/test_realtime.py), [smoke.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/tests/smoke.py)
- CLI 앵커: `make lint`, `make test`, `make smoke`, `PYTHONPATH=. pytest`, `PYTHONPATH=. python -m tests.smoke`

## 끝에서 남겨야 할 문장

- 이 랩의 강점은 connection state, presence TTL, user-level fan-out을 아주 작은 인메모리 모델로 선명하게 보여 준다는 점이다.
- 이 랩의 현재 한계는 인증이 `token == user_id`로 단순화돼 있고, Redis/DB는 핵심 전달 경로가 아니라 readiness와 확장 경계에만 남아 있으며, 2026-03-14 셸에서는 기본 `make` 진입점이 path/interpreter 문제로 바로 닫히지 않는다는 점이다.
- 다음 랩인 `G-ops-lab`은 이 연결 모델 위에서 운영성, health, 관찰 가능성을 더 직접적으로 다루는 비교 대상으로 연결한다.
