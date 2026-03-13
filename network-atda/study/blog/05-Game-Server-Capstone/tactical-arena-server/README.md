# Tactical Arena Server blog

이 디렉터리는 `Tactical Arena Server`를 `strict source-only` 기준으로 다시 읽는 capstone blog 시리즈다. chronology는 `problem/README.md`, `problem/Makefile`, `cpp/src/`, `cpp/tests/`, `problem/script/*.py`를 바탕으로, 일반적인 개발자라면 밟았을 구현 순서를 추론해 세 구간으로 나눠 정리했다.

## source set
- [`../../../05-Game-Server-Capstone/tactical-arena-server/README.md`](../../../05-Game-Server-Capstone/tactical-arena-server/README.md)
- [`../../../05-Game-Server-Capstone/tactical-arena-server/problem/README.md`](../../../05-Game-Server-Capstone/tactical-arena-server/problem/README.md)
- [`../../../05-Game-Server-Capstone/tactical-arena-server/problem/Makefile`](../../../05-Game-Server-Capstone/tactical-arena-server/problem/Makefile)
- [`../../../05-Game-Server-Capstone/tactical-arena-server/cpp/README.md`](../../../05-Game-Server-Capstone/tactical-arena-server/cpp/README.md)
- [`../../../05-Game-Server-Capstone/tactical-arena-server/cpp/src/protocol.cpp`](../../../05-Game-Server-Capstone/tactical-arena-server/cpp/src/protocol.cpp)
- [`../../../05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_server.cpp`](../../../05-Game-Server-Capstone/tactical-arena-server/cpp/src/arena_server.cpp)
- [`../../../05-Game-Server-Capstone/tactical-arena-server/cpp/src/state.cpp`](../../../05-Game-Server-Capstone/tactical-arena-server/cpp/src/state.cpp)
- [`../../../05-Game-Server-Capstone/tactical-arena-server/cpp/src/repository.cpp`](../../../05-Game-Server-Capstone/tactical-arena-server/cpp/src/repository.cpp)
- [`../../../05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_protocol.cpp`](../../../05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_protocol.cpp)
- [`../../../05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_state.cpp`](../../../05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_state.cpp)
- [`../../../05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_repository.cpp`](../../../05-Game-Server-Capstone/tactical-arena-server/cpp/tests/test_repository.cpp)
- [`../../../05-Game-Server-Capstone/tactical-arena-server/problem/script/integration_test.py`](../../../05-Game-Server-Capstone/tactical-arena-server/problem/script/integration_test.py)
- [`../../../05-Game-Server-Capstone/tactical-arena-server/problem/script/load_smoke_test.py`](../../../05-Game-Server-Capstone/tactical-arena-server/problem/script/load_smoke_test.py)

## 읽는 순서
1. [`00-series-map.md`](00-series-map.md)
2. [`10-development-timeline.md`](10-development-timeline.md)
3. [`20-development-timeline.md`](20-development-timeline.md)
4. [`30-development-timeline.md`](30-development-timeline.md)
5. [`../../../05-Game-Server-Capstone/tactical-arena-server/README.md`](../../../05-Game-Server-Capstone/tactical-arena-server/README.md)

## 검증 진입점
- `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test`

## chronology 메모
- capstone은 source set이 넓기 때문에 `build/setup`, `protocol/state`, `integration/verification` 세 구간으로 나눴다.
