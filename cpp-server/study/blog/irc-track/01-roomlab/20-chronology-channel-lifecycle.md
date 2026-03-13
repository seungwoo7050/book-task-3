# 20 Channel Lifecycle

## Day 1
### Session 2

- 목표: `JOIN`과 `PART`가 channel lifecycle을 어디서 만들고 지우는지 확인한다.
- 진행: `execute_join.cpp`를 중심으로 `JOIN 0`, 신규 channel 생성, key/limit/invite-only 검사, 마지막 user가 나갈 때 channel 제거까지 따라갔다.
- 이슈: 처음엔 channel state가 별도 service에 숨겨져 있을 것 같았지만, 실제로는 `Executor`가 server DB와 `Channel` 객체를 함께 갱신하는 구조였다.
- 판단: 이 lab의 중심은 fancy IRC feature가 아니라 "room membership을 양방향으로 깨지지 않게 유지하는 것"이다.

CLI:

```bash
$ cd study/irc-track/01-roomlab/cpp
$ sed -n '1,260p' src/execute_join.cpp
$ rg -n "JOIN 0|TOOMANYCHANNELS|INVITEONLYCHAN|BADCHANNELKEY|CHANNELISFULL" src/execute_join.cpp
```

이 시점의 핵심 코드는 신규 channel 생성 분기였다.

```cpp
Channel *chan = new Channel(*it, node);
server.chans.push_front(chan);
server.chandb.insert(std::pair<std::string, std::list<Channel *>::iterator>(*it, server.chans.begin()));
chan->clientdb.insert(std::pair<int, Connection *>(node->sockfd, node));
node->chandb.insert(std::pair<std::string, Channel *>(*it, chan));
```

처음엔 `JOIN`이 단순히 membership 하나만 더하는 명령처럼 보였는데, 실제로는 server 쪽 `chandb`, channel 쪽 `clientdb`, client 쪽 `chandb`를 한 번에 맞춰야만 다음 `PRIVMSG`나 cleanup이 성립한다.

이 선택은 `JOIN 0`에서도 그대로 드러난다.

```cpp
Executor::broadcast(server, chan, ":" + node->nickname + " PART " + chan->name + " \r\n");
node->chandb.erase(beg);
chan->part(node);
if (chan->clientdb.empty())
    delete chan;
```

나중에 보니 `roomlab`에서 room lifecycle을 따로 떼어 둔 이유는 RFC 기능 수를 줄이기 위해서가 아니라, 이 양방향 정리 흐름을 capstone보다 먼저 읽게 만들기 위해서였다.

