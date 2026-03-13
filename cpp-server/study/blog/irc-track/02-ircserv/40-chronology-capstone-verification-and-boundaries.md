# 40 Capstone Verification And Boundaries

## 2026-03-11
### Session 1

- 목표: 현재 `ircserv`가 capstone으로서 무엇을 검증하는지 고정한다.
- 진행: `Makefile`, `cpp/README.md`, `tests/test_irc_join.py`를 함께 읽었다.
- 판단: canonical smoke path는 `CAP LS 302`로 capability surface를 먼저 확인하고, 세 client가 `JOIN #ops`, `MODE +i`, `INVITE`, `TOPIC`, `PRIVMSG`, `KICK`, invite-only rejoin rejection, `PING`/`PONG`까지 한 번에 묶어 돈다.
- 검증: README 표면은 `verified`, 테스트 최종 신호는 `ircserv capstone smoke passed.`다.
- 다음: 다른 도메인의 capstone 비교는 `arenaserv`가 맡는다.

CLI:

```bash
$ cd study/irc-track/02-ircserv/cpp
$ sed -n '1,200p' Makefile
$ sed -n '1,240p' tests/test_irc_join.py
$ make clean && make test
```

출력:

```text
ircserv capstone smoke passed.
```

이 시점의 핵심 코드는 smoke test가 일부러 만드는 마지막 실패 경로였다.

```python
time.sleep(0.2)
send_line(bob, "JOIN #ops")
if " 473 bob #ops " not in recv_until(bob, " 473 bob #ops ", time.time() + 8):
    raise RuntimeError("invite-only rejoin rejection missing")
```

처음엔 `INVITE` 성공만 확인하면 충분할 것 같았는데, 실제 capstone의 핵심은 초대받지 않은 상태로 다시 들어오려 할 때 정책이 유지되는지를 끝까지 확인하는 데 있었다. 그래서 `ircserv`는 기능 나열이 아니라 channel policy의 일관성을 검증하는 lab으로 읽힌다.

현재 경계:

- 포함: `CAP LS 302`, `005 ISUPPORT`, `MODE`, `TOPIC`, `INVITE`, `KICK`
- 제외: TLS, SASL, services, full IRCv3 negotiation

