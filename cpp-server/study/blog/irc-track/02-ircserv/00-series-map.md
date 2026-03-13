# ircserv series map

이 시리즈는 `ircserv`를 `roomlab`의 단순 기능 확장이 아니라, 기존 subset 위에 privilege와 advanced command를 통합한 pure TCP capstone으로 다시 읽기 위한 지도다.

## 이 프로젝트가 답하는 질문

- `roomlab`의 registration과 room lifecycle을 유지한 채 `CAP`, `MODE`, `TOPIC`, `INVITE`, `KICK`를 어디까지 통합해야 할까
- advanced IRC 기능을 넣어도 여전히 작은 smoke test로 설명 가능한 범위를 지킬 수 있을까

## 읽는 순서

1. [10-chronology-baseline-capability-and-registration.md](10-chronology-baseline-capability-and-registration.md)
2. [20-chronology-channel-privilege-and-mode-state.md](20-chronology-channel-privilege-and-mode-state.md)
3. [30-chronology-advanced-command-flows.md](30-chronology-advanced-command-flows.md)
4. [40-chronology-capstone-verification-and-boundaries.md](40-chronology-capstone-verification-and-boundaries.md)

## 참조한 실제 파일

- `study/irc-track/02-ircserv/README.md`
- `study/irc-track/02-ircserv/problem/README.md`
- `study/irc-track/02-ircserv/cpp/README.md`
- `study/irc-track/02-ircserv/cpp/Makefile`
- `study/irc-track/02-ircserv/cpp/include/inc/Channel.hpp`
- `study/irc-track/02-ircserv/cpp/include/inc/Server.hpp`
- `study/irc-track/02-ircserv/cpp/src/Executor.cpp`
- `study/irc-track/02-ircserv/cpp/src/Channel.cpp`
- `study/irc-track/02-ircserv/cpp/src/Server.cpp`
- `study/irc-track/02-ircserv/cpp/tests/test_irc_join.py`
- `study/irc-track/02-ircserv/docs/README.md`

## Canonical CLI

```bash
cd study/irc-track/02-ircserv/cpp
make clean && make test
```

## Git Anchor

- `2026-03-09 73372bd Add project: backend-fastapi, backend-spring, cpp-server`
- `2026-03-10 7dc71a8 docs: enhance cpp-server`
- `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`

## 추론 원칙

- chronology는 `roomlab`에 이미 있던 baseline surface를 먼저 고정한 뒤, `Channel` mode bit와 privilege state, 초대/강퇴/topic 시나리오, smoke verification 순으로 확장한다.
- `ircserv`의 차이는 명령 개수 자체보다 "operator privilege를 별도 state로 들고 다닌다"는 점에서 설명한다.

