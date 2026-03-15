# F-realtime-lab series map

이 시리즈는 F 랩을 "WebSocket 붙인 예제"로 읽지 않는다. 실제 source of truth를 따라가 보면 이 프로젝트의 중심은 연결 상태와 사용자 online 상태를 같은 값처럼 취급하지 않고, heartbeat TTL과 fan-out을 인메모리 runtime 모델로 얼마나 단순하게 드러내는가에 있다.

## 이 시리즈가 붙잡는 질문

- WebSocket 연결이 살아 있다는 것과 사용자가 online이라고 판정되는 것은 어디서 갈라지는가
- presence는 왜 receive loop 하나로 끝나지 않고 별도 heartbeat/조회 HTTP surface를 가지는가
- 한 사용자의 다중 소켓 fan-out은 현재 어디까지 구현되어 있고, Redis는 왜 아직 확장 경계로만 남아 있는가
- 재연결 보조용 HTTP surface라는 문제 정의에 비해 현재 구현은 어디까지를 직접 제공하는가

## 왜 이 순서로 읽는가

1. `problem/README.md`와 `docs/README.md`로 이 랩이 메시지 내용보다 connection lifecycle, TTL heartbeat, fan-out을 먼저 묻는다는 점을 확인한다.
2. `realtime.py` route와 `runtime.py`를 보며 WebSocket connect, presence heartbeat, notification fan-out이 각각 어떤 표면으로 나뉘는지 확인한다.
3. `main.py`, `api/deps.py`, `config.py`를 따라가며 이 모델이 DB가 아니라 `app.state` 메모리 객체로 유지된다는 점을 본다.
4. 통합 테스트와 smoke를 함께 보며 잘못된 token disconnect, TTL 만료, WebSocket fan-out이 현재 셸에서 어떻게 재현되는지 확인한다.
5. 마지막에 `make lint`, `make test`, `make smoke`와 보조 재실행 결과를 붙여 현재 재현 가능 상태를 닫는다.

## 근거로 사용한 자료

- `backend-fastapi/labs/F-realtime-lab/README.md`
- `backend-fastapi/labs/F-realtime-lab/problem/README.md`
- `backend-fastapi/labs/F-realtime-lab/docs/README.md`
- `backend-fastapi/labs/F-realtime-lab/fastapi/README.md`
- `backend-fastapi/labs/F-realtime-lab/fastapi/Makefile`
- `backend-fastapi/labs/F-realtime-lab/fastapi/app/api/v1/routes/realtime.py`
- `backend-fastapi/labs/F-realtime-lab/fastapi/app/runtime.py`
- `backend-fastapi/labs/F-realtime-lab/fastapi/app/main.py`
- `backend-fastapi/labs/F-realtime-lab/fastapi/app/api/deps.py`
- `backend-fastapi/labs/F-realtime-lab/fastapi/app/core/config.py`
- `backend-fastapi/labs/F-realtime-lab/fastapi/tests/conftest.py`
- `backend-fastapi/labs/F-realtime-lab/fastapi/tests/integration/test_realtime.py`
- `backend-fastapi/labs/F-realtime-lab/fastapi/tests/smoke.py`

## 현재 검증 상태

- 2026-03-14 기준 `make lint`는 현재 셸에서 통과했다.
- 같은 날짜 `make test`는 `tests/conftest.py` import 시점에 `ModuleNotFoundError: No module named 'app'`로 멈췄다.
- 같은 날짜 `make smoke`는 `python3`가 `/opt/homebrew/bin/python3`를 타면서 `ModuleNotFoundError: No module named 'fastapi'`로 실패했다.
- 보조 확인으로 `PYTHONPATH=. pytest`를 다시 돌리면 WebSocket 통합 테스트 2개가 통과한다. 다만 `pytest_asyncio`는 `asyncio_default_fixture_loop_scope` 미설정 deprecation warning을 남긴다.
- `PYTHONPATH=. python -m tests.smoke`도 `/api/v1/health/live` 200으로 통과한다.
- 즉 현재 실시간 runtime 모델 자체는 살아 있지만, 공식 `make` 진입점은 여전히 import path와 interpreter 선택에 영향을 받는다.

## 현재 구현에서 좁게 남은 부분

- WebSocket 인증은 현재 `token == user_id` 비교 한 줄로 단순화돼 있다.
- presence와 fan-out의 핵심 상태는 [`app.state.connection_manager`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/app/main.py) 와 [`app.state.presence_tracker`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/app/main.py) 에 인메모리로 유지된다.
- Redis와 DB health check는 readiness surface에 남아 있지만, 실제 realtime delivery 경로는 그것들에 기대지 않는다.
- 문제 정의가 말한 reconnect 보조 HTTP surface는 현재 `presence heartbeat`와 `presence 조회`로 읽히지만, 메시지 replay나 session resume 같은 더 강한 surface는 없다.

## 현재 범위 밖

- 완전한 broker 기반 수평 확장 구현
- 메시지 replay 보장
- 대규모 채팅 제품 수준의 방/채널 모델

## 본문

- [10-development-timeline.md](10-development-timeline.md)
  - connection lifecycle, TTL presence, in-memory fan-out, current verification split을 구현 순서로 복원한다.
