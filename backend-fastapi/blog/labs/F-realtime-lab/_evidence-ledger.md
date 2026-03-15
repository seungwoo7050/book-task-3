# F-realtime-lab evidence ledger

## 독립 프로젝트 판정

- 판정: 처리 대상
- 이유: [`problem/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/problem/README.md) 가 WebSocket 인증, TTL heartbeat, fan-out, reconnect 보조 HTTP surface를 독립된 성공 기준으로 두고, 통합 테스트가 잘못된 token disconnect와 presence 만료를 직접 고정한다.
- 프로젝트 질문: connection lifecycle과 online 판정을 어떻게 분리해서 설명할 것인가.
- 복원 방식: 기존 `blog/` 본문은 근거에서 제외하고, `problem/README`, source code, tests, 실제 재실행 CLI만 사용했다.

## 근거 인벤토리

- [`README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/README.md)
- [`problem/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/problem/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/docs/README.md)
- [`fastapi/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/README.md)
- [`fastapi/Makefile`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/Makefile)
- [`app/api/v1/routes/realtime.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/app/api/v1/routes/realtime.py)
- [`app/runtime.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/app/runtime.py)
- [`app/main.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/app/main.py)
- [`app/api/deps.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/app/api/deps.py)
- [`app/core/config.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/app/core/config.py)
- [`tests/conftest.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/tests/conftest.py)
- [`tests/integration/test_realtime.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/tests/integration/test_realtime.py)
- [`tests/smoke.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi/tests/smoke.py)

## Chronology ledger

| 순서 | 당시 목표 | 변경 단위 | 실제로 확인한 것 | CLI | 검증 신호 | 다음으로 넘어간 이유 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 실시간 기능이 메시지 전달보다 connection model 문제인지 먼저 판정한다 | `README.md`, `problem/README.md`, `docs/README.md` | 성공 기준이 payload보다 WebSocket 인증, TTL heartbeat, fan-out, reconnect 보조 HTTP surface를 먼저 요구한다 | `sed -n '1,240p' backend-fastapi/labs/F-realtime-lab/README.md`<br>`sed -n '1,260p' backend-fastapi/labs/F-realtime-lab/problem/README.md` | 이 랩의 중심은 메시지 내용보다 연결 상태를 어떻게 모델링하는가다 | 이제 route와 runtime이 그 모델을 어떤 표면으로 분리하는지 내려가 봐야 한다 |
| 2 | WebSocket 연결과 presence 판정을 어떤 surface로 나누는지 확인한다 | `realtime.py`, `runtime.py`, `schemas/realtime.py` | WebSocket route, presence heartbeat, presence 조회, notification fan-out이 서로 다른 entry point로 분리돼 있다 | `rg -n 'presence|notifications|websocket|token' backend-fastapi/labs/F-realtime-lab/fastapi/app` | 연결이 살아 있음과 online 판정은 같은 값처럼 보이지만 갱신 표면이 다르다 | 다음은 이 상태가 어디에 저장되는지, Redis/DB와 어떤 관계인지 확인한다 |
| 3 | 핵심 상태가 persistence가 아니라 인메모리 runtime에 있음을 고정한다 | `main.py`, `api/deps.py`, `runtime.py`, `config.py` | `ConnectionManager`와 `PresenceTracker`는 `app.state`에 올라가고, 사용자별 소켓 집합과 monotonic `last_seen`으로 fan-out/online을 계산한다 | `rg -n 'app.state|connections|last_seen|ttl_seconds' backend-fastapi/labs/F-realtime-lab/fastapi/app` | Redis/DB는 readiness surface와 확장 경계 쪽에 남고, 현재 realtime delivery 핵심은 메모리 모델이다 | 이제 테스트가 invalid token, TTL expiry, WebSocket delivery를 어떻게 고정하는지 본다 |
| 4 | runtime semantics를 테스트와 smoke에서 확인한다 | `tests/conftest.py`, `test_realtime.py`, `smoke.py` | 잘못된 token은 즉시 disconnect, TTL 만료 후 offline, 정상 연결에는 HTTP notification이 fan-out 된다 | `sed -n '1,360p' backend-fastapi/labs/F-realtime-lab/fastapi/tests/integration/test_realtime.py` | 실시간 랩의 핵심은 fan-out 성공만이 아니라 끊김과 만료 뒤 상태가 어떻게 수렴하는가다 | 마지막으로 오늘 셸에서 공식 진입점과 보조 재실행이 어디서 갈리는지 닫는다 |
| 5 | 현재 재검증 상태를 최신 값으로 닫는다 | `Makefile`, 현재 셸 환경 | lint는 통과하고, `PYTHONPATH` 보조 재실행은 테스트와 smoke가 통과하지만, 기본 `make` 진입점은 path/interpreter 문제를 드러낸다 | `make lint`<br>`make test`<br>`make smoke`<br>`PYTHONPATH=. pytest`<br>`PYTHONPATH=. python -m tests.smoke` | `make lint` 통과, `make test`는 `No module named 'app'`, `make smoke`는 `No module named 'fastapi'`, 보조 재실행은 통과한다 | 문서는 runtime 모델이 살아 있다는 사실과 공식 진입점 drift를 함께 남겨야 한다 |
