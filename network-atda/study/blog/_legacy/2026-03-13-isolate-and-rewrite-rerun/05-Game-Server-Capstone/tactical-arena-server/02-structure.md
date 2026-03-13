    # Structure Design — Tactical Arena Server

    ## opening
    - 시작 질문: 이 프로젝트를 실제로 어디서부터 만들기 시작했는가.
    - 바로 보여 줄 증거: `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test`와 ``cpp/src/protocol.cpp::parse_control_line` and `cpp/src/protocol.cpp::decode_input_packet``.
    - 서술 원칙: 결과 요약보다 Session별 판단 이동을 우선한다.
    - 메모: `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test`가 통과하는 상태를 출발점으로 삼되, 실제 글의 첫 장면은 ``cpp/src/protocol.cpp::parse_control_line` and `cpp/src/protocol.cpp::decode_input_packet``에서 시작한다.

    ## Session 1 — TCP control과 UDP gameplay 프로토콜부터 닫았다
- 다룰 파일/표면: `cpp/src/protocol.cpp`, `docs/concepts/protocol.md`, `problem/code/control-protocol.txt`
- 글에서 먼저 던질 질문: "capstone의 첫 복잡성은 game rule보다 protocol surface가 TCP/UDP 두 채널로 갈라진다는 점이다"
- 꼭 넣을 CLI: `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem run-server`
- 꼭 남길 검증 신호: control command와 UDP input packet을 같은 naming/field 규칙으로 설명할 수 있게 됐다.
- 핵심 전환 문장: capstone에서는 application protocol 설계가 곧 테스트 가능성의 출발점이다.
## Session 2 — authoritative simulation을 state layer로 분리했다
- 다룰 파일/표면: `cpp/src/state.cpp`, `docs/concepts/simulation.md`
- 글에서 먼저 던질 질문: "room strand 안에서 돌아가는 authoritative state는 `step()`이 하나의 truth가 되어야 설명 가능하다"
- 꼭 넣을 CLI: `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem run-bot-demo`
- 꼭 남길 검증 신호: bot demo와 state test가 같은 tick/update 규칙을 공유하게 됐다.
- 핵심 전환 문장: 실시간 서버에서 중요한 건 thread 수보다 state transition을 어디서 직렬화하느냐다.
## Session 3 — server orchestration과 persistence를 붙였다
- 다룰 파일/표면: `cpp/src/arena_server.cpp`, `cpp/src/repository.cpp`, `docs/concepts/persistence.md`, `docs/concepts/architecture.md`
- 글에서 먼저 던질 질문: "게임 서버 설명 가능성은 결국 room lifecycle과 repository contract가 분리돼 있느냐에 달렸다"
- 꼭 넣을 CLI: `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem run-server`
- 꼭 남길 검증 신호: login/create profile, room update, match result persistence가 하나의 run-server surface로 이어졌다.
- 핵심 전환 문장: 네트워크 capstone은 transport보다 room/session/persistence 경계를 얼마나 분리했는지가 유지보수성을 좌우한다.
## Session 4 — bot demo와 smoke harness로 전체 시스템을 닫았다
- 다룰 파일/표면: `cpp/tests/test_protocol.cpp`, `cpp/tests/test_state.cpp`, `cpp/tests/test_repository.cpp`, `problem/script/integration_test.py`, `problem/script/load_smoke_test.py`, `cpp/src/arena_bot.cpp`, `cpp/src/arena_loadtest.cpp`
- 글에서 먼저 던질 질문: "capstone은 단일 unit test보다 서로 다른 실행 entrypoint를 묶은 smoke contract가 필요하다"
- 꼭 넣을 CLI: `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test`
- 꼭 남길 검증 신호: CTest 3/3 PASS + integration_test ok + load_smoke_test ok
- 핵심 전환 문장: 설명 가능한 capstone은 구현만이 아니라 demo와 verification까지 source tree 안에 포함될 때 완성된다.

    ## ending
    - 마지막 단락에서는 현재 한계를 README bullet 그대로 축약해 남긴다.
    - production auth, TLS, anti-cheat, spectator, sharding, NAT traversal은 범위 밖입니다.
- `UDP_BIND nonce` 검증은 최소 수준입니다.
- snapshot은 delta compression 없이 full-state 전송입니다.
- GUI client 대신 `arena_bot`, `arena_loadtest`로 검증합니다.
