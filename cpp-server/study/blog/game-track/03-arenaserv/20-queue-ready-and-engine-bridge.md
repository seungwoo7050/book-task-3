# arenaserv 2. queue, ready, 그리고 engine event bridge

timed loop와 session token이 생기면, 그다음 서버의 역할은 꽤 분명해진다. raw TCP command를 engine API에 연결하고, engine이 낸 event를 다시 적절한 소켓으로 fan-out 해야 한다. `arenaserv`의 중간 장면이 거의 전부 bridge 코드로 읽히는 이유도 바로 여기 있다.

[`Server::handle_line()`](../../../game-track/03-arenaserv/cpp/src/Server.cpp)은 명령어를 `HELLO`, `QUEUE`, `READY`, `INPUT`, `REJOIN`, `LEAVE`, `PING`, `QUIT`으로 나눈다. 이 중 `QUEUE`와 `READY`는 특히 얇다. 현재 연결에 세션 토큰이 있는지만 확인하고, 그다음은 그대로 `engine.queue_player()`와 `engine.ready_player()`를 부른다.

```cpp
if (!this->engine.queue_player(client.token, error))
{
    this->send_error(client, error.code, error.message);
    return;
}
this->dispatch_engine_events();
```

실제 중심은 [`dispatch_engine_events()`](../../../game-track/03-arenaserv/cpp/src/Server.cpp)에 있다. engine에서 drain한 event는 두 종류다. 특정 token 한 명에게만 가야 하는 `EventScope::Single`이 있고, room 안의 여러 token에게 fan-out 해야 하는 `EventScope::Room`이 있다. 서버는 `token_to_fd`를 이용해 이 token을 현재 살아 있는 소켓으로 다시 찾아낸다.

그래서 transport layer는 player state를 직접 들고 있지 않는다. engine이 상태를 알고, server는 그 상태에서 나온 event를 어느 fd로 보내야 하는지만 안다. 바로 이 분리가 중요한데, 덕분에 `ticklab`의 ruleset은 그대로 두면서도 TCP capstone을 얇게 유지할 수 있다.

`pump_ticks()`와 이 bridge가 만나면 countdown과 snapshot이 실제 네트워크 표면으로 나온다. 입력이 없어도 tick이 흐르고, tick이 흐르면 engine이 `COUNTDOWN`, `ROOM ... in_round`, `SNAPSHOT`을 emit하고, server는 그 event를 room의 각 fd로 뿌린다. [`tests/test_arenaserv.py`](../../../game-track/03-arenaserv/cpp/tests/test_arenaserv.py)의 `scenario_party_lobby()`가 이 경로를 그대로 확인한다. 3인과 4인 파티를 만들고 모두 `READY`를 누르면 `COUNTDOWN 3`과 `SNAPSHOT 0`이 오고, overflow 사용자는 `ERROR room_full`을 받는다.

결국 이 글의 초점은 command가 늘었다는 데 있지 않다. 이미 있는 engine event를 "누구에게 보내야 하는가"로 번역하는 bridge가 생겼고, 그 덕분에 headless proof가 TCP 표면까지 올라온다는 점이 더 중요하다.

