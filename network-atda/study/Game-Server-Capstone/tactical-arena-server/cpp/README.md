# C++ 구현 안내

    이 디렉터리는 `Tactical Arena Server`의 공개 구현을 담습니다. 현재 저장소의 canonical 검증을 통과하는 범위를 기준으로 코드를 읽을 수 있게 정리합니다.

    ## 어디서부터 읽으면 좋은가

    1. `cpp/src/arena_bot.cpp` - 핵심 구현 진입점입니다.
2. `cpp/src/arena_loadtest.cpp` - 핵심 구현 진입점입니다.
3. `cpp/src/arena_server.cpp` - 핵심 구현 진입점입니다.
4. `cpp/src/protocol.cpp` - 핵심 구현 진입점입니다.
5. `cpp/src/repository.cpp` - 핵심 구현 진입점입니다.
6. `cpp/src/state.cpp` - 핵심 구현 진입점입니다.
7. `cpp/tests/test_protocol.cpp` - 검증 의도와 보조 테스트를 확인합니다.
8. `cpp/tests/test_repository.cpp` - 검증 의도와 보조 테스트를 확인합니다.
9. `cpp/tests/test_state.cpp` - 검증 의도와 보조 테스트를 확인합니다.

    ## 기준 명령

    - 서버 실행: `make -C study/Game-Server-Capstone/tactical-arena-server/problem run-server`
- bot 데모: `make -C study/Game-Server-Capstone/tactical-arena-server/problem run-bot-demo`
- load smoke: `make -C study/Game-Server-Capstone/tactical-arena-server/problem load-test`
- 정식 검증: `make -C study/Game-Server-Capstone/tactical-arena-server/problem test`
- 구현 위치: `cpp/src/`
- 테스트 위치: `cpp/tests/`

    ## 현재 범위

    `C++20 + Boost.Asio + SQLite + CMake/CTest` 기반으로 구현한 `2~4인 authoritative tactical arena server`다.

    ## 남은 약점

    - 현재 한계는 프로젝트 README를 기준으로 정리합니다.
