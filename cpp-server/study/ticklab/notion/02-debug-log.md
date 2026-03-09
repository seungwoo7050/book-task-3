# ticklab — 디버그 기록: sequence 검증, reconnect snapshot, draw 타이밍

작성일: 2026-03-09

## 문제 1: stale sequence가 조용히 덮어써졌다

### 어떻게 발견했는가

`test_stale_sequence_and_validation`을 작성하는 과정에서였다. 같은 seq number(1)로 입력을 두 번 보냈는데, 첫 번째 입력이 두 번째로 조용히 대체되었다. 에러도 없고, 무시도 없고, 그냥 마지막 값이 남았다.

이건 "last writer wins" 동작이고, 실제 게임에서는 위험하다. 클라이언트가 네트워크 지연으로 같은 패킷을 재전송하면, 서버가 이미 처리한 입력을 다시 적용하는 셈이 된다.

### 무엇이 문제였는가

`submit_input()`에서 pending input이 이미 있을 때 새 입력으로 교체하는 로직은 있었지만, **seq가 단조 증가하는지를 먼저 확인하는 guard가 없었다**. `last_seq` 비교 로직이 있긴 했으나, 함수 중간에 있어서 pending input을 덮어쓴 뒤에야 도달했다.

### 무엇을 했는가

`submit_input()`의 초입으로 `seq <= last_seq` 검사를 올렸다. 이 조건에 걸리면 `stale_sequence` 에러를 반환하고 함수를 즉시 종료한다. pending input은 건드리지 않는다.

```cpp
if (input.seq <= participant.last_seq)
{
    error = Error("stale_sequence", "input sequence must increase monotonically");
    return false;
}
```

### 검증

테스트에서 seq=1 입력을 두 번 보내면 두 번째가 `stale_sequence` 에러로 거절되는 것을 확인했다. 추가로, 대각선 이동(`dx=1, dy=1`)이 `invalid_input`으로 거절되는 것도 같은 테스트에서 확인했다.

## 문제 2: 재접속은 성공했지만, 현재 상태를 알 수 없었다

### 어떻게 발견했는가

`rejoin_player()`를 처음 구현했을 때는 단순히 `participant.connected = true`로 복구하는 것이 전부였다. 재접속 자체는 성공하는데, 재접속한 플레이어가 현재 게임이 어떤 상태인지 — 어떤 phase인지, 몇 번째 tick인지, 다른 플레이어들의 위치가 어디인지 — 전혀 알 수 없었다.

### 무엇을 했는가

`rejoin_player()`가 재접속 성공 시 상태 복구 이벤트를 자동으로 밀어주게 했다:

1. `WELCOME <token>` — 세션 복구 확인
2. `ROOM <room_id> <phase>` — 현재 room phase 알림
3. phase가 `countdown`이면 `COUNTDOWN <remaining>` 추가
4. phase가 `in_round` 또는 `finished`이면 `SNAPSHOT <tick> <json>` 추가

이렇게 하면 재접속한 클라이언트가 현재 상태를 완전히 복원할 수 있다.

### 검증

`test_rejoin_grace_window`에서 disconnect 후 50 tick 이내 rejoin이 성공하고, `grace_ticks + 1` 이후 rejoin이 `expired_session`으로 실패하는 것을 확인했다. snapshot 재전송은 drain_events()로 이벤트를 확인하는 방식으로 검증했다.

## 문제 3: timeout draw가 이벤트 없이 끝났다

### 어떻게 발견했는가

`test_draw_timeout`을 작성하면서였다. 양쪽 다 아무 행동도 하지 않으면 `max_round_ticks`(30 tick)에 도달해서 라운드가 끝나야 한다. 그런데 라운드가 끝나기는 하는데, `ROUND_END draw` 이벤트가 나오지 않았다.

### 무엇이 문제였는가

`advance_one_tick()` 안에서 snapshot을 emit한 뒤 라운드 종료 조건을 확인하는 순서가 잘못되어 있었다. snapshot emit과 종료 체크 사이에 early return이 있어서, 특정 조건에서 `maybe_finish_round()`가 호출되지 않는 경로가 있었다.

### 무엇을 했는가

`advance_one_tick()`의 마지막에 `maybe_finish_round()`를 **항상** 호출하도록 고정했다. 이 함수는 라운드가 끝났는지(생존자 0~1명이거나, round_tick이 max에 도달했는지)를 확인하고, 조건이 맞으면 `ROUND_END`를 emit한다.

```cpp
// advance_one_tick() 마지막
this->maybe_finish_round();
```

### 검증

`test_draw_timeout`에서 30 tick 전진 후 `ROUND_END draw` 이벤트가 정확히 발생하는 것을 확인했다.
