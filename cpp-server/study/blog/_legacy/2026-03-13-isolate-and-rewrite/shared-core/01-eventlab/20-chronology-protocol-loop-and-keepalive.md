# 20 Protocol Loop And Keepalive

## Day 1
### Session 2

- 목표: `eventlab`의 protocol surface가 얼마나 작은지, 그리고 keep-alive가 어디서 개입하는지 확인한다.
- 진행: `Server::process_input`, `handle_line`, `keep_alive`, `EventManager::listen_event`, `open_listenfd`를 이어서 읽었다.
- 이슈: 처음엔 `PING`/`PONG`이 테스트용 보조 기능처럼 보였지만, 실제로는 idle cutoff를 강제하는 핵심 계약이었다.
- 판단: 이 lab은 복잡한 parser를 붙이는 대신, newline framing과 `PING :idle-check`를 직접 `Server.cpp`에서 처리해 runtime 경계가 흐려지지 않게 만든다.

CLI:

```bash
$ cd study/shared-core/01-eventlab/cpp
$ rg -n "keep_alive|process_input|handle_line|open_listenfd" src include/inc
$ sed -n '60,220p' src/Server.cpp
$ sed -n '70,220p' src/EventManager.cpp
```

이 시점의 핵심 코드는 아래였다.

```cpp
if (!client.pinged && now - client.timestamp > timeout)
{
    client.pinged = true;
    this->queue_reply(client, "PING :idle-check\r\n");
}
else if (client.pinged && now - client.timestamp > cutoff)
{
    stale.push_back(client.fd);
}
```

처음엔 keep-alive가 단순 heartbeat 정도라고 생각했는데, 실제로는 `timestamp -> pinged -> stale`로 이어지는 두 단계 상태 전이가 이 lab의 disconnect discipline을 만든다. 그래서 뒤쪽 capstone이 이 구조를 재사용하더라도 원인을 runtime 층에서 먼저 읽을 수 있게 된다.

같은 이유로 protocol 처리도 끝까지 작게 남겨 둔다.

```cpp
if (line == "QUIT")
{
    this->queue_reply(client, "BYE\r\n");
    client.doomed = true;
    return;
}

if (line.compare(0, 4, "PING") == 0)
{
    this->queue_reply(client, "PONG " + token + "\r\n");
    return;
}
```

이 정도로 명령 수를 제한했기 때문에, 여기서 깨지는 문제는 parser나 state machine보다 runtime loop 자체에 가깝다고 볼 수 있다.

