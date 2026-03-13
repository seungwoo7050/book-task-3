# 10 Baseline Capability And Registration

## Day 1
### Session 1

- 목표: `ircserv`가 `roomlab` baseline을 버린 새 서버가 아니라, 그 위에 capability negotiation을 얹은 capstone인지 확인한다.
- 진행: `problem/README.md`, `cpp/README.md`, `_execute_cap`, `_execute_user`, test의 `CAP LS 302` 시작 부분을 함께 읽었다.
- 이슈: 처음엔 `CAP`이 고급 부가 기능처럼 보였지만, 실제 smoke test는 registration 이전에 `CAP LS 302` 응답을 먼저 받아 modern IRC surface를 확인한다.
- 판단: 이 프로젝트의 출발점은 `roomlab` baseline을 유지하면서도 "호환 가능한 capstone"이라는 신호를 앞단에서 주는 것이다.

CLI:

```bash
$ cd study/irc-track/02-ircserv/cpp
$ sed -n '1,200p' README.md
$ rg -n "_execute_cap|_execute_user|_isupport" src/Executor.cpp tests/test_irc_join.py
$ sed -n '150,260p' src/Executor.cpp
$ sed -n '1,120p' tests/test_irc_join.py
```

이 시점의 핵심 코드는 `CAP LS 302`에 대한 최소 응답이었다.

```cpp
if (msg.params.size() == 1 && msg.params[0] == "END")
    return;
if (msg.params.size() != 2)
    rpl = BUILD_ERR_NEEDMOREPARAMS(server.servername, msg.command);
else if (msg.params[0] == "LS" && msg.params[1] == "302")
    rpl = "CAP * LS :\r\n";
```

처음엔 capabilities를 길게 나열할 줄 알았는데, 실제 구현은 "302를 이해한다"는 최소 handshake만 먼저 제공한다. 그래서 `ircserv`의 capstone 성격은 기능 풍부함보다 compatibility surface를 어디까지 드러낼지에 가깝다.

이 baseline은 registration completion과도 연결된다.

```python
send_line(alice, "CAP LS 302")
if "CAP * LS :" not in recv_until(alice, "CAP * LS :", time.time() + 5):
    raise RuntimeError("CAP LS 302 response missing")
```

나중에 보니 `ircserv`는 `roomlab`의 registration path를 유지한 채 그 앞에 capability probe를 얹는 구조였다.

