# Tests

`make test`는 `tests/test_roomlab.py`를 실행한다. 검증 범위는 다음과 같다.

- 등록(`PASS`/`NICK`/`USER`)
- 중복 nick 거절
- `JOIN`
- channel `PRIVMSG`
- `NOTICE`
- `PING`/`PONG`
- `QUIT` cleanup
