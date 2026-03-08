# C++ 구현 안내

이 디렉터리는 `Tactical Arena Server`의 공개 C++ 구현을 담는다.

## 구성

- `src/arena_server.cpp`
- `src/arena_bot.cpp`
- `src/arena_loadtest.cpp`
- `src/protocol.cpp`
- `src/state.cpp`
- `src/repository.cpp`
- `include/arena/*.hpp`
- `tests/test_protocol.cpp`
- `tests/test_state.cpp`
- `tests/test_repository.cpp`
- `CMakeLists.txt`

## 기준 명령

- configure/build: `cmake -S study/Game-Server-Capstone/tactical-arena-server/cpp -B study/Game-Server-Capstone/tactical-arena-server/cpp/build`
- test: `make -C study/Game-Server-Capstone/tactical-arena-server/problem test`
- bot demo: `make -C study/Game-Server-Capstone/tactical-arena-server/problem run-bot-demo`

## 구현 메모

- 상태: `verified`
- 범위: single-process authoritative session server, bot client, in-process load runner
- 빌드: `C++20 + Boost.Asio headers + SQLite + CMake/CTest`
- 산출물: `arena_server`, `arena_bot`, `arena_loadtest`

## 현재 약점

- UDP endpoint proof는 light-weight nonce arming 수준이다.
- message schema는 hand-written parser라 버전 협상이나 backward compatibility 계층이 없다.
- single-node/local-first 구조라 운영 분산 문제는 다루지 않는다.

## 구현 포인트

- TCP 세션 I/O는 per-session strand로 직렬화한다.
- room/match 진행은 room strand에서만 상태를 수정한다.
- SQLite 공유 연결은 repository 내부 mutex로 직렬화한다.
- load smoke는 외부 프로세스 래퍼가 아니라 in-process bot worker로 구현한다.
