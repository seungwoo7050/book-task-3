# 02-ircserv-cpp 문제지

## 왜 중요한가

앞선 IRC lab에서 나눈 책임을 한 서버에 다시 통합하되, pure TCP 기준의 capstone 범위를 분명하게 유지해야 한다.

## 목표

시작 위치의 구현을 완성해 roomlab 범위의 core command를 유지한다, CAP LS 302, TOPIC, MODE, KICK, INVITE를 추가한다, registration 과정에서 005 ISUPPORT를 광고한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/irc-track/02-ircserv/cpp/src/Channel.cpp`
- `../study/irc-track/02-ircserv/cpp/src/Connection.cpp`
- `../study/irc-track/02-ircserv/cpp/src/debug.cpp`
- `../study/irc-track/02-ircserv/cpp/src/EventManager.cpp`
- `../study/irc-track/02-ircserv/cpp/tests/test_irc_join.py`
- `../study/irc-track/02-ircserv/cpp/Makefile`

## starter code / 입력 계약

- `../study/irc-track/02-ircserv/cpp/src/Channel.cpp`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- roomlab 범위의 core command를 유지한다.
- CAP LS 302, TOPIC, MODE, KICK, INVITE를 추가한다.
- registration 과정에서 005 ISUPPORT를 광고한다.
- raw TCP client로 검증 가능한 smoke test를 제공한다.

## 제외 범위

- TLS, SASL, operator services
- full IRCv3 capability negotiation
- persistence와 운영 배포 자동화

## 성공 체크리스트

- 핵심 흐름은 `_do_leaks`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `wait_for_port`와 `send_line`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/irc-track/02-ircserv/cpp test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/cpp-server/study/irc-track/02-ircserv/cpp test
```

- `02-ircserv`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`02-ircserv-cpp_answer.md`](02-ircserv-cpp_answer.md)에서 확인한다.
