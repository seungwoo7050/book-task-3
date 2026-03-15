# ircserv 문제

## 문제

앞선 IRC lab에서 나눈 책임을 한 서버에 다시 통합하되, pure TCP 기준의 capstone 범위를 분명하게 유지해야 한다.

## 성공 기준

- `roomlab` 범위의 core command를 유지한다.
- `CAP LS 302`, `TOPIC`, `MODE`, `KICK`, `INVITE`를 추가한다.
- registration 과정에서 `005 ISUPPORT`를 광고한다.
- raw TCP client로 검증 가능한 smoke test를 제공한다.

## canonical verification 시작 위치

- 실행과 검증 진입점은 [../cpp/README.md](../cpp/README.md)다.

## 제외 범위

- TLS, SASL, operator services
- full IRCv3 capability negotiation
- persistence와 운영 배포 자동화

## 현재 근거

- [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp)
- [../cpp/src/Channel.cpp](../cpp/src/Channel.cpp)
- [../cpp/src/Server.cpp](../cpp/src/Server.cpp)
- [../cpp/tests/test_irc_join.py](../cpp/tests/test_irc_join.py)
