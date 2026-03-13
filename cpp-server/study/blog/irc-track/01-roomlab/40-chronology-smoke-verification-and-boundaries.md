# 40 Smoke Verification And Boundaries

## 2026-03-11
### Session 1

- 목표: 현재 `roomlab`이 어떤 end-to-end subset을 검증하는지 고정한다.
- 진행: `Makefile`, `cpp/README.md`, `tests/test_roomlab.py`를 함께 읽었다.
- 판단: 이 lab의 canonical check는 raw socket 세 개를 열어 registration, `JOIN`, channel `PRIVMSG`, direct `NOTICE`, duplicate nick rejection, `PING`/`PONG`, `QUIT`, `PART` 오류까지 한 번에 묶는 smoke test다.
- 검증: README 표면은 `verified`, 테스트 최종 신호는 `roomlab smoke passed.`다.
- 다음: `CAP`, invite-only mode, `TOPIC`, `INVITE`, `KICK` 같은 advanced command는 `ircserv`가 맡는다.

CLI:

```bash
$ cd study/irc-track/01-roomlab/cpp
$ sed -n '1,200p' Makefile
$ sed -n '1,240p' tests/test_roomlab.py
$ make clean && make test
```

출력:

```text
roomlab smoke passed.
```

이 시점의 핵심 코드는 smoke test의 등록 helper였다.

```python
send_line(sock, f"PASS {password}")
send_line(sock, f"NICK {nick}")
send_line(sock, f"USER {nick} 0 * :{nick}")
return recv_until(sock, f" 005 {nick} ", time.time() + 5)
```

처음엔 테스트가 `001` welcome만 기다릴 줄 알았는데, 실제로는 `005`까지 받아 registration completion을 판단한다. 즉 `roomlab`은 채팅 성공보다 "subset surface가 완전히 열렸는가"를 더 중요한 계약으로 본다.

현재 경계:

- 포함: `PASS`, `NICK`, `USER`, `JOIN`, `PART`, `PRIVMSG`, `NOTICE`, `PING`, `QUIT`
- 제외: `CAP`, `MODE`, `TOPIC`, `INVITE`, `KICK`, TLS, SASL

