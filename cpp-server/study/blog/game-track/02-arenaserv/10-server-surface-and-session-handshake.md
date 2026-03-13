# arenaserv 1. timed event loop와 session handshake를 붙이기

`arenaserv`을 읽을 때 가장 먼저 붙잡아야 할 사실은 게임 규칙이 새로 쓰이지 않았다는 점이다. [`cpp/src/MatchEngine.cpp`](../../../game-track/02-arenaserv/cpp/src/MatchEngine.cpp)와 [`cpp/include/inc/MatchEngine.hpp`](../../../game-track/02-arenaserv/cpp/include/inc/MatchEngine.hpp)는 `ticklab`과 동일하다. 그래서 이 capstone의 새 일은 ruleset이 아니라, 그 ruleset이 시간을 잃지 않고 TCP 위에서 살아 움직이게 만드는 runtime surface 쪽에 있다.

그 변화는 [`cpp/src/EventManager.cpp`](../../../game-track/02-arenaserv/cpp/src/EventManager.cpp)와 [`cpp/src/Server.cpp`](../../../game-track/02-arenaserv/cpp/src/Server.cpp)에서 드러난다. `EventManager::retrieve_events()`는 `timeout_ms` 인자를 받아 `epoll_wait`나 `kevent` 대기 시간을 조절하고, `Server::run_event_loop()`는 매 loop 끝에서 `pump_ticks()`를 호출한다.

```cpp
while (this->last_tick_ms + tick_interval_ms <= now)
{
    this->engine.advance_one_tick();
    this->dispatch_engine_events();
    this->last_tick_ms += tick_interval_ms;
}
```

이제 서버는 더 이상 "소켓 이벤트가 있을 때만 움직이는 프로그램"이 아니다. 네트워크가 조용해도 countdown과 round timeout을 위해 tick은 계속 흘러야 한다. authoritative game server에서 runtime이 달라지는 첫 장면이 바로 여기다.

session handshake도 이 timed loop 위에 얹힌다. `Client` 구조체는 `fd`, `recvbuf`, `sendbuf` 옆에 `token`을 갖고, 서버는 별도로 `token_to_fd` 맵을 유지한다. `handle_hello()`가 `engine.register_player()`를 성공시키면, 새 token을 현재 fd와 연결하고 `dispatch_engine_events()`를 통해 `WELCOME token-n`을 전송한다. connection과 player session이 분리되기 시작하는 순간이다.

이 구조 덕분에 뒤의 `REJOIN`도 자연스럽게 설명된다. 새로운 TCP 연결이 들어와도 token만 같으면 같은 세션을 다시 붙일 수 있기 때문이다. 그래서 `arenaserv`의 첫 글은 게임 규칙 설명보다, 이미 검증한 authoritative engine이 TCP와 시간 의존 runtime 위에서도 흔들리지 않게 붙는 앞면을 만드는 이야기로 읽는 편이 맞다.

