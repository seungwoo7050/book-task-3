# arenaserv structure plan

`arenaserv`은 rule set 설명보다 bridge 설명이 더 중요한 문서다. 독자는 "ticklab 엔진이 왜 그대로 남아 있는가"와 "그러면 서버는 정확히 무엇을 새로 맡는가"를 알고 싶어 한다. 그래서 시리즈도 timed runtime, engine event bridge, end-to-end TCP proof 순서로 설계한다.

## 10-server-surface-and-session-handshake.md

첫 글은 `EventManager::retrieve_events(..., timeout_ms)`, `Server::run_event_loop()`, `Server::pump_ticks()`, `handle_hello()`를 중심으로 잡는다. `MatchEngine`은 이미 준비돼 있고, 새 일은 시간을 잃지 않는 루프와 세션 토큰 앞면을 만드는 데 있다는 점을 먼저 분명히 해야 한다.

## 20-queue-ready-and-engine-bridge.md

둘째 글은 `handle_queue()`, `handle_ready()`, `dispatch_engine_events()`, `token_to_fd`, `pump_ticks()`를 중심에 둔다. 여기서는 command parsing보다 engine event fan-out이 이 capstone의 실질적인 구현이라는 점이 독자에게 자연스럽게 들어와야 한다.

## 30-input-rejoin-and-room-events.md

마지막 글은 `handle_input()`, `handle_rejoin()`, `handle_leave()`, `tests/test_arenaserv.py`를 묶어 proof 장면으로 읽게 만든다. `make clean && make test`, `arenaserv smoke passed.`를 닫는 신호로 두고, invalid input, stale sequence, rejoin, room_full, draw timeout이 실제 소켓에서 어떻게 확인되는지 보여 준다.

