# Tests

`make test`는 `tests/test_irc_join.py`를 실행한다. 검증 범위는 다음과 같다.

- `CAP LS 302`
- registration과 `005 ISUPPORT`
- `JOIN`
- `MODE +i`
- `INVITE`
- `TOPIC`
- `PRIVMSG`
- `KICK`
- invite-only 재입장 거절
- `PING`/`PONG`
