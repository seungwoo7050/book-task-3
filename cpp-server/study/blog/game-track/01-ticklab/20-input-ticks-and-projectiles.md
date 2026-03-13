# ticklab 2. input, tick, projectile를 authoritative 순서로 처리하기

room phase가 고정되면 다음 질문은 자연스럽다. 언제 어떤 입력을 받아들이고, 같은 tick 안에서 어떤 순서로 world state를 advance할 것인가. `ticklab`에서 authoritative 성격이 가장 또렷해지는 순간도 바로 여기다.

기준점은 [`submit_input()`](../../../game-track/01-ticklab/cpp/src/MatchEngine.cpp)이다. 이 함수는 단순히 이동값을 저장하지 않는다. 현재 phase가 `InRound`인지, 플레이어가 room 안에 있고 살아 있는지, `seq`가 이전보다 증가하는지, 이동이 한 칸 orthogonal move인지, facing이 `N/E/S/W`인지부터 먼저 확인한다.

```cpp
if (input.seq <= participant.last_seq)
{
    error = Error("stale_sequence", "input sequence must increase monotonically");
    return false;
}
```

이후 [`advance_one_tick()`](../../../game-track/01-ticklab/cpp/src/MatchEngine.cpp)이 authoritative 순서를 정한다. countdown phase면 숫자를 줄이거나 round를 시작하고, in-round phase면 `process_inputs()` -> `move_projectiles()` -> `SNAPSHOT` emission -> `maybe_finish_round()` 순서로 진행한다. 플레이어 위치 갱신과 투사체 판정, snapshot이 이 순서로 묶이기 때문에 외부에서 보는 state가 일관성을 갖는다.

`process_inputs()`는 pending input을 읽어 위치와 facing을 갱신하고, `fire`가 켜져 있으면 현재 바라보는 방향 기준으로 projectile을 만든다. `move_projectiles()`는 그 projectile를 한 칸씩 전진시키며 충돌을 검사하고, 맞은 대상에겐 `HIT`, HP가 0 이하가 되면 `ELIM`을 emit한다. 마지막 `maybe_finish_round()`는 살아 있는 플레이어 수가 1명 이하가 되면 승자를, `max_round_ticks`를 넘기면 draw를 기록한다.

이 흐름에서 [`snapshot_json()`](../../../game-track/01-ticklab/cpp/src/MatchEngine.cpp)이 하는 일도 크다. snapshot은 room, phase, tick, 각 플레이어의 좌표와 HP, alive/connected 상태, projectile 위치까지 모두 담는다. 그래서 테스트는 내부 필드를 직접 들여다보지 않고도, 나중에 서버가 외부로 보내게 될 상태를 같은 모양으로 확인할 수 있다.

결국 이 글의 초점은 물리 계산의 디테일 자체보다 acceptance order에 있다. 어떤 입력을 같은 tick에 반영할지, 어떤 시점에 snapshot을 찍을지, 어떤 조건에서 round를 끝낼지를 엔진이 먼저 고정해 두기 때문에, 뒤에서 transport를 붙여도 authoritative 기준은 흔들리지 않는다.

