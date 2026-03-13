# ticklab 1. engine 표면과 room phase부터 고정하기

`ticklab`의 첫 번째 선택은 게임 서버를 바로 소켓 위에 올리지 않는 것이다. [`problem/README.md`](../../../game-track/01-ticklab/problem/README.md)가 요구하는 것도 network 없는 authoritative simulation이고, 그래서 시작점은 클라이언트 연결이 아니라 [`cpp/include/inc/MatchEngine.hpp`](../../../game-track/01-ticklab/cpp/include/inc/MatchEngine.hpp)다.

헤더를 보면 엔진이 먼저 고정하고 싶은 대상이 분명하다. `Error`, `Input`, `Event`, `Participant`, `Projectile`, 그리고 `Phase` enum이 있다. 여기에 `board_width`, `board_height`, `max_players`, `max_hp`, `countdown_steps`, `grace_ticks`, `max_round_ticks` 같은 상수가 붙는다. 즉 이 엔진은 이미 "어떤 세션이 어떤 방에서 몇 tick 동안 어떤 phase를 거치며 싸우는가"를 네트워크 없이 설명할 수 있다.

실제 흐름은 [`cpp/src/MatchEngine.cpp`](../../../game-track/01-ticklab/cpp/src/MatchEngine.cpp)의 registration과 room phase 함수에서 열린다. `register_player()`는 nickname을 검증하고 `token-<n>` 형태의 세션 토큰을 발급한다. `queue_player()`는 사용자를 room에 넣고 `ROOM arena-1 lobby` 이벤트를 발행한다. 그리고 `ready_player()`는 최소 두 명이 모두 준비되면 `start_countdown()`을 부른다.

```cpp
if (static_cast<int>(this->room_order_.size()) >= min_players && this->all_room_players_ready())
    this->start_countdown();
```

그다음 `start_countdown()`은 `ROOM arena-1 countdown`과 `COUNTDOWN 3`을 밀어 넣고, `start_round()`는 phase를 `InRound`로 바꾸며 `SNAPSHOT 0 ...`까지 바로 emit한다. 눈에 띄는 점은 이 모든 변화가 엔진 이벤트 큐 안에서 닫힌다는 것이다. 아직 클라이언트 소켓도, 직렬화 계층도 없지만, 외부는 `drain_events()`만 호출하면 같은 장면을 그대로 볼 수 있다.

이게 중요한 이유는 뒤의 TCP capstone이 이 규칙을 다시 생각할 필요가 없기 때문이다. 서버는 나중에 이 이벤트를 네트워크로 중계하기만 하면 된다. 그래서 `ticklab`의 첫 글은 게임 규칙을 많이 소개하는 문서라기보다, phase machine과 event surface를 먼저 분리해 authoritative 판단의 바닥을 고정하는 글로 읽는 편이 맞다.

