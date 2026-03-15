# Tactical Arena Server Evidence Ledger

## 이번에 읽은 자료

- 문제 사양: `study/05-Game-Server-Capstone/tactical-arena-server/problem/README.md`
- 구현 엔트리:
  - `study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_server.cpp`
  - `study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/protocol.cpp`
  - `study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/state.cpp`
  - `study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/repository.cpp`
- unit tests:
  - `cpp/tests/test_protocol.cpp`
  - `cpp/tests/test_state.cpp`
  - `cpp/tests/test_repository.cpp`
- scenario harness:
  - `problem/script/integration_test.py`
  - `problem/script/load_smoke_test.py`
  - `problem/script/run_bot_demo.sh`

## 핵심 코드 근거

- `parse_control_line()` / `format_control_line()`: TCP control plane grammar를 고정한다.
- `encode_input_packet()` / `decode_input_packet()` / `encode_snapshot_packet()` / `decode_snapshot_packet()`: UDP realtime packet contract를 고정한다.
- `ArenaServer::handle_line()`: login, resume, room lifecycle, ready, udp_bind를 control verbs로 분기한다.
- `MatchState::step()`: disconnect forfeit, respawn, input apply, projectile update, match finish를 authoritative tick 안에 넣는다.
- `SqliteRepository::record_match()`: transaction 안에서 match_history insert와 player_stats update를 함께 처리한다.

## 테스트 근거

`make -C network-atda/study/05-Game-Server-Capstone/tactical-arena-server/problem test`

결과:

- `test_protocol` pass
- `test_state` pass
- `test_repository` pass
- `integration_test ok`
- `load_smoke_test ok`

보조 실행:

- `make -C .../tactical-arena-server/problem run-bot-demo`
- 결과:
  - `demo-beta MATCH_RESULT winner=1 scoreboard=1:0:0,2:0:0`
  - `demo-alpha MATCH_RESULT winner=1 scoreboard=1:0:0,2:0:0`

integration/load 세부:

- `integration_test.py`
  - `scenario_full_match`
  - `scenario_resume_same_player`
  - `scenario_forfeit`
  - `scenario_out_of_order_udp`
- `load_smoke_test.py`
  - `room-count=2`
  - `bots-per-room=4`
  - 검증 조건 `match_history >= 2`, `players >= 8`

## 이번에 고정한 해석

- 이 capstone의 가치는 feature count보다, protocol/simulation/persistence/test harness가 서로 느슨하지만 검증 가능한 경계로 나뉘어 있다는 데 있다.
- integration harness는 reconnect, forfeit, UDP ordering 같은 system behavior를, load smoke는 multi-room capacity baseline을, bot demo는 presentation-grade happy path를 각각 맡는다.
- authoritative server라 해도 simulation correctness와 protocol correctness는 서로 다른 테스트로 고정해야 한다.
- 그리고 load smoke와 bot demo는 같은 "실행된다"는 문장이라도 서로 다른 목적을 가진 증거라는 점이 중요하다.
