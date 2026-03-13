# Tactical Arena Server 개발 타임라인 1

## Day 1 — build 계약, protocol wire 포맷

### Session 1

- 목표: capstone을 "게임 서버"가 아니라 "재현 가능한 계약 집합"으로 읽기 시작한다.
- 진행: `problem/Makefile`을 먼저 열었다. `configure`, `build`, `test`, `run-server`, `run-bot-demo`, `load-test` 타깃이 있고, `test`는 C++ CTest, Python integration, Python load smoke 세 가지를 순서대로 실행한다.
- 이슈: 처음에는 `arena_server.cpp`를 바로 열고 싶었다. 하지만 서버 진입점을 먼저 보면 protocol과 state의 계약을 알기 전에 이벤트 루프 코드를 읽게 되어 전체 구조가 거꾸로 보인다.
- 판단: build & test 타깃이 강제하는 순서 — "protocol → state → repository, 그 다음 server" — 가 이 capstone을 읽는 올바른 순서라는 결론을 먼저 세웠다.

```bash
$ make -C study/05-Game-Server-Capstone/tactical-arena-server/problem configure
-- The CXX compiler identification is AppleClang ...
-- Build files have been written to: .../cpp/build

$ make -C study/05-Game-Server-Capstone/tactical-arena-server/problem build
[ 14%] Building CXX object ...
[100%] Linked CXX executable arena_server
```

핵심 Makefile 구조:

```make
test: build
	ctest --test-dir $(BUILD_DIR) --output-on-failure
	$(PYTHON) script/integration_test.py $(BUILD_DIR)
	$(PYTHON) script/load_smoke_test.py $(BUILD_DIR)
```

- 메모: 이 Makefile 세 줄이 capstone의 목표를 명시한다. "실행된다"가 아니라 "CTest + integration + load smoke가 모두 통과한다"가 기준이다.

### Session 2

- 목표: TCP control channel의 text protocol과 UDP binary packet format을 테스트 코드 수준에서 먼저 고정한다.
- 진행: `test_protocol.cpp`를 읽었다. `parse_control_line("LOGIN name=alpha")`가 `verb="LOGIN"`, `fields["name"]="alpha"`를 리턴하는지, `InputPacket`을 encode → decode하면 `sequence`와 `aim_x`가 살아남는지, `SnapshotPacket` 안의 두 번째 entity `player_id`와 `alive`가 일치하는지 순서대로 확인한다.
- 이슈: UDP binary packet을 보기 전에 floating-point를 big-endian으로 직렬화하는 방법이 궁금했다. `protocol.cpp`를 보니 `std::bit_cast<std::uint32_t>(value)`로 float bit-pattern을 그대로 재해석한 뒤 `append_be`로 4바이트를 내보낸다.
- 이슈 2: control line parser에서 `token.find('=')`가 `npos`이거나 0이거나 `size()-1`이면 `nullopt`를 리턴한다. 이 세 가지 경계가 잘못된 login 시도를 모두 막는다.

핵심 코드:

```cpp
// control line 파싱
while (stream >> token) {
    const auto pos = token.find('=');
    if (pos == std::string::npos || pos == 0 || pos == token.size() - 1) {
        return std::nullopt;
    }
    message.fields[token.substr(0, pos)] = token.substr(pos + 1);
}

// float big-endian 직렬화
void append_float(std::vector<std::uint8_t>& output, float value) {
    append_be(output, std::bit_cast<std::uint32_t>(value));
}
```

### Session 3

- 목표: C++ 단위 테스트를 실제로 실행하고, protocol round-trip이 통과하는지 확인한다.
- 진행: CMake build 후 `ctest --output-on-failure`로 세 단위 테스트를 돌렸다.

```bash
$ ctest --test-dir study/05-Game-Server-Capstone/tactical-arena-server/cpp/build \
    --output-on-failure
Test project .../cpp/build
    Start 1: test_protocol
1/3 Test #1: test_protocol .............. Passed    0.00 sec
    Start 2: test_state
2/3 Test #2: test_state ................. Passed    0.00 sec
    Start 3: test_repository
3/3 Test #3: test_repository ............ Passed    0.01 sec

100% tests passed, 0 tests failed out of 3
```

- 정리:
  - `parse_control_line()`은 `verb key=value...` 공백 구분 형식의 입구다. verb가 없거나 field 형식이 틀리면 `nullopt`를 리턴해 상위 handler가 즉시 연결을 끊을 수 있다.
  - binary packet은 float를 `std::bit_cast`로 `uint32_t`에 재해석해 big-endian으로 보낸다. 이 방식은 플랫폼 float 표현을 가정하지 않아도 round-trip이 보장된다.
  - CTest 3개 통과가 이후 integration / load smoke test의 전제 조건이다.
