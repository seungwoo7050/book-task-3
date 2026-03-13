# roomlab 1. registration과 subset 서버 표면 세우기

`roomlab`의 출발점은 "작동하는 IRC 서버"를 빨리 보여 주는 데 있지 않다. [`problem/README.md`](../../../irc-track/01-roomlab/problem/README.md)가 강조하는 것도 registration과 room lifecycle을 실제 TCP 서버 위에서 core subset 범위로 분명하게 보이라는 점이다. 그래서 첫 장면은 command 목록보다 [`cpp/src/Connection.cpp`](../../../irc-track/01-roomlab/cpp/src/Connection.cpp)와 [`cpp/src/Server.cpp`](../../../irc-track/01-roomlab/cpp/src/Server.cpp)가 어떻게 무거워졌는지에서 시작한다.

`Connection`은 더 이상 단순한 fd wrapper가 아니다. `recvbuf`, `sendbuf` 옆에 `nickname`, `username`, `hostname`, `chandb`, `is_authed`, `is_registered`가 붙는다. 즉 이 시점부터 서버는 "소켓 하나"가 아니라 "아직 등록되지 않았지만 곧 등록될 수 있는 사용자"를 다루기 시작한다.

서버 루프의 큰 뼈대는 놀랄 만큼 비슷하다. [`Server::_run_event_loop()`](../../../irc-track/01-roomlab/cpp/src/Server.cpp)는 여전히 accept/read/write 세 갈래로 나뉘지만, read branch 안에서 `Parser::make_messages()`로 batch를 만들고 `Executor::process()`에 넘기는 순간 runtime과 parser가 실제 상태 전이와 연결된다.

subset 범위가 실제로 어디까지인지 보여 주는 장면도 바로 그 dispatcher 안에 있다.

```cpp
case Message::PASS:    _execute_pass(server, node, *it); break;
case Message::NICK:    _execute_nick(server, node, *it); break;
case Message::USER:    _execute_user(server, node, *it); break;
case Message::JOIN:    _execute_join(server, node, *it); break;
case Message::PART:    _execute_part(server, node, *it); break;
case Message::PRIVMSG: _execute_privmsg(server, node, *it); break;
```

흥미로운 점은 `Executor.cpp` 안에 `CAP`, `TOPIC`, `INVITE`, `KICK`, `MODE` helper 정의가 이미 있다는 사실이다. 하지만 roomlab에서 중요한 것은 helper의 존재가 아니라 dispatcher가 실제로 무엇을 열어 두는가다. 지금 노출된 표면은 registration, room lifecycle, delivery, ping/pong, quit까지다. capstone과의 경계는 바로 여기서 생긴다.

registration은 `PASS -> NICK -> USER` 세 단계로 고정된다. `_execute_pass()`는 password mismatch면 즉시 `to_doom()`으로 연결을 종료 대기 상태로 돌리고, `_execute_nick()`은 lowercase nick을 `nickdb`에 넣는다. 마지막 `_execute_user()`는 등록 완료 시 `001`부터 `005`까지 묶어 보낸다. 그래서 [`tests/test_roomlab.py`](../../../irc-track/01-roomlab/cpp/tests/test_roomlab.py)의 `register()` helper가 완료 신호로 `005`를 기다리는 것이다.

결국 roomlab의 첫 글은 "IRC 명령이 많다"는 인상을 주려는 문서가 아니다. `eventlab`의 runtime 위에 `Connection` 상태와 subset dispatcher를 얹어, 등록이 끝난 사용자만 다음 상태로 넘어가게 만드는 서버 앞면을 세우는 과정으로 읽는 편이 맞다.

