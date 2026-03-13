# 20 Input Ticks And Projectiles

## Day 1
### Session 2

- 목표: authoritative 판단이 실제로 어디서 일어나는지 input validation과 tick advance 흐름에서 확인한다.
- 진행: `submit_input`, `advance_one_tick`, `process_inputs`, `move_projectiles`, `maybe_finish_round`를 함께 읽었다.
- 이슈: 처음엔 projectile hit이 복잡성의 중심이라고 생각했는데, 실제로는 그 전에 `seq`, orthogonal move, facing validity를 잘라 내는 입력 계약이 더 결정적이었다.
- 판단: 이 lab의 두 번째 답은 "언제 발사체를 움직일까"보다 "어떤 입력만 authoritative하게 받아들일까"다.

CLI:

```bash
$ cd study/game-track/01-ticklab/cpp
$ rg -n "submit_input|advance_one_tick|process_inputs|move_projectiles|maybe_finish_round" src/MatchEngine.cpp
$ sed -n '180,420p' src/MatchEngine.cpp
```

이 시점의 핵심 코드는 stale sequence와 invalid move를 막는 분기였다.

```cpp
if (input.seq <= participant.last_seq)
{
    error = Error("stale_sequence", "input sequence must increase monotonically");
    return false;
}
if ((input.dx < -1 || input.dx > 1) || (input.dy < -1 || input.dy > 1) || (std::abs(input.dx) + std::abs(input.dy) > 1))
{
    error = Error("invalid_input", "movement must be at most one orthogonal tile");
    return false;
}
```

처음엔 client가 보내는 좌표만 그대로 적용하면 될 것 같았는데, 실제 엔진은 `last_seq`와 orthogonal movement 제약을 직접 들고 있어서 replay나 diagonal movement를 뒤쪽 서버가 아니라 여기서 끊는다.

이후 tick advance는 검증 흐름을 한 단계 더 단순하게 만든다.

```cpp
++this->round_tick_;
this->process_inputs();
this->move_projectiles();

{
    std::ostringstream oss;
    oss << "SNAPSHOT " << this->round_tick_ << " " << this->snapshot_json();
    this->emit_room(oss.str());
}
this->maybe_finish_round();
```

나중에 보니 `ticklab`의 핵심은 projectile 계산보다도 "tick마다 어떤 순서로 world를 굴릴 것인가"를 고정하는 데 있었다.
