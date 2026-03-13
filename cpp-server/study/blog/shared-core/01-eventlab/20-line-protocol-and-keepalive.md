# eventlab 2. line protocol과 keep-alive가 올라가는 자리

event loop 뼈대가 잡히고 나면, 다음으로 드러나는 문제는 바이트 스트림을 어디서 끊을 것인가다. `eventlab`은 parser lab이 아니지만, 그렇다고 raw byte를 바로 도메인 처리로 넘기지도 않는다. 이 지점이 뒤의 `msglab`로 이어지는 자연스러운 다리가 된다.

[`Server::read_packet()`](../../../shared-core/01-eventlab/cpp/src/Server.cpp)은 먼저 읽은 바이트를 `recvbuf`에 쌓는다. 그다음 [`Server::process_input()`](../../../shared-core/01-eventlab/cpp/src/Server.cpp)이 `\n` 경계를 찾아 완성된 line만 꺼낸다. 아직은 가장 단순한 형태지만, "경계 자르기"를 소켓 read와 분리해 둔 순간 parser가 들어올 자리가 이미 정리된다.

```cpp
std::size_t pos = client.recvbuf.find('\n');
std::string line = client.recvbuf.substr(0, pos);
client.recvbuf.erase(0, pos + 1);
if (!line.empty() && line[line.size() - 1] == '\r')
    line.erase(line.size() - 1);
```

이후 [`handle_line()`](../../../shared-core/01-eventlab/cpp/src/Server.cpp)은 일부러 아주 적은 계약만 연다. `QUIT`이면 `BYE`를 보내고 종료 대기 상태로 돌리고, `PING <token>`이면 `PONG <token>`으로 응답하고, 나머지는 전부 `ECHO <line>`으로 되돌린다. 작은 규칙이지만, 이 정도면 읽기/쓰기/종료 흐름을 end-to-end로 확인하기엔 충분하다.

`queue_reply()`가 작은 함수인데도 중요한 이유도 여기 있다. 응답을 즉시 `send()`하지 않고 `sendbuf`와 `sendq`에 넣어 write phase로 넘기기 때문이다. 그래서 read와 write가 서로 얽히지 않고, event loop의 세 갈래 구조도 그대로 유지된다.

keep-alive는 그보다 한 단계 앞에서 작동한다. [`Server::keep_alive()`](../../../shared-core/01-eventlab/cpp/src/Server.cpp)는 매 loop 초반에 각 클라이언트의 `timestamp`를 훑고, 일정 시간 응답이 없으면 `PING :idle-check`를 보낸다. 이미 ping을 보냈는데도 더 오래 침묵하면 그제야 연결을 정리한다.

```cpp
if (!client.pinged && now - client.timestamp > timeout)
    this->queue_reply(client, "PING :idle-check\r\n");
else if (client.pinged && now - client.timestamp > cutoff)
    stale.push_back(client.fd);
```

이 장면이 중요한 이유는 keep-alive가 별도 기능처럼 붙어 있지 않기 때문이다. 여기서는 운영 편의 기능이 아니라, 응답 없는 fd를 오래 붙잡지 않기 위한 런타임 정책으로 event loop 앞단에 놓여 있다. 그렇게 보면 `eventlab`의 둘째 글은 명령어를 소개하는 글이라기보다, line framing과 session 정리 경계가 어디서 시작되는지 보여 주는 글에 가깝다.

