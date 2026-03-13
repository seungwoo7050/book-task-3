    # Series Map — Tactical Arena Server

    | 항목 | 내용 |
    | :--- | :--- |
    | 대상 프로젝트 | `05-Game-Server-Capstone/tactical-arena-server` |
    | 문제 배경 | 이 저장소에서 누적한 네트워크 학습을 하나의 설명 가능한 서버로 묶기 위해 직접 설계한 신규 capstone 프로젝트 |
    | 공개 답안 표면 | `cpp/src/arena_bot.cpp`, `cpp/src/arena_loadtest.cpp`, `cpp/src/arena_server.cpp`, `cpp/src/protocol.cpp`, `cpp/src/repository.cpp`, `cpp/src/state.cpp` |
    | 정식 검증 | `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test` |
    | rewrite 방식 | `isolate-and-rewrite` |
    | legacy 보관 위치 | `_legacy/2026-03-13-isolate-and-rewrite/05-Game-Server-Capstone/tactical-arena-server` |

    ## 프로젝트 경계
    - 이 프로젝트는 TCP control, UDP gameplay, fixed tick state, SQLite persistence, bot/load smoke를 하나로 엮는 authoritative game server를 독립 문제로 다룬다.
    - `README.md`, `problem/`, `cpp/`, `docs/`가 한 폴더 아래에 닫혀 있어 다른 lab 없이도 범위 설명과 재검증이 가능하다.
    - canonical entrypoint는 `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test`이며, 이번 재실행에서도 CTest 3/3 PASS + integration_test ok + load_smoke_test ok 신호를 확인했다.

    ## 이번 rewrite의 입력 표면
    - `problem/code/control-protocol.txt`: TCP/UDP wire format 요약
- `problem/data/schema.sql`: SQLite schema 참조본
- `problem/data/arena-map.txt`: 고정 arena 규칙 설명
- `problem/script/integration_test.py`: reconnect, forfeit, UDP ordering integration harness
- `problem/script/load_smoke_test.py`: 8 bots / 2 rooms smoke harness
    - 소스 파일: `cpp/src/arena_bot.cpp`, `cpp/src/arena_loadtest.cpp`, `cpp/src/arena_server.cpp`, `cpp/src/protocol.cpp`, `cpp/src/repository.cpp`, `cpp/src/state.cpp`
    - 테스트 파일: `cpp/tests/test_protocol.cpp`, `cpp/tests/test_repository.cpp`, `cpp/tests/test_state.cpp`
    - `docs/concepts/architecture.md` - Architecture
- `docs/concepts/load-testing.md` - Load Testing
- `docs/concepts/persistence.md` - Persistence
- `docs/concepts/protocol.md` - Protocol

    ## 이번 rewrite에서 제외한 입력
    - 기존 `study/blog/05-Game-Server-Capstone/tactical-arena-server` 초안
    - `notion/`, `notion-archive/` 계열 노트
    - track 단위 회고나 다른 프로젝트 blog

    ## 이번 글에서 꼭 복원할 장면
    - Session 1: TCP control과 UDP gameplay 프로토콜부터 닫았다
- Session 2: authoritative simulation을 state layer로 분리했다
- Session 3: server orchestration과 persistence를 붙였다
- Session 4: bot demo와 smoke harness로 전체 시스템을 닫았다

    ## 이번 프로젝트가 남긴 학습 포인트
    - line-based TCP control protocol과 binary UDP packet을 함께 설계하는 방법
- room 단위 상태를 strand로 직렬화하는 authoritative simulation 구조
- reconnect window, forfeit, fixed tick, respawn 같은 게임 서버 상태 전이
- SQLite persistence를 deterministic test와 연결하는 방법
- bot demo와 load smoke를 발표 자료로 묶는 방법
