# C++17 Implementation

상태: `verified`

## Problem Scope Covered

- authoritative room state machine
- fixed-step countdown과 round tick
- input validation, stale sequence rejection
- reconnect grace and snapshot regeneration
- deterministic transcript-driven tests

## Build Command

```sh
make clean && make
```

## Test Command

```sh
make test
```

## Known Gaps

- 네트워크 I/O는 포함하지 않는다.
- projectile physics는 단일 tile grid와 단일 action `FIRE`로 제한한다.

## Implementation Notes

- `MatchEngine`은 room, players, projectiles, round phase를 한 곳에 둔다.
- countdown과 grace window는 tick 기반으로 계산한다.
- 테스트 바이너리 이름은 `ticklab_tests`다.
