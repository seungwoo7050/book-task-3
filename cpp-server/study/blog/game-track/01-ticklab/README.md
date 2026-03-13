# ticklab blog

이 디렉터리는 `ticklab`을 `source-first` 방식으로 다시 읽는 프로젝트 단위 blog 시리즈다. chronology는 프로젝트 README, `problem/README.md`, `cpp/README.md`, `cpp/Makefile`, `cpp/include/inc/MatchEngine.hpp`, `cpp/src/MatchEngine.cpp`, `cpp/tests/test_ticklab.cpp`, `problem/data/arena-transcript.txt`를 기준으로 복원했다.

## source set

- [../../../game-track/01-ticklab/README.md](../../../game-track/01-ticklab/README.md)
- [../../../game-track/01-ticklab/problem/README.md](../../../game-track/01-ticklab/problem/README.md)
- [../../../game-track/01-ticklab/problem/data/arena-transcript.txt](../../../game-track/01-ticklab/problem/data/arena-transcript.txt)
- [../../../game-track/01-ticklab/cpp/README.md](../../../game-track/01-ticklab/cpp/README.md)
- [../../../game-track/01-ticklab/cpp/Makefile](../../../game-track/01-ticklab/cpp/Makefile)
- [../../../game-track/01-ticklab/cpp/include/inc/MatchEngine.hpp](../../../game-track/01-ticklab/cpp/include/inc/MatchEngine.hpp)
- [../../../game-track/01-ticklab/cpp/src/MatchEngine.cpp](../../../game-track/01-ticklab/cpp/src/MatchEngine.cpp)
- [../../../game-track/01-ticklab/cpp/tests/test_ticklab.cpp](../../../game-track/01-ticklab/cpp/tests/test_ticklab.cpp)

## 읽는 순서

1. [00-series-map.md](00-series-map.md)
2. [10-chronology-engine-surface-and-room-phases.md](10-chronology-engine-surface-and-room-phases.md)
3. [20-chronology-input-ticks-and-projectiles.md](20-chronology-input-ticks-and-projectiles.md)
4. [30-chronology-rejoin-timeout-and-verification.md](30-chronology-rejoin-timeout-and-verification.md)
5. [../../../game-track/01-ticklab/README.md](../../../game-track/01-ticklab/README.md)

## 검증 진입점

```bash
cd ../../../game-track/01-ticklab/cpp
make clean && make test
```

## chronology 메모

- `ticklab`은 network 없는 headless engine lab이라 chronology도 API surface -> tick processing -> reconnect/verification 순으로 분리했다.
- `arena-transcript.txt`가 실제 chronology의 중요한 증거라서 source set에 포함했다.
- `2026-03-11`은 현재 README의 `verified` surface와 test pass string이 고정된 날짜 앵커다.

