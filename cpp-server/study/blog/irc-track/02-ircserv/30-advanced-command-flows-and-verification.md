# ircserv 3. advanced command가 cleanup까지 버티는지 확인하기

advanced command를 추가할수록 가장 먼저 위험해지는 것은 응답 포맷보다 state cleanup이다. ircserv에서 그 점이 가장 잘 보이는 함수는 [`_execute_kick()`](../../../irc-track/02-ircserv/cpp/src/Executor.cpp)다. `KICK`은 channel 전체에 이벤트를 방송하는 것만으로 끝나지 않는다. target user의 `chandb`에서도 해당 channel을 지워야 다음 상태 전이가 꼬이지 않는다.

```cpp
Executor::broadcast(server, chan,
    ":" + node->nickname + " KICK " + channame + " " + nickname + " :" + comment + "\r\n");

targetnode->chandb.erase(channame);
chan->part(targetnode);
```

바로 이 두 줄 때문에 capstone의 무게가 느껴진다. roomlab에서는 advanced helper가 있어도 dispatcher가 그 경로를 열지 않았지만, ircserv에서는 `KICK`이 실제 membership cleanup까지 책임진다. `INVITE`와 `MODE`가 privilege를 만들었다면, `KICK`은 그 privilege가 상태를 안전하게 바꾸는지 끝까지 시험한다.

[`tests/test_irc_join.py`](../../../irc-track/02-ircserv/cpp/tests/test_irc_join.py)는 이 흐름을 end-to-end로 확인한다. alice가 `JOIN #ops` 후 `MODE #ops +i`를 걸고, carol을 `INVITE`해 invite-only room에 들인다. 그다음 `TOPIC #ops :control room`과 `PRIVMSG #ops :hello capstone`이 이어지고, 마지막으로 alice가 `KICK #ops bob :bye`를 보내면 bob은 더 이상 room member가 아니게 된다. 그래서 다시 `JOIN #ops`를 시도하면 `473 invite-only`로 거절된다.

직접 실행한 CLI는 아래처럼 닫힌다.

```sh
cd /Users/woopinbell/work/book-task-3/cpp-server/study/irc-track/02-ircserv/cpp
make clean && make test
```

```text
python3 tests/test_irc_join.py
ircserv capstone smoke passed.
```

이 smoke는 capstone이 단순히 mode나 invite를 저장하는지보다, 그 상태가 실제 rejoin rejection과 membership cleanup까지 밀려 가는지를 보여 준다. 동시에 이 문서가 일부러 남겨 두는 범위도 분명하다. TLS, SASL, services는 없고, CAP negotiation도 `LS 302` 최소 응답만 구현한다. 그래서 ircserv의 마무리는 full IRCd 선언이 아니라, pure TCP capstone으로서 설명 가능한 범위를 끝까지 지켜 냈다는 proof에 가깝다.

