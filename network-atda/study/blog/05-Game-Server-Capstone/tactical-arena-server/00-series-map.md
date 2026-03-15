# Tactical Arena Server 시리즈 맵

이 capstone의 중심 질문은 "authoritative game server를 설명 가능하게 만들려면 어떤 경계를 코드와 테스트에서 분리해야 하는가"다. 현재 구현은 TCP line protocol로 lobby/control을, UDP binary packets로 realtime input/snapshot을, `RoomContext` strand와 `MatchState`로 simulation을, `SqliteRepository`로 persistence를, integration/load/demo scripts로 end-to-end verification을 각각 나눈다.

## 이 capstone을 읽는 질문

- 왜 control plane은 TCP line protocol이고 realtime plane은 UDP binary packet인가
- room-local strand와 `MatchState`가 authoritative simulation의 경계를 어떻게 만든다
- unit test, integration scenario, load smoke, bot demo는 서로 어떤 다른 시스템 속성을 고정하는가

## 이번에 사용한 근거

- `problem/README.md`
- `cpp/src/arena_server.cpp`
- `cpp/src/protocol.cpp`
- `cpp/src/state.cpp`
- `cpp/src/repository.cpp`
- `cpp/tests/test_protocol.cpp`
- `cpp/tests/test_state.cpp`
- `cpp/tests/test_repository.cpp`
- `problem/script/integration_test.py`
- `problem/script/load_smoke_test.py`
- 2026-03-14 재실행한 `make test`, `run-bot-demo`

## 이번 재실행에서 고정한 사실

- control line parser는 `VERB key=value ...` 형식을 쓰고 newline으로 종료한다.
- UDP packet codec은 `InputPacket`, `HeartbeatPacket`, `SnapshotPacket`을 big-endian binary로 encode/decode한다.
- `MatchState`는 projectile hit, respawn, disconnect forfeit, winner selection까지 authoritative state transition을 가진다.
- full `make test`는 CTest unit 3개 뒤 integration scenario와 load smoke를 연속 실행한다.
