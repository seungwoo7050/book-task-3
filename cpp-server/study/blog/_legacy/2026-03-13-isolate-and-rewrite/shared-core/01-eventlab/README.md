# eventlab blog

이 디렉터리는 `eventlab`을 `source-first` 방식으로 다시 읽는 프로젝트 단위 blog 시리즈다. chronology는 프로젝트 README, `problem/README.md`, `cpp/README.md`, `cpp/Makefile`, `cpp/include/inc/Server.hpp`, `cpp/src/EventManager.cpp`, `cpp/src/Server.cpp`, `cpp/tests/test_eventlab.py`를 기준으로 복원했다.

## source set

- [../../../shared-core/01-eventlab/README.md](../../../shared-core/01-eventlab/README.md)
- [../../../shared-core/01-eventlab/problem/README.md](../../../shared-core/01-eventlab/problem/README.md)
- [../../../shared-core/01-eventlab/cpp/README.md](../../../shared-core/01-eventlab/cpp/README.md)
- [../../../shared-core/01-eventlab/cpp/Makefile](../../../shared-core/01-eventlab/cpp/Makefile)
- [../../../shared-core/01-eventlab/cpp/include/inc/Server.hpp](../../../shared-core/01-eventlab/cpp/include/inc/Server.hpp)
- [../../../shared-core/01-eventlab/cpp/src/EventManager.cpp](../../../shared-core/01-eventlab/cpp/src/EventManager.cpp)
- [../../../shared-core/01-eventlab/cpp/src/Server.cpp](../../../shared-core/01-eventlab/cpp/src/Server.cpp)
- [../../../shared-core/01-eventlab/cpp/tests/test_eventlab.py](../../../shared-core/01-eventlab/cpp/tests/test_eventlab.py)

## 읽는 순서

1. [00-series-map.md](00-series-map.md)
2. [10-chronology-runtime-and-socket-surface.md](10-chronology-runtime-and-socket-surface.md)
3. [20-chronology-protocol-loop-and-keepalive.md](20-chronology-protocol-loop-and-keepalive.md)
4. [30-chronology-smoke-verification-and-boundaries.md](30-chronology-smoke-verification-and-boundaries.md)
5. [../../../shared-core/01-eventlab/README.md](../../../shared-core/01-eventlab/README.md)

## 검증 진입점

```bash
cd ../../../shared-core/01-eventlab/cpp
make clean && make test
```

## chronology 메모

- repo-level git history가 얇아서 chronology는 `Day / Session`을 기본으로 썼다.
- `2026-03-11`은 현재 README와 `cpp/README.md`가 `verified` 상태를 고정한 날짜 앵커다.
- 별도 노트 계층은 읽지 않았고, 실제 글은 source set과 test contract만으로 재구성했다.
