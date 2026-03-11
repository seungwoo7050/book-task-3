# roomlab 문제

## 문제

등록과 room lifecycle을 실제 TCP 서버 위에서 다루되, RFC 전체가 아니라 core IRC subset 범위만 분명하게 보여 줄 수 있어야 한다.

## 성공 기준

- `PASS`, `NICK`, `USER` 기반 등록을 처리한다.
- `JOIN`, `PART`로 room create, join, leave를 처리한다.
- `PRIVMSG`, `NOTICE`를 전달한다.
- `PING`, `PONG`, `QUIT`과 idle keep-alive를 처리한다.
- duplicate nick 거절과 disconnect cleanup이 동작한다.

## 현재 근거

- [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp)
- [../cpp/src/execute_join.cpp](../cpp/src/execute_join.cpp)
- [../cpp/src/Server.cpp](../cpp/src/Server.cpp)
- [../cpp/tests/test_roomlab.py](../cpp/tests/test_roomlab.py)
