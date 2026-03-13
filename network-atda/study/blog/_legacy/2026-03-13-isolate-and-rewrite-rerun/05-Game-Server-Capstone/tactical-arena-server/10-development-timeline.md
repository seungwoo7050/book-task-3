# Tactical Arena Server — Development Timeline

Tactical Arena Server를 다시 쓸 때 가장 먼저 고정한 건 `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test`가 기대하는 실행 표면이었다. 기존 blog 초안은 `_legacy/2026-03-13-isolate-and-rewrite/05-Game-Server-Capstone/tactical-arena-server`로 옮기고, 이번 글은 `README.md`, `problem/Makefile`, 그리고 `cpp/src/`와 `cpp/tests/`만으로 chronology를 복원했다.

```bash
make -C study/05-Game-Server-Capstone/tactical-arena-server/problem run-server
make -C study/05-Game-Server-Capstone/tactical-arena-server/problem run-bot-demo
make -C study/05-Game-Server-Capstone/tactical-arena-server/problem load-test
make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test
```

## Session 1 — TCP control과 UDP gameplay 프로토콜부터 닫았다
먼저 붙든 질문은 "capstone의 첫 복잡성은 game rule보다 protocol surface가 TCP/UDP 두 채널로 갈라진다는 점이다"였다. 그래서 작업 단위도 `cpp/src/protocol.cpp`, `docs/concepts/protocol.md`, `problem/code/control-protocol.txt`처럼 작게 잘랐다. 실제 조치는 control line parse/format, resume token 생성, binary packet encode/decode를 별도 protocol layer로 분리했다.
이 구간의 기준 명령은 `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem run-server`였고, 여기서 확인한 신호는 다음과 같았다. control command와 UDP input packet을 같은 naming/field 규칙으로 설명할 수 있게 됐다. 이 단계가 남긴 개념 메모도 분명했다. application protocol 설계가 곧 테스트 가능성의 출발점이라는 감각.

## Session 2 — authoritative simulation을 state layer로 분리했다
먼저 붙든 질문은 "room strand 안에서 돌아가는 authoritative state는 `step()`이 하나의 truth가 되어야 설명 가능하다"였다. 그래서 작업 단위도 `cpp/src/state.cpp`, `docs/concepts/simulation.md`처럼 작게 잘랐다. 실제 조치는 submit_input, step, build_snapshot_packet, apply_forfeit_timeouts를 중심으로 fixed tick state machine을 만들었다.
이 구간의 기준 명령은 `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem run-bot-demo`였고, 여기서 확인한 신호는 다음과 같았다. bot demo와 state test가 같은 tick/update 규칙을 공유하게 됐다. 이 단계가 남긴 개념 메모도 분명했다. 실시간 서버에서 중요한 건 thread 수보다 state transition을 어디서 직렬화하느냐다.

## Session 3 — server orchestration과 persistence를 붙였다
먼저 붙든 질문은 "게임 서버 설명 가능성은 결국 room lifecycle과 repository contract가 분리돼 있느냐에 달렸다"였다. 그래서 작업 단위도 `cpp/src/arena_server.cpp`, `cpp/src/repository.cpp`, `docs/concepts/persistence.md`, `docs/concepts/architecture.md`처럼 작게 잘랐다. 실제 조치는 TcpSession, RoomContext, UDP datagram dispatch, sqlite repository initialization/login/result save를 연결했다.
이 구간의 기준 명령은 `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem run-server`였고, 여기서 확인한 신호는 다음과 같았다. login/create profile, room update, match result persistence가 하나의 run-server surface로 이어졌다. 이 단계가 남긴 개념 메모도 분명했다. room/session/persistence 경계를 분리하는 감각.

## Session 4 — bot demo와 smoke harness로 전체 시스템을 닫았다
먼저 붙든 질문은 "capstone은 단일 unit test보다 서로 다른 실행 entrypoint를 묶은 smoke contract가 필요하다"였다. 그래서 작업 단위도 `cpp/tests/test_protocol.cpp`, `cpp/tests/test_state.cpp`, `cpp/tests/test_repository.cpp`, `problem/script/integration_test.py`, `problem/script/load_smoke_test.py`, `cpp/src/arena_bot.cpp`, `cpp/src/arena_loadtest.cpp`처럼 작게 잘랐다. 실제 조치는 CTest와 Python integration/load harness, bot client binaries를 canonical `make test`에 묶었다.
이 구간의 기준 명령은 `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test`였고, 여기서 확인한 신호는 다음과 같았다. CTest 3/3 PASS + integration_test ok + load_smoke_test ok. 이 단계가 남긴 개념 메모도 분명했다. 설명 가능한 capstone은 demo와 verification까지 source tree 안에 포함될 때 완성된다는 감각.

## Verification and Boundaries
이번 rewrite에서도 `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test`를 다시 실행해 CTest 3/3 PASS + integration_test ok + load_smoke_test ok 결과를 확인했다. 글은 결과 자랑으로 끝내지 않고, 지금 남아 있는 범위를 아래처럼 고정한다.
- production auth, TLS, anti-cheat, spectator, sharding, NAT traversal은 범위 밖입니다.
- `UDP_BIND nonce` 검증은 최소 수준입니다.
- snapshot은 delta compression 없이 full-state 전송입니다.
- GUI client 대신 `arena_bot`, `arena_loadtest`로 검증합니다.
