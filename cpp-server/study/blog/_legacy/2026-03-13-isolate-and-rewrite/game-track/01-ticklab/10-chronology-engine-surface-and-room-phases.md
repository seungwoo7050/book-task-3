# 10 Engine Surface And Room Phases

## Day 1
### Session 1

- 목표: `ticklab`이 gameplay toy가 아니라 room phase를 가진 authoritative engine인지 먼저 확인한다.
- 진행: `README`, `problem/README.md`, `MatchEngine.hpp`, `queue_player`, `ready_player`, `start_countdown`, `start_round`를 이어서 읽었다.
- 이슈: 처음엔 hit 판정이 중심일 줄 알았지만, 실제로는 `Lobby -> Countdown -> InRound -> Finished`를 어떻게 끊김 없이 넘길지가 먼저였다.
- 판단: 이 lab의 첫 질문은 projectile mechanics보다 "match phase를 network 없이 어떻게 관찰할까"였다.

CLI:

```bash
$ cd study/game-track/01-ticklab/cpp
$ sed -n '1,200p' README.md
$ sed -n '1,220p' include/inc/MatchEngine.hpp
$ rg -n "queue_player|ready_player|start_countdown|start_round|Phase" src/MatchEngine.cpp
$ sed -n '110,260p' src/MatchEngine.cpp
```

이 시점의 핵심 코드는 ready가 countdown으로 넘어가는 문턱이었다.

```cpp
it->second.ready = true;
if (static_cast<int>(this->room_order_.size()) >= min_players && this->all_room_players_ready())
    this->start_countdown();
```

처음엔 방에 두 명만 들어오면 자동 시작되는 줄 알았는데, 실제로는 `min_players`뿐 아니라 `all_room_players_ready()`까지 만족해야 countdown이 열린다. 그래서 이 lab은 단순 turn simulation이 아니라 lobby coordination까지 엔진이 직접 갖고 간다.

같은 흐름은 phase 전환 이벤트에서도 보인다.

```cpp
this->phase_ = Phase::Countdown;
this->emit_room("ROOM " + this->room_id_ + " countdown");
```

나중에 보니 `ticklab`은 "규칙 계산기"보다 "room state machine"이라는 표현이 더 맞았다.

