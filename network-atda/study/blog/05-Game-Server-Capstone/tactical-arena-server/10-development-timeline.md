# Tactical Arena Server development timeline

`Tactical Arena Server`를 읽을 때 먼저 잡아야 하는 것은 기능 목록이 아니라, 어디서부터 구현이나 분석이 무거워졌는가이다.

그래서 이 문서는 문제 문서, 핵심 파일, 테스트, CLI 출력만 남기고 나머지 군더더기는 걷어 냈다.

## 구현 순서 한눈에 보기

1. `study/05-Game-Server-Capstone/tactical-arena-server/problem`의 문제 문서와 실행 target으로 출발점을 고정했다.
2. `study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/state.cpp`의 핵심 구간에서 동작 규칙을 설명할 수 있는 최소 앵커를 골랐다.
3. `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test`와 테스트/verify 파일을 연결해 통과 신호와 남은 경계를 정리했다.

## 1. 서버 표면과 실행 경로를 먼저 고정하기

이 단계에서는 구현 세부로 바로 내려가지 않았다. 먼저 어떤 파일이 진입점이고 어떤 명령이 검증 기준인지 고정하는 일이 더 급했다.

- 당시 목표: `Tactical Arena Server`를 읽는 출발점과 성공 기준을 고정한다.
- 실제 진행: `problem/README.md`와 `problem/Makefile`을 먼저 확인한 뒤, `parse_control_line`가 있는 파일로 내려갔다.
- 검증 신호: `make help`에 보이는 target만으로도 이 프로젝트가 어떤 명령으로 열리고 닫히는지 설명할 수 있었다.
- 새로 배운 것: line-based TCP control protocol과 binary UDP packet을 함께 설계하는 방법

핵심 코드/trace:

```cpp
std::optional<ControlMessage> parse_control_line(const std::string& raw_line) {
    std::string line = trim_copy(raw_line);
    if (line.empty()) {
        return std::nullopt;
    }

    std::istringstream stream(line);
    ControlMessage message;
    if (!(stream >> message.verb)) {
        return std::nullopt;
```

왜 이 코드가 중요했는가:

문제 사양을 읽은 뒤 바로 이 지점으로 내려오면, 말로 적힌 요구가 실제 파일 구조와 어떻게 만나는지 곧바로 보인다.

CLI:

```bash
$ make -C study/05-Game-Server-Capstone/tactical-arena-server/problem help
  configure        Configure the CMake build directory
  build            Build the project binaries
  test             Run CTest, integration checks, and load smoke
  run-server       Run the arena server with default local ports
  run-bot-demo     Launch a short local demo with two bots
```

## 2. control protocol, match step, persistence를 같은 서버 흐름으로 묶기

중간 단계의 핵심은 '무엇을 만들었나'보다 '어느 줄에서 규칙이 드러나는가'를 잡는 일이었다.

- 당시 목표: `C++20 + Boost.Asio + SQLite + CMake/CTest 기반으로 구현한 2~4인 authoritative tactical arena server입니다.`를 실제 근거에 붙인다.
- 실제 진행: `MatchState::step` 주변을 중심으로 symbol이나 trace 결과를 다시 좁혀 읽었다.
- 검증 신호: 짧은 `rg`/filter 출력만으로도 어느 줄이 설명의 중심인지 바로 드러났다.
- 새로 배운 것: room 단위 상태를 strand로 직렬화하는 authoritative simulation 구조

핵심 코드/trace:

```cpp
std::optional<MatchResult> MatchState::step(std::uint64_t now_ms) {
    if (finished_) {
        return std::nullopt;
    }

    const auto delta_ms = std::max<std::uint64_t>(1, now_ms - last_step_ms_);
    const auto dt_seconds = static_cast<float>(delta_ms) / 1000.0F;
    last_step_ms_ = now_ms;
    ++server_tick_;
```

왜 이 코드가 중요했는가:

핵심은 함수 이름 자체가 아니라, 이 줄 주변에서 어떤 입력이 어떤 결과로 바뀌는지가 한 번에 드러난다는 점이다.

CLI:

```bash
$ rg -n -e 'parse_control_line' -e 'MatchState::step' -e 'record_match' -e 'handle_line' 'study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_bot.cpp' 'study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_loadtest.cpp' 'study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_server.cpp' 'study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/protocol.cpp' 'study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/repository.cpp' 'study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/state.cpp' 'study/05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_protocol.cpp' 'study/05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_repository.cpp' 'study/05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_state.cpp'
study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/repository.cpp:159:void SqliteRepository::record_match(
study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/protocol.cpp:65:std::optional<ControlMessage> parse_control_line(const std::string& raw_line) {
study/05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_protocol.cpp:20:    const auto parsed = parse_control_line("LOGIN name=alpha");
study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_loadtest.cpp:129:    auto login = arena::parse_control_line(read_line(tcp_socket, buffer));
study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_loadtest.cpp:147:            const auto list = arena::parse_control_line(read_line(tcp_socket, buffer));
study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_loadtest.cpp:171:        const auto message = arena::parse_control_line(read_line(tcp_socket, buffer));
```

## 3. 통합 검증과 남은 범위를 정리하기

마지막 단계에서는 단순히 테스트가 통과했다는 사실만 적지 않으려고 했다. 어디까지 확인됐고 무엇이 아직 범위 밖인지 같이 남겨야 글이 정직해진다.

- 당시 목표: 검증 결과와 남은 경계를 함께 정리한다.
- 실제 진행: `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test`를 다시 실행하고, `def scenario_full_match`가 남아 있는 파일을 본문 마지막 근거로 삼았다.
- 검증 신호: 현재 공개 답안이 재현된다는 출력과, README limitation이 동시에 확인됐다.
- 새로 배운 것: reconnect window, forfeit, fixed tick, respawn 같은 게임 서버 상태 전이

핵심 코드/trace:

```python
def scenario_full_match(build_dir: Path) -> None:
    with running_server(build_dir, match_duration_ms=2500, resume_window_ms=500) as ctx:
        host_proc = subprocess.Popen(
            [
                str(build_dir / "arena_bot"),
                "--host", "127.0.0.1",
                "--tcp-port", str(ctx["tcp_port"]),
                "--mode", "scripted",
                "--role", "host",
                "--name", "alpha",
```

왜 이 코드가 중요했는가:

마지막에 이 파일을 남겨 두는 이유는, 이 프로젝트가 실제로 무엇을 통과해야 끝나는지 가장 직접적으로 보여 주기 때문이다.

CLI:

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

## 남은 경계

- production auth, TLS, anti-cheat, spectator, sharding, NAT traversal은 범위 밖입니다.
- `UDP_BIND nonce` 검증은 최소 수준입니다.
- snapshot은 delta compression 없이 full-state 전송입니다.
- GUI client 대신 `arena_bot`, `arena_loadtest`로 검증합니다.
