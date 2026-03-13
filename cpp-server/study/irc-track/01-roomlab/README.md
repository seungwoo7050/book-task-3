# roomlab

## 이 lab이 푸는 문제

작동하는 작은 IRC 서버를 설명할 때 registration, room membership, broadcast, cleanup을 한 덩어리로만 보면 capstone과의 차이가 사라진다. `roomlab`은 IRC subset 서버의 첫 완성형으로서 core 상태 전이만 먼저 고정한다.

## 내가 만든 답

- `PASS`, `NICK`, `USER` 기반 registration을 구현한다.
- `JOIN`, `PART`, `PRIVMSG`, `NOTICE`, `QUIT`으로 room lifecycle을 만든다.
- duplicate nick, broadcast, disconnect cleanup을 multi-client smoke test로 검증한다.

## 범위 밖

- `TOPIC`, `MODE`, `KICK`, `INVITE`, `CAP`
- TLS, SASL, services
- 게임 관련 command와 state

## 검증 방법

- 상태: `verified`
- 기준일: `2026-03-11`
- 위치: [cpp/README.md](cpp/README.md)

```sh
cd cpp
make clean && make test
```

## 핵심 파일

- [problem/README.md](problem/README.md)
- [cpp/src/Executor.cpp](cpp/src/Executor.cpp)
- [cpp/src/execute_join.cpp](cpp/src/execute_join.cpp)
- [cpp/tests/test_roomlab.py](cpp/tests/test_roomlab.py)

## Source-First Blog

- 실제 소스와 테스트만으로 다시 읽는 chronology는 [../../blog/irc-track/01-roomlab/README.md](../../blog/irc-track/01-roomlab/README.md)에서 이어진다.

## 다음 단계

- 고급 channel command까지 확장한 capstone은 [../02-ircserv/README.md](../02-ircserv/README.md)
