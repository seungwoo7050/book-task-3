# Tactical Arena Server 개발 타임라인

현재 구현을 다시 읽으면 이 capstone의 흐름은 거대한 monolith를 한 번에 설명하는 식이 아니다. 오히려 control protocol, realtime packet contract, authoritative simulation, persistence, verification harness를 차례로 쌓아 올리는 구조다. 전환점은 다섯 번이다.

## 1. 먼저 control plane과 realtime plane을 다른 wire contract로 분리한다

`protocol.cpp`는 TCP control line과 UDP binary packet을 서로 다른 문법으로 고정한다. control plane은 `LOGIN name=alpha` 같은 line-based grammar를 쓰고, realtime plane은 `InputPacket`, `HeartbeatPacket`, `SnapshotPacket`을 big-endian binary로 encode/decode한다. 이 분리 덕분에 lobby semantics와 latency-sensitive gameplay traffic이 한 표현식에 섞이지 않는다.

즉 capstone의 첫 문턱은 socket 수보다 wire contract separation이다.

## 2. `ArenaServer`는 room lifecycle과 session recovery를 control verb로 묶는다

`arena_server.cpp`의 `handle_line()`은 `LOGIN`, `RESUME`, `CREATE_ROOM`, `JOIN_ROOM`, `READY`, `UDP_BIND`를 명시적으로 분기한다. 이 계층은 match simulation을 직접 돌리지 않고, player/session/room association을 조정하는 control coordinator 역할을 맡는다. resume token과 room membership state도 여기서 관리된다.

이 단계 때문에 capstone은 "게임 로직만 있는 서버"가 아니라, reconnect와 lobby flow까지 포함한 service surface로 확장된다.

## 3. 실제 authoritative semantics는 room-local `MatchState` 안에서 닫힌다

`MatchState::step()`은 disconnect forfeit, respawn, input apply, projectile update, finish rule을 fixed tick 안에 넣는다. unit test `test_state.cpp`는 out-of-order input ignore, lethal projectile -> respawn, disconnect timeout -> forfeit winner selection을 각각 고정한다. 즉 authoritative simulation의 핵심은 networking이 아니라 state transition consistency다.

이 전환 덕분에 realtime server가 단순 packet relay가 아니라 game authority라는 점이 분명해진다.

## 4. persistence는 side effect가 아니라 match result contract로 묶인다

`SqliteRepository::record_match()`는 transaction 안에서 `match_history` insert와 `player_stats` update를 함께 처리한다. unit test `test_repository.cpp`는 winner wins increment, loser losses increment, latest result blob 저장까지 확인한다. persistence가 별도 부록이 아니라 match conclusion semantics의 일부로 묶여 있는 셈이다.

즉 capstone의 데이터 계층은 "나중에 저장해도 되는 로그"가 아니라 gameplay 결과를 확정하는 contract다.

## 5. 마지막으로 verification harness가 system behavior를 역할별 시나리오로 분리해 고정한다

`make test`는 CTest unit 3개 뒤 integration test와 load smoke를 연속 실행한다. `integration_test.py`는 full match, resume same player, forfeit, out-of-order UDP scenario를 다루고, `load_smoke_test.py`는 2 rooms x 4 bots를 돌려 `match_history >= 2`, `players >= 8`를 확인한다. `run_bot_demo.sh`는 발표용 happy path를 간단히 재생성하고, 실제 rerun에서도 alpha/beta 둘 다 `MATCH_RESULT winner=1 scoreboard=1:0:0,2:0:0`를 출력했다.

결국 이 capstone의 마지막 전환점은 "서버가 돌아간다"에서 끝나지 않고, unit/integration/load/demo가 각기 다른 시스템 속성을 어떻게 증명하는지까지 구조화하는 데 있다.

## 지금 남는 한계

현재 구현은 production shooter backend가 아니다. TLS, anti-cheat, sharding, NAT traversal, spectator, advanced UDP reliability는 intentionally 빠져 있다. 하지만 학습용 authoritative server로서 protocol, state, persistence, verification의 경계를 한 저장소 안에 설명 가능하게 묶는 목표는 충분히 달성했다.
