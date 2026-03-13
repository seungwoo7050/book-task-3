# ircserv blog

이 디렉터리는 `ircserv`를 `source-first` 방식으로 다시 읽는 프로젝트 단위 blog 시리즈다. chronology는 프로젝트 README, `problem/README.md`, `cpp/README.md`, `cpp/Makefile`, `cpp/include/inc/Channel.hpp`, `cpp/src/Executor.cpp`, `cpp/src/Channel.cpp`, `cpp/src/Server.cpp`, `cpp/tests/test_irc_join.py`를 기준으로 복원했다.

## source set

- [../../../irc-track/02-ircserv/README.md](../../../irc-track/02-ircserv/README.md)
- [../../../irc-track/02-ircserv/problem/README.md](../../../irc-track/02-ircserv/problem/README.md)
- [../../../irc-track/02-ircserv/cpp/README.md](../../../irc-track/02-ircserv/cpp/README.md)
- [../../../irc-track/02-ircserv/cpp/Makefile](../../../irc-track/02-ircserv/cpp/Makefile)
- [../../../irc-track/02-ircserv/cpp/include/inc/Channel.hpp](../../../irc-track/02-ircserv/cpp/include/inc/Channel.hpp)
- [../../../irc-track/02-ircserv/cpp/include/inc/Server.hpp](../../../irc-track/02-ircserv/cpp/include/inc/Server.hpp)
- [../../../irc-track/02-ircserv/cpp/src/Executor.cpp](../../../irc-track/02-ircserv/cpp/src/Executor.cpp)
- [../../../irc-track/02-ircserv/cpp/src/Channel.cpp](../../../irc-track/02-ircserv/cpp/src/Channel.cpp)
- [../../../irc-track/02-ircserv/cpp/tests/test_irc_join.py](../../../irc-track/02-ircserv/cpp/tests/test_irc_join.py)

## 읽는 순서

1. [00-series-map.md](00-series-map.md)
2. [10-chronology-baseline-capability-and-registration.md](10-chronology-baseline-capability-and-registration.md)
3. [20-chronology-channel-privilege-and-mode-state.md](20-chronology-channel-privilege-and-mode-state.md)
4. [30-chronology-advanced-command-flows.md](30-chronology-advanced-command-flows.md)
5. [40-chronology-capstone-verification-and-boundaries.md](40-chronology-capstone-verification-and-boundaries.md)
6. [../../../irc-track/02-ircserv/README.md](../../../irc-track/02-ircserv/README.md)

## 검증 진입점

```bash
cd ../../../irc-track/02-ircserv/cpp
make clean && make test
```

## chronology 메모

- `ircserv`는 `roomlab` 위에 advanced command를 얹는 capstone이므로, chronology도 baseline 유지 -> mode state 추가 -> invite/topic/kick flow -> smoke verification 순서로 나눴다.
- `2026-03-11`은 현재 `verified` surface를 고정하는 날짜 앵커다.
- 본문은 별도 노트 계층 없이 source set과 smoke test contract만으로 재구성했다.
