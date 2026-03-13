# roomlab blog

이 디렉터리는 `roomlab`을 `source-first` 방식으로 다시 읽는 프로젝트 단위 blog 시리즈다. chronology는 프로젝트 README, `problem/README.md`, `cpp/README.md`, `cpp/Makefile`, `cpp/include/inc/Server.hpp`, `cpp/src/Executor.cpp`, `cpp/src/execute_join.cpp`, `cpp/src/Server.cpp`, `cpp/tests/test_roomlab.py`를 기준으로 복원했다.

## source set

- [../../../irc-track/01-roomlab/README.md](../../../irc-track/01-roomlab/README.md)
- [../../../irc-track/01-roomlab/problem/README.md](../../../irc-track/01-roomlab/problem/README.md)
- [../../../irc-track/01-roomlab/cpp/README.md](../../../irc-track/01-roomlab/cpp/README.md)
- [../../../irc-track/01-roomlab/cpp/Makefile](../../../irc-track/01-roomlab/cpp/Makefile)
- [../../../irc-track/01-roomlab/cpp/include/inc/Server.hpp](../../../irc-track/01-roomlab/cpp/include/inc/Server.hpp)
- [../../../irc-track/01-roomlab/cpp/src/Executor.cpp](../../../irc-track/01-roomlab/cpp/src/Executor.cpp)
- [../../../irc-track/01-roomlab/cpp/src/execute_join.cpp](../../../irc-track/01-roomlab/cpp/src/execute_join.cpp)
- [../../../irc-track/01-roomlab/cpp/src/Server.cpp](../../../irc-track/01-roomlab/cpp/src/Server.cpp)
- [../../../irc-track/01-roomlab/cpp/tests/test_roomlab.py](../../../irc-track/01-roomlab/cpp/tests/test_roomlab.py)

## 읽는 순서

1. [00-series-map.md](00-series-map.md)
2. [10-chronology-registration-and-server-surface.md](10-chronology-registration-and-server-surface.md)
3. [20-chronology-channel-lifecycle.md](20-chronology-channel-lifecycle.md)
4. [30-chronology-delivery-cleanup-and-errors.md](30-chronology-delivery-cleanup-and-errors.md)
5. [40-chronology-smoke-verification-and-boundaries.md](40-chronology-smoke-verification-and-boundaries.md)
6. [../../../irc-track/01-roomlab/README.md](../../../irc-track/01-roomlab/README.md)

## 검증 진입점

```bash
cd ../../../irc-track/01-roomlab/cpp
make clean && make test
```

## chronology 메모

- `roomlab`은 `eventlab`과 `msglab`을 한 서버로 합치는 첫 단계라, chronology도 registration surface -> channel mutation -> delivery/error -> smoke verification 순으로 쪼갰다.
- `2026-03-11`은 현재 `verified` 상태가 고정된 날짜 앵커고, 그 이전 세부 구현 순서는 `Day / Session`으로 복원했다.
- 이 문서는 별도 노트 계층 없이 source set과 smoke test contract만으로 구성했다.
