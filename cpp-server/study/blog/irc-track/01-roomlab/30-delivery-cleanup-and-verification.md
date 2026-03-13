# roomlab 3. delivery와 cleanup이 같은 경로에서 닫히는지 보기

roomlab의 마지막 장면은 메시지를 얼마나 많이 보내느냐보다, 보낸 뒤에 얼마나 깔끔하게 정리하느냐에 있다. [`cpp/src/Executor.cpp`](../../../irc-track/01-roomlab/cpp/src/Executor.cpp)의 `_execute_privmsg()`와 `_execute_notice()`는 채널 대상과 사용자 대상을 나눠 처리한다. 채널 대상이면 `server.chandb`에서 room을 찾고, 개인 대상이면 `nickdb`를 통해 직접 사용자를 찾는다.

```cpp
if (msg.params[0].find('#') != std::string::npos)
    broadcast(server, channelPtr, toSend + "\r\n");
else
    dispatch_packet(server, *it->second, toSend + "\r\n");
```

`NOTICE`가 IRC 관례대로 대부분의 에러를 조용히 삼키는 반면, `PRIVMSG`는 recipient 누락이나 text 누락, 존재하지 않는 nick을 직접 돌려준다는 점도 이 구간에서 드러난다. 작은 subset 서버라도 command semantic이 이미 갈라지기 시작한 셈이다.

더 흥미로운 장면은 `QUIT`과 실제 소켓 종료가 만나는 곳이다. `_execute_quit()`는 먼저 각 channel에 `QUIT` broadcast를 보낸 뒤 `to_doom()`으로 연결을 종료 대기 상태로 바꾼다. 그리고 write phase가 끝나면 [`Server::_disconnect()`](../../../irc-track/01-roomlab/cpp/src/Server.cpp)가 `sendq`, `sockdb`, `nickdb`, `node->chandb`, `server.chandb`를 한 번에 정리한다. 즉 "사용자가 QUIT을 보냈다"와 "fd가 닫혔다"가 결국 같은 cleanup path로 합쳐진다.

[`tests/test_roomlab.py`](../../../irc-track/01-roomlab/cpp/tests/test_roomlab.py)는 이 흐름을 raw TCP로 한 번에 확인한다. alice와 bob이 등록을 끝내고 같은 room에 들어간 뒤, `PRIVMSG`와 `NOTICE`가 오가고, duplicate nick `alice`는 `433`으로 거절된다. 이어서 `PING token123`에 `PONG token123`이 돌아오고, alice의 `QUIT :gone away`는 bob에게 broadcast된다. 마지막으로 room 밖 사용자의 `PART #lab`은 `442`로 거절된다.

직접 실행한 CLI는 아래처럼 닫힌다.

```sh
cd /Users/woopinbell/work/book-task-3/cpp-server/study/irc-track/01-roomlab/cpp
make clean && make test
```

```text
python3 tests/test_roomlab.py
roomlab smoke passed.
```

이 결과가 말해 주는 것은 roomlab이 단순한 데모가 아니라는 점이다. registration, join, delivery, duplicate nick, ping/pong, quit cleanup까지 한 번의 smoke path 안에서 이어진다. 다만 dispatcher가 아직 core subset만 열고 있다는 점도 같이 남는다. 그 문을 실제로 열어 capstone으로 가는 버전이 [`../02-ircserv/README.md`](../02-ircserv/README.md)다.

