# arenaserv evidence ledger

`arenaserv`의 chronology는 "ticklab 엔진은 그대로 두고, transport와 time-aware runtime을 위에 올린다"는 관점으로 읽는 편이 가장 명확하다. 아래 ledger는 그 흐름을 `Phase 1`부터 `Phase 4`까지 다시 묶은 것이다.

## Phase 1

가장 먼저 달라지는 곳은 engine이 아니라 event loop다. 네트워크가 조용해도 시간이 흐르는 서버가 필요해지기 때문이다.

- 순서: 1
- 시간 표지: Phase 1
- 당시 목표: event loop가 fixed tick을 함께 돌릴 수 있게 만든다.
- 변경 단위: `cpp/include/inc/EventManager.hpp`, `cpp/src/EventManager.cpp`, `cpp/src/Server.cpp`
- 처음 가설: arena server는 새 protocol보다 먼저 "이벤트 대기 중에도 tick이 멈추지 않는 loop"가 필요하다.
- 실제 조치: `EventManager::retrieve_events()`에 `timeout_ms`를 추가하고 `Server::pump_ticks()`가 `tick_interval_ms`마다 `engine.advance_one_tick()`을 호출하게 만든다.
- CLI: `make clean && make test`
- 검증 신호: smoke test가 별도 입력 없이도 countdown과 draw timeout을 기다려서 확인한다.
- 핵심 코드 앵커: `EventManager::retrieve_events(..., timeout_ms)`, `Server::run_event_loop()`, `Server::pump_ticks()`
- 새로 배운 것: authoritative TCP server의 핵심 차이는 소켓 read/write보다 "시간이 흐르는 engine"을 루프에 섞는 방식에 있다.
- 다음: session handshake를 붙인다.

## Phase 2

시간이 흐르는 루프가 생기면, 다음엔 connection과 player session을 분리해야 한다. 그래야 rejoin이 transport 재접속이 아니라 세션 연속성으로 설명된다.

- 순서: 2
- 시간 표지: Phase 2
- 당시 목표: raw TCP connection을 engine session token과 연결한다.
- 변경 단위: `cpp/src/Server.cpp`
- 처음 가설: `HELLO`와 `REJOIN`만 제대로 되면 connection과 session을 분리해 다룰 수 있다.
- 실제 조치: `Client`에 `token`을 두고 `token_to_fd` 맵을 만들며, `handle_hello()`가 `engine.register_player()` 이후 `dispatch_engine_events()`로 `WELCOME token-n`을 밀어낸다.
- CLI: `make clean && make test`
- 검증 신호: 테스트 helper `register()`가 실제 `WELCOME token-...`에서 토큰을 추출한다.
- 핵심 코드 앵커: `Server::Client`, `handle_hello()`, `dispatch_engine_events()`
- 새로 배운 것: connection id와 player session token을 분리해야 rejoin이 가능해진다.
- 다음: queue/ready와 room event bridge를 본다.

## Phase 3

세션이 연결되고 나면, 서버의 주된 일은 게임 규칙을 다시 계산하는 것이 아니라 엔진 호출과 이벤트 fan-out을 맡는 bridge가 된다.

- 순서: 3
- 시간 표지: Phase 3
- 당시 목표: 엔진 이벤트를 TCP 응답으로 fan-out하고, raw line command를 엔진 호출로 번역한다.
- 변경 단위: `cpp/src/Server.cpp`, `cpp/src/MatchEngine.cpp`
- 처음 가설: `MatchEngine`은 그대로 두고 `Server`가 입력 파싱과 event fan-out만 맡으면 transport가 얇아진다.
- 실제 조치: `handle_queue()`, `handle_ready()`, `handle_input()`, `handle_rejoin()`, `handle_leave()`가 엔진 API를 호출하고 `dispatch_engine_events()`가 single event와 room event를 분리해 보낸다.
- CLI: `make clean && make test`
- 검증 신호: smoke test가 `ROOM arena-1 lobby`, `COUNTDOWN 3`, `SNAPSHOT 0`, `HIT`, `ROUND_END alpha`, `ERROR stale_sequence`를 실제 소켓에서 본다.
- 핵심 코드 앵커: `handle_line()`, `handle_queue()`, `handle_ready()`, `handle_input()`, `handle_rejoin()`, `dispatch_engine_events()`
- 새로 배운 것: arenaserv의 핵심 코드는 대부분 engine을 다시 쓰는 것이 아니라 "event scope를 fd로 fan-out하는 bridge"다.
- 다음: reconnect, room_full, draw timeout까지 실제 smoke 시나리오로 닫는다.

## Phase 4

마지막 phase는 capstone proof를 transport 표면까지 끌어올리는 단계다. duel, rejoin, overflow, draw timeout이 서로 다른 시나리오로 나뉘는 이유도 읽기 편한 proof를 만들기 위해서다.

- 순서: 4
- 시간 표지: Phase 4
- 당시 목표: duel, rejoin, overflow, draw timeout을 TCP 표면에서 모두 증명한다.
- 변경 단위: `cpp/tests/test_arenaserv.py`
- 처음 가설: capstone proof는 한 테스트에 몰기보다 session continuity, room capacity, round timeout을 분리해 보는 편이 읽기 쉽다.
- 실제 조치: `scenario_duel_and_rejoin()`, `scenario_party_lobby()`, `scenario_draw_timeout()`를 만든다.
- CLI: `make clean && make test`
- 검증 신호: `arenaserv smoke passed.`
- 핵심 코드 앵커: `tests/test_arenaserv.py`
- 새로 배운 것: authoritative engine proof를 transport까지 끌어올리려면 rejoin, room_full, draw timeout 같은 경계 장면이 꼭 필요하다.
- 다음: 같은 저장소의 다른 capstone인 `ircserv`와 transport/state bridge 패턴을 비교할 수 있다.

