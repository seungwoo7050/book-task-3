# ircserv 문제 재구성

이 문서는 현재 저장소의 구현, 테스트, 보존된 기록을 바탕으로 다시 정리한 학습용 문제 설명이다. `ircserv`는 RFC 전체를 재현하는 프로젝트가 아니라, 이 커리큘럼에서 “pure TCP IRC capstone”이라 부를 만한 핵심 범위를 보여 주는 프로젝트다.

## 학습 목표

- 앞선 IRC lab에서 나눈 책임을 한 서버에 다시 통합한다.
- channel privilege와 advanced command를 다뤄 capstone 수준의 completeness를 만든다.
- raw TCP 기준으로 end-to-end smoke test를 설계한다.

## 구현해야 할 것

- `roomlab` 범위의 core command 유지
- `CAP LS 302`, `TOPIC`, `MODE`, `KICK`, `INVITE` 추가
- registration 과정에서 `005 ISUPPORT` 광고
- raw TCP client로 검증 가능한 smoke test 작성

## 산출물

- C++17 capstone IRC server
- raw TCP end-to-end smoke test

## 범위에서 제외하는 것

- TLS, SASL, operator services
- full IRCv3 capability negotiation
- 운영 배포와 persistence

## 현재 저장소에서 확인할 수 있는 근거

- [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp): advanced command 처리
- [../cpp/src/Channel.cpp](../cpp/src/Channel.cpp): channel privilege와 state
- [../cpp/src/Server.cpp](../cpp/src/Server.cpp): event loop와 connection lifecycle
- [../cpp/tests/test_irc_join.py](../cpp/tests/test_irc_join.py): capstone smoke test
