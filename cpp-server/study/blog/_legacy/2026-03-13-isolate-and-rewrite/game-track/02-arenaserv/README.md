# arenaserv blog

이 디렉터리는 `arenaserv`를 `source-first` 방식으로 다시 읽는 프로젝트 단위 blog 시리즈다. chronology는 프로젝트 README, `problem/README.md`, `cpp/README.md`, `cpp/Makefile`, `cpp/include/inc/Server.hpp`, `cpp/include/inc/EventManager.hpp`, `cpp/src/Server.cpp`, `cpp/src/MatchEngine.cpp`, `cpp/tests/test_arenaserv.py`를 기준으로 복원했다.

## source set

- [../../../game-track/02-arenaserv/README.md](../../../game-track/02-arenaserv/README.md)
- [../../../game-track/02-arenaserv/problem/README.md](../../../game-track/02-arenaserv/problem/README.md)
- [../../../game-track/02-arenaserv/cpp/README.md](../../../game-track/02-arenaserv/cpp/README.md)
- [../../../game-track/02-arenaserv/cpp/Makefile](../../../game-track/02-arenaserv/cpp/Makefile)
- [../../../game-track/02-arenaserv/cpp/include/inc/Server.hpp](../../../game-track/02-arenaserv/cpp/include/inc/Server.hpp)
- [../../../game-track/02-arenaserv/cpp/include/inc/EventManager.hpp](../../../game-track/02-arenaserv/cpp/include/inc/EventManager.hpp)
- [../../../game-track/02-arenaserv/cpp/include/inc/MatchEngine.hpp](../../../game-track/02-arenaserv/cpp/include/inc/MatchEngine.hpp)
- [../../../game-track/02-arenaserv/cpp/src/Server.cpp](../../../game-track/02-arenaserv/cpp/src/Server.cpp)
- [../../../game-track/02-arenaserv/cpp/src/MatchEngine.cpp](../../../game-track/02-arenaserv/cpp/src/MatchEngine.cpp)
- [../../../game-track/02-arenaserv/cpp/tests/test_arenaserv.py](../../../game-track/02-arenaserv/cpp/tests/test_arenaserv.py)

## 읽는 순서

1. [00-series-map.md](00-series-map.md)
2. [10-chronology-server-surface-and-session-handshake.md](10-chronology-server-surface-and-session-handshake.md)
3. [20-chronology-queue-ready-and-engine-bridge.md](20-chronology-queue-ready-and-engine-bridge.md)
4. [30-chronology-input-rejoin-and-room-events.md](30-chronology-input-rejoin-and-room-events.md)
5. [40-chronology-multi-client-verification-and-boundaries.md](40-chronology-multi-client-verification-and-boundaries.md)
6. [../../../game-track/02-arenaserv/README.md](../../../game-track/02-arenaserv/README.md)

## 검증 진입점

```bash
cd ../../../game-track/02-arenaserv/cpp
make clean && make test
```

## chronology 메모

- `arenaserv`는 `eventlab` runtime과 `ticklab` engine을 다시 합치는 capstone이므로, chronology도 command surface -> engine bridge -> rejoin/input path -> multi-client smoke verification 순서로 나눴다.
- `2026-03-11`은 현재 `verified` surface를 고정한 날짜 앵커다.
- 본문은 별도 노트 계층 없이 source set과 smoke test contract만으로 재구성했다.
