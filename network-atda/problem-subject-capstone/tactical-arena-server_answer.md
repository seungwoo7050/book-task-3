# tactical-arena-server 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 기능 통합: TCP/UDP 분리, authoritative simulation, reconnect, persistence가 하나의 서버로 통합됩니다, 재현성: make test 한 번으로 unit + integration + load smoke를 재현합니다, 설명 가능성: 문제 정의, 설계, 검증, 한계를 문서로 설명할 수 있습니다를 한 흐름으로 설명하고 검증한다. 핵심은 `send_line`와 `parse_args`, `trace_enabled` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 기능 통합: TCP/UDP 분리, authoritative simulation, reconnect, persistence가 하나의 서버로 통합됩니다.
- 재현성: make test 한 번으로 unit + integration + load smoke를 재현합니다.
- 설명 가능성: 문제 정의, 설계, 검증, 한계를 문서로 설명할 수 있습니다.
- 첫 진입점은 `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_bot.cpp`이고, 여기서 `send_line`와 `parse_args` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_bot.cpp`: `send_line`, `parse_args`, `trace_enabled`, `trace`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_loadtest.cpp`: `send_line`, `parse_args`, `run_bot_worker`, `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_server.cpp`: `parse_args`, `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/protocol.cpp`: `append_be`, `append_float`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/repository.cpp`: `read_profile_row`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_protocol.cpp`: `expect`, `main`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_repository.cpp`: `expect`, `main`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_state.cpp`: `expect`, `main`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_bot.cpp`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `expect` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make -C /Users/woopinbell/work/book-task-3/network-atda/study/05-Game-Server-Capstone/tactical-arena-server/problem test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/network-atda/study/05-Game-Server-Capstone/tactical-arena-server/problem test
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `expect`와 `main`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/network-atda/study/05-Game-Server-Capstone/tactical-arena-server/problem test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_bot.cpp`
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_loadtest.cpp`
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_server.cpp`
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/protocol.cpp`
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/repository.cpp`
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_protocol.cpp`
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_repository.cpp`
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_state.cpp`
- `../study/05-Game-Server-Capstone/tactical-arena-server/problem/code/control-protocol.txt`
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/CMakeLists.txt`
