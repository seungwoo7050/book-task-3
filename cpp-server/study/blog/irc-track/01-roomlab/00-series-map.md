# roomlab series map

이 시리즈는 `roomlab`을 "작은 IRC 서버"가 아니라 registration과 room lifecycle을 먼저 고정하는 subset lab으로 다시 읽기 위한 지도다.

## 이 프로젝트가 답하는 질문

- 등록 전후에 허용 명령을 어떻게 나눠야 room state가 망가지지 않을까
- `JOIN`, `PART`, `PRIVMSG`, `QUIT`가 server database와 channel database를 동시에 어떻게 갱신할까

## 읽는 순서

1. [10-chronology-registration-and-server-surface.md](10-chronology-registration-and-server-surface.md)
2. [20-chronology-channel-lifecycle.md](20-chronology-channel-lifecycle.md)
3. [30-chronology-delivery-cleanup-and-errors.md](30-chronology-delivery-cleanup-and-errors.md)
4. [40-chronology-smoke-verification-and-boundaries.md](40-chronology-smoke-verification-and-boundaries.md)

## 참조한 실제 파일

- `study/irc-track/01-roomlab/README.md`
- `study/irc-track/01-roomlab/problem/README.md`
- `study/irc-track/01-roomlab/cpp/README.md`
- `study/irc-track/01-roomlab/cpp/Makefile`
- `study/irc-track/01-roomlab/cpp/include/inc/Server.hpp`
- `study/irc-track/01-roomlab/cpp/include/inc/Connection.hpp`
- `study/irc-track/01-roomlab/cpp/include/inc/Channel.hpp`
- `study/irc-track/01-roomlab/cpp/src/Executor.cpp`
- `study/irc-track/01-roomlab/cpp/src/execute_join.cpp`
- `study/irc-track/01-roomlab/cpp/src/Server.cpp`
- `study/irc-track/01-roomlab/cpp/tests/test_roomlab.py`
- `study/irc-track/01-roomlab/docs/README.md`

## Canonical CLI

```bash
cd study/irc-track/01-roomlab/cpp
make clean && make test
```

## Git Anchor

- `2026-03-09 73372bd Add project: backend-fastapi, backend-spring, cpp-server`
- `2026-03-10 7dc71a8 docs: enhance cpp-server`
- `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`

## 추론 원칙

- chronology는 `PASS/NICK/USER` registration path를 먼저, 그다음 `JOIN/PART`로 channel DB mutation을, 마지막으로 `PRIVMSG/NOTICE/QUIT`와 smoke test를 읽는 순서로 복원한다.
- `roomlab`과 `ircserv`의 코드 표면이 비슷해 보여도, 여기서는 `CAP`, `MODE`, `TOPIC`, `INVITE`, `KICK`를 의도적으로 제외한 subset 경계를 유지한다.

