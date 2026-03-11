# arenaserv 문제

## 문제

authoritative game server의 핵심 계약을 pure TCP 환경에서 가장 작은 capstone으로 보여 줄 수 있어야 한다.

## 성공 기준

- `HELLO`, `QUEUE`, `READY`, `INPUT`, `PING`, `REJOIN`, `LEAVE`를 처리한다.
- `WELCOME`, `ROOM`, `COUNTDOWN`, `SNAPSHOT`, `HIT`, `ELIM`, `ROUND_END`, `ERROR`를 보낸다.
- 20x20 bounded tile arena, 2~4인 room, HP 3, 단일 action `FIRE` 규칙을 유지한다.
- 10초 reconnect grace를 처리한다.

## 현재 근거

- [../cpp/src/Server.cpp](../cpp/src/Server.cpp)
- [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp)
- [../cpp/tests/test_arenaserv.py](../cpp/tests/test_arenaserv.py)
