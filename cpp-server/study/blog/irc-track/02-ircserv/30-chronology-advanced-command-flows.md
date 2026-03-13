# 30 Advanced Command Flows

## Day 2
### Session 1

- 목표: invite-only channel, invite delivery, kick cleanup 같은 advanced flow가 실제로 어떻게 이어지는지 확인한다.
- 진행: `_execute_invite`, `_execute_kick`, test의 `alice/bob/carol` 시나리오를 같이 읽었다.
- 이슈: 처음엔 `INVITE`와 `KICK`이 독립 명령이라고 생각했는데, 실제 smoke path에서는 `MODE +i -> INVITE -> JOIN -> TOPIC -> PRIVMSG -> KICK -> rejoin rejection` 순서로 하나의 channel policy 이야기로 묶여 있었다.
- 판단: `ircserv`의 세 번째 답은 "고급 명령을 많이 넣는다"가 아니라 "한 channel policy가 여러 command를 관통하게 만든다"는 쪽에 있다.

CLI:

```bash
$ cd study/irc-track/02-ircserv/cpp
$ rg -n "_execute_invite|_execute_kick|INVITE carol|KICK #ops bob|473 bob" src/Executor.cpp tests/test_irc_join.py
$ sed -n '520,760p' src/Executor.cpp
$ sed -n '70,180p' tests/test_irc_join.py
```

이 시점의 핵심 코드는 invite-only channel에서 초대장을 별도 DB로 남기는 부분이었다.

```cpp
chan->invitedb.insert(std::pair<int, Connection *>(targetnode->sockfd, targetnode));

dispatch_packet(server, targetnode, ":" + node->nickname + " INVITE " + target + " " + channame + "\r\n");
dispatch_packet(server, node, BUILD_RPL_INVITING(server.servername, node->nickname, target, channame));
```

처음엔 `INVITE`가 단지 event 하나를 보내는 줄 알았는데, 실제로는 `invitedb`에 남아야만 뒤쪽 `JOIN`이 `473 invite-only`를 통과할 수 있다. 그래서 이 명령은 알림보다 state mutation에 더 가깝다.

같은 맥락으로 `KICK`도 단순 broadcast가 아니다.

```cpp
Executor::broadcast(server, chan, ":" + node->nickname + " KICK " + channame + " " + nickname + " :" + comment + "\r\n");

targetnode->chandb.erase(channame);
chan->part(targetnode);
```

나중에 보니 `KICK`의 핵심은 메시지보다, target user를 channel과 client 양쪽 인덱스에서 동시에 떼어 내는 정리 흐름이었다.

