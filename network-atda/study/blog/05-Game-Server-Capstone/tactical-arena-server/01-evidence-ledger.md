# Tactical Arena Server evidence ledger

이 문서는 긴 본문을 읽기 전에, 세 단계에서 어떤 판단이 있었는지만 빠르게 붙들기 위한 압축본이다.

## Phase 1. 서버 표면과 실행 경로를 먼저 고정하기

- 당시 목표: `Tactical Arena Server`를 어디서부터 읽어야 하는지 고정한다.
- 핵심 변경 단위: `study/05-Game-Server-Capstone/tactical-arena-server/problem/README.md`, `study/05-Game-Server-Capstone/tactical-arena-server/problem/Makefile`, `study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/protocol.cpp`
- 무슨 판단을 했는가: 문제 설명보다 실행 표면을 먼저 잡아야 뒤 설명이 흔들리지 않는다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/05-Game-Server-Capstone/tactical-arena-server/problem help
  configure        Configure the CMake build directory
  build            Build the project binaries
  test             Run CTest, integration checks, and load smoke
  run-server       Run the arena server with default local ports
  run-bot-demo     Launch a short local demo with two bots
```
- 검증 신호:
  - `make help`만 봐도 이 프로젝트가 어떤 target으로 열리고 닫히는지 드러난다.
  - 이 단계에서의 역할: 앞선 트랙에서 배운 TCP/UDP, 신뢰 전송, 진단 도구, deterministic test 패턴을 하나의 서버 설계로 통합해 설명하는 단계가 필요했기 때문에 추가한 capstone입니다.
- 핵심 코드/trace 앵커: `study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/protocol.cpp`의 `parse_control_line`
- 다음으로 넘어간 이유: 이제 어디를 읽어야 할지 정해졌으니, 실제로 판단이 몰린 함수나 trace section으로 내려갈 수 있었다.

## Phase 2. control protocol, match step, persistence를 같은 서버 흐름으로 묶기

- 당시 목표: `C++20 + Boost.Asio + SQLite + CMake/CTest 기반으로 구현한 2~4인 authoritative tactical arena server입니다.`를 실제 코드나 trace 근거에 붙여 본다.
- 핵심 변경 단위: `study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/state.cpp`
- 무슨 판단을 했는가: 중심 규칙은 넓게 흩어져 있지 않고, 실제 분기나 frame evidence가 모이는 지점에 있다고 봤다.
- 실행한 CLI:

```bash
$ rg -n -e 'parse_control_line' -e 'MatchState::step' -e 'record_match' -e 'handle_line' 'study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_bot.cpp' 'study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_loadtest.cpp' 'study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_server.cpp' 'study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/protocol.cpp' 'study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/repository.cpp' 'study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/state.cpp' 'study/05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_protocol.cpp' 'study/05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_repository.cpp' 'study/05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_state.cpp'
study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/repository.cpp:159:void SqliteRepository::record_match(
study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/protocol.cpp:65:std::optional<ControlMessage> parse_control_line(const std::string& raw_line) {
study/05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_protocol.cpp:20:    const auto parsed = parse_control_line("LOGIN name=alpha");
study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_loadtest.cpp:129:    auto login = arena::parse_control_line(read_line(tcp_socket, buffer));
study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_loadtest.cpp:147:            const auto list = arena::parse_control_line(read_line(tcp_socket, buffer));
study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_loadtest.cpp:171:        const auto message = arena::parse_control_line(read_line(tcp_socket, buffer));
```
- 검증 신호:
  - 이 출력만으로도 `MatchState::step` 주변이 설명의 중심축이라는 점이 드러난다.
  - room 단위 상태를 strand로 직렬화하는 authoritative simulation 구조
- 핵심 코드/trace 앵커: `study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/state.cpp`의 `MatchState::step`
- 다음으로 넘어간 이유: 중심 규칙을 잡은 뒤에는, 이 구현이나 분석이 실제로 무엇으로 닫히는지만 확인하면 됐다.

## Phase 3. 통합 검증과 남은 범위를 정리하기

- 당시 목표: 통과 신호와 남은 범위를 한 번에 정리한다.
- 핵심 변경 단위: `study/05-Game-Server-Capstone/tactical-arena-server/problem/script/integration_test.py`, `problem/script/`, `docs/`
- 무슨 판단을 했는가: 검증 출력이 좋게 나와도 README limitation을 그대로 남겨야 범위가 정확해진다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test
-- Build files have been written to: /Users/woopinbell/work/book-task-3/network-atda/study/05-Game-Server-Capstone/tactical-arena-server/cpp/build
gmake[1]: Entering directory '/Users/woopinbell/work/book-task-3/network-atda/study/05-Game-Server-Capstone/tactical-arena-server/cpp/build'
[100%] Built target test_repository
gmake[1]: Leaving directory '/Users/woopinbell/work/book-task-3/network-atda/study/05-Game-Server-Capstone/tactical-arena-server/cpp/build'
python3 script/integration_test.py ../cpp/build
integration_test ok
python3 script/load_smoke_test.py ../cpp/build
load_smoke_test ok
```
- 검증 신호:
  - `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test`가 현재 공개 답안을 다시 재현해 준다.
  - production auth, TLS, anti-cheat, spectator, sharding, NAT traversal은 범위 밖입니다.
- 핵심 코드/trace 앵커: `study/05-Game-Server-Capstone/tactical-arena-server/problem/script/integration_test.py`의 `def scenario_full_match`
- 다음으로 넘어간 이유: 통과 신호와 경계가 모두 적혔으니, 긴 본문에서는 각 단계를 더 사람 읽기 좋게 풀어 쓰면 된다.
