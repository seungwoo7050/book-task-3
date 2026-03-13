# 20 Queue Ready And Engine Bridge

## Day 1
### Session 2

- 목표: `ticklab`의 engine이 `arenaserv` 안에서 어떻게 socket world와 이어지는지 확인한다.
- 진행: `pump_ticks`, `handle_queue`, `handle_ready`, `dispatch_engine_events`, `EventManager` timeout surface를 함께 읽었다.
- 이슈: 처음엔 server가 직접 room state를 들고 있을 줄 알았는데, 실제로는 queue/ready 자체도 engine에 위임하고 server는 event routing만 맡는다.
- 판단: 이 프로젝트의 두 번째 답은 "게임 규칙을 서버로 옮긴다"가 아니라 "엔진 이벤트를 socket reply로 재배선한다"는 쪽에 있다.

CLI:

```bash
$ cd study/game-track/02-arenaserv/cpp
$ rg -n "pump_ticks|handle_queue|handle_ready|dispatch_engine_events|retrieve_events" src/Server.cpp include/inc/EventManager.hpp
$ sed -n '60,220p' src/Server.cpp
$ sed -n '1,160p' include/inc/EventManager.hpp
```

이 시점의 핵심 코드는 tick pump와 engine event dispatch를 따로 두는 구조였다.

```cpp
while (this->last_tick_ms + tick_interval_ms <= now)
{
    this->engine.advance_one_tick();
    this->dispatch_engine_events();
    this->last_tick_ms += tick_interval_ms;
}
```

처음엔 `recv`가 들어올 때만 world가 움직일 것 같았는데, 실제로는 `retrieve_events(newq, this->sendq, sentq, events, 50)` 뒤에 별도 `pump_ticks()`가 돌아서 입력이 없어도 countdown과 round tick이 계속 전진한다. 이 선택 덕분에 authoritative timeline이 client traffic과 분리된다.

같은 구조는 room events를 돌려보낼 때도 유지된다.

```cpp
const std::vector<std::string> room_tokens = this->engine.room_tokens();
for (std::vector<std::string>::const_iterator token_it = room_tokens.begin(); token_it != room_tokens.end(); ++token_it)
{
    std::map<std::string, int>::iterator found = this->token_to_fd.find(*token_it);
    if (found == this->token_to_fd.end())
        continue;
    std::map<int, Client>::iterator client_it = this->clients.find(found->second);
    if (client_it == this->clients.end())
        continue;
    this->queue_reply(client_it->second, it->line + "\r\n");
}
```

나중에 보니 `arenaserv`에서 server가 새로 만든 것은 simulation이 아니라, simulation event를 연결별 send buffer로 fan-out하는 bridge였다.
