# Tactical Arena Server 시리즈 지도

이 프로젝트를 한 줄로: TCP control channel과 UDP realtime binary packet을 분리하고, authoritative fixed-tick simulation에 SQLite persistence까지 붙여 `make test` 한 번으로 단위·통합·부하 검증을 모두 재현하는 C++20 게임 서버를 만든 기록.

## 파일 구성

| 파일 | 역할 |
|------|------|
| `problem/code/control-protocol.txt` | TCP control line 사양 |
| `problem/data/schema.sql` | SQLite 스키마 |
| `cpp/src/protocol.cpp` | wire 포맷 encode/decode |
| `cpp/src/state.cpp` | authoritative simulation |
| `cpp/src/repository.cpp` | SQLite persistence |
| `cpp/src/arena_server.cpp` | TCP/UDP 이벤트 루프 |
| `cpp/tests/test_protocol.cpp` | protocol round-trip 검증 |
| `cpp/tests/test_state.cpp` | simulation 규칙 검증 |
| `cpp/tests/test_repository.cpp` | profile/match history 검증 |
| `problem/script/integration_test.py` | 실제 프로세스 시나리오 |
| `problem/script/load_smoke_test.py` | 2 rooms / 8 bots 부하 확인 |
| `problem/Makefile` | configure / build / test / run-server / run-bot-demo / load-test |

## canonical verification

```bash
# 빌드 + C++ 단위 + Python 통합 + 부하 스모크
make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test

# 서버 단독 실행
make -C study/05-Game-Server-Capstone/tactical-arena-server/problem run-server

# 봇 데모
make -C study/05-Game-Server-Capstone/tactical-arena-server/problem run-bot-demo

# 부하 스모크 단독
make -C study/05-Game-Server-Capstone/tactical-arena-server/problem load-test
```

## 이 시리즈에서 따라갈 질문

1. `parse_control_line()`은 `verb key=value ...` 형식을 어떻게 파싱하며, 이 parser가 전체 control flow의 입구가 되는 이유는?
2. `submit_input()`이 "더 최신 sequence만 반영한다"는 규칙이 authoritative server와 relay의 차이를 어떻게 만드는가?
3. `MatchState::step()`의 fixed-tick 진행에서 forfeit / respawn / projectile 처리 순서가 중요한 이유는?
4. `SqliteRepository::record_match()`의 transaction 경계가 없으면 무슨 조건에서 데이터가 빠지는가?
5. integration harness의 `running_server()` context manager와 `RESUME` 시나리오는 `resume_window_ms`를 어떻게 실제 프로세스로 검증하는가?

## 글 파일

- [10-development-timeline.md](10-development-timeline.md): build 계약, protocol wire 포맷 고정
- [20-development-timeline.md](20-development-timeline.md): simulation 규칙, server 이벤트 루프, persistence
- [30-development-timeline.md](30-development-timeline.md): 통합 시나리오, 부하 스모크, bot demo

## 문제 범위
- TCP control channel과 UDP realtime channel을 분리한 authoritative arena server를 만든다.
- room/lobby/login/resume, fixed-tick simulation, SQLite persistence, bot/load verification을 한 저장소 안에 묶는다.
- 단순 demo가 아니라 `make test` 한 번으로 unit + integration + load smoke가 재현돼야 한다.

## 제공물과 사용자 작성 답안
- 제공물: `problem/code/control-protocol.txt`, `problem/data/schema.sql`, `problem/data/arena-map.txt`, `problem/script/*.py`
- 사용자 작성 답안: `cpp/src/*.cpp`, `cpp/tests/*.cpp`
- 빌드/실행 진입점: `problem/Makefile`, `cpp/CMakeLists.txt`

## canonical verification
- configure/build/test: `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test`
- 서버 실행: `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem run-server`
- 봇 데모: `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem run-bot-demo`
- 부하 스모크: `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem load-test`

## 이 시리즈에서 따라갈 질문
- 제어 프로토콜과 UDP packet wire format은 어디서 고정되는가
- authoritative state와 reconnect/forfeit는 어떤 테스트가 받쳐 주는가
- SQLite persistence와 integration/load harness는 어떤 순서로 묶이는가

## 글 파일
- [`10-development-timeline.md`](10-development-timeline.md): build, protocol, entrypoint 구간
- [`20-development-timeline.md`](20-development-timeline.md): simulation, reconnect, persistence 구간
- [`30-development-timeline.md`](30-development-timeline.md): unit, integration, load smoke, demo 구간
