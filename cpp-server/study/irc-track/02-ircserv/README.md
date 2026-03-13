# ircserv

## 이 lab이 푸는 문제

capstone이 되면 기능만 늘리는 쪽으로 흐르기 쉽다. `ircserv`는 그런 확장이 아니라, `eventlab`, `msglab`, `roomlab`에서 분리한 런타임, parser, 상태 전이를 다시 한 서버로 합치면서도 읽기 쉬운 범위를 유지하는 문제를 푼다.

## 내가 만든 답

- `roomlab` 범위의 core command를 유지한다.
- `CAP LS 302`, `TOPIC`, `MODE`, `KICK`, `INVITE`, `005 ISUPPORT`를 추가한다.
- raw TCP smoke test로 privilege와 advanced command를 end-to-end로 검증한다.

## 범위 밖

- TLS, SASL, operator services
- full IRCv3 capability negotiation
- 운영 배포와 persistence

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
- [cpp/src/Channel.cpp](cpp/src/Channel.cpp)
- [cpp/tests/test_irc_join.py](cpp/tests/test_irc_join.py)

## Source-First Blog

- 실제 소스와 테스트만으로 다시 읽는 chronology는 [../../blog/irc-track/02-ircserv/README.md](../../blog/irc-track/02-ircserv/README.md)에서 이어진다.

## 다음 단계

- 다른 도메인의 capstone과 비교하려면 [../../game-track/03-arenaserv/README.md](../../game-track/03-arenaserv/README.md)
