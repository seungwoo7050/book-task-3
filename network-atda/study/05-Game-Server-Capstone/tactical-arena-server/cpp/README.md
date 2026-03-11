# C++ 구현 안내

## 이 폴더의 역할
이 디렉터리는 `Tactical Arena Server`의 공개 구현을 담습니다. `problem/`의 제공 자료와 분리된 사용자 작성 답안을 이 폴더에서 확인합니다.

## 먼저 볼 파일
- `cpp/src/arena_bot.cpp` - 핵심 구현 진입점입니다.
- `cpp/src/arena_loadtest.cpp` - 핵심 구현 진입점입니다.
- `cpp/src/arena_server.cpp` - 핵심 구현 진입점입니다.
- `cpp/src/protocol.cpp` - 핵심 구현 진입점입니다.
- `cpp/src/repository.cpp` - 핵심 구현 진입점입니다.
- `cpp/src/state.cpp` - 핵심 구현 진입점입니다.
- `cpp/tests/test_protocol.cpp` - 검증 의도와 보조 테스트를 확인합니다.
- `cpp/tests/test_repository.cpp` - 검증 의도와 보조 테스트를 확인합니다.
- `cpp/tests/test_state.cpp` - 검증 의도와 보조 테스트를 확인합니다.

## 기준 명령
- 검증: `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test`

## 현재 범위
`C++20 + Boost.Asio + SQLite + CMake/CTest` 기반으로 구현한 `2~4인 authoritative tactical arena server`입니다.

## 남은 약점
- production auth, TLS, anti-cheat, spectator, sharding, NAT traversal은 범위 밖입니다.
- `UDP_BIND nonce` 검증은 최소 수준입니다.
- snapshot은 delta compression 없이 full-state 전송입니다.
- GUI client 대신 `arena_bot`, `arena_loadtest`로 검증합니다.
