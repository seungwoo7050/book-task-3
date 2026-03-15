# 01-roomlab-cpp 문제지

## 왜 중요한가

등록과 room lifecycle을 실제 TCP 서버 위에서 다루되, RFC 전체가 아니라 core IRC subset 범위만 분명하게 보여 줄 수 있어야 한다.

## 목표

시작 위치의 구현을 완성해 PASS, NICK, USER 기반 등록을 처리한다, JOIN, PART로 room create, join, leave를 처리한다, PRIVMSG, NOTICE를 전달한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/irc-track/01-roomlab/cpp/src/Channel.cpp`
- `../study/irc-track/01-roomlab/cpp/src/Connection.cpp`
- `../study/irc-track/01-roomlab/cpp/src/debug.cpp`
- `../study/irc-track/01-roomlab/cpp/src/EventManager.cpp`
- `../study/irc-track/01-roomlab/cpp/tests/test_roomlab.py`
- `../study/irc-track/01-roomlab/cpp/Makefile`

## starter code / 입력 계약

- `../study/irc-track/01-roomlab/cpp/src/Channel.cpp`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- PASS, NICK, USER 기반 등록을 처리한다.
- JOIN, PART로 room create, join, leave를 처리한다.
- PRIVMSG, NOTICE를 전달한다.
- PING, PONG, QUIT과 idle keep-alive를 처리한다.
- duplicate nick 거절과 disconnect cleanup이 동작한다.

## 제외 범위

- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `_do_leaks`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `wait_for_port`와 `send_line`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/irc-track/01-roomlab/cpp test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/cpp-server/study/irc-track/01-roomlab/cpp test
```

- `01-roomlab`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`01-roomlab-cpp_answer.md`](01-roomlab-cpp_answer.md)에서 확인한다.
