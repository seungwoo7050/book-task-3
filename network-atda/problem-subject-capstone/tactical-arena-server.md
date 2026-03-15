# tactical-arena-server 문제지

## 왜 중요한가

이 문서는 Tactical Arena Server를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 구현 세부와 공개 구현 경로는 상위 프로젝트 README가 연결하는 경로를 따라가면 됩니다.

## 목표

시작 위치의 구현을 완성해 기능 통합: TCP/UDP 분리, authoritative simulation, reconnect, persistence가 하나의 서버로 통합됩니다, 재현성: make test 한 번으로 unit + integration + load smoke를 재현합니다, 설명 가능성: 문제 정의, 설계, 검증, 한계를 문서로 설명할 수 있습니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_bot.cpp`
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_loadtest.cpp`
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_server.cpp`
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/protocol.cpp`
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_protocol.cpp`
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_repository.cpp`
- `../study/05-Game-Server-Capstone/tactical-arena-server/problem/code/control-protocol.txt`
- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/CMakeLists.txt`

## starter code / 입력 계약

- `../study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_bot.cpp`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 기능 통합: TCP/UDP 분리, authoritative simulation, reconnect, persistence가 하나의 서버로 통합됩니다.
- 재현성: make test 한 번으로 unit + integration + load smoke를 재현합니다.
- 설명 가능성: 문제 정의, 설계, 검증, 한계를 문서로 설명할 수 있습니다.
- 발표 가능성: bot demo와 캡처 자료를 바로 재생성할 수 있습니다.
- 코드 품질: CMake/CTest 기반의 읽기 쉬운 C++ 구조를 유지합니다.

## 제외 범위

- `../study/05-Game-Server-Capstone/tactical-arena-server/problem/code/control-protocol.txt` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `send_line`와 `parse_args`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `expect`와 `main`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/05-Game-Server-Capstone/tactical-arena-server/problem/code/control-protocol.txt` 등 fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/network-atda/study/05-Game-Server-Capstone/tactical-arena-server/problem test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/network-atda/study/05-Game-Server-Capstone/tactical-arena-server/problem test
```

- `tactical-arena-server`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`tactical-arena-server_answer.md`](tactical-arena-server_answer.md)에서 확인한다.
