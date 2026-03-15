# 03-arenaserv-cpp 문제지

## 왜 중요한가

authoritative game server의 핵심 계약을 pure TCP 환경에서 가장 작은 capstone으로 보여 줄 수 있어야 한다.

## 목표

시작 위치의 구현을 완성해 HELLO, QUEUE, READY, INPUT, PING, REJOIN, LEAVE를 처리한다, WELCOME, ROOM, COUNTDOWN, SNAPSHOT, HIT, ELIM, ROUND_END, ERROR를 보낸다, x20 bounded tile arena, 2~4인 room, HP 3, 단일 action FIRE 규칙을 유지한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/game-track/03-arenaserv/cpp/src/EventManager.cpp`
- `../study/game-track/03-arenaserv/cpp/src/main.cpp`
- `../study/game-track/03-arenaserv/cpp/src/MatchEngine.cpp`
- `../study/game-track/03-arenaserv/cpp/src/Server.cpp`
- `../study/game-track/03-arenaserv/cpp/tests/test_arenaserv.py`
- `../study/game-track/03-arenaserv/cpp/Makefile`

## starter code / 입력 계약

- `../study/game-track/03-arenaserv/cpp/src/EventManager.cpp`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- HELLO, QUEUE, READY, INPUT, PING, REJOIN, LEAVE를 처리한다.
- WELCOME, ROOM, COUNTDOWN, SNAPSHOT, HIT, ELIM, ROUND_END, ERROR를 보낸다.
- x20 bounded tile arena, 2~4인 room, HP 3, 단일 action FIRE 규칙을 유지한다.
- 초 reconnect grace를 처리한다.

## 제외 범위

- UDP와 client prediction
- room shard, persistence, metrics, external matchmaking
- 여러 active room 동시 운영

## 성공 체크리스트

- 핵심 흐름은 `main`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `wait_for_port`와 `send_line`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/03-arenaserv/cpp test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/03-arenaserv/cpp test
```

- `03-arenaserv`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`03-arenaserv-cpp_answer.md`](03-arenaserv-cpp_answer.md)에서 확인한다.
