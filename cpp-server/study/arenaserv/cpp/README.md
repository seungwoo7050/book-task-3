# C++17 Implementation

상태: `verified`

## Problem Scope Covered

- pure TCP authoritative arena server
- session token 발급과 reconnect grace
- single-room queue/ready/countdown/in_round/finished state machine
- snapshot, hit, elimination, round end broadcast
- 2인, 3인, 4인 smoke test

## Build Command

```sh
make clean && make
```

## Test Command

```sh
make test
```

## Known Gaps

- UDP, client prediction, rollback은 다루지 않는다.
- room shard, persistence, metrics, external matchmaking은 없다.
- single active room만 지원한다.

## Implementation Notes

- 네트워크 I/O는 `EventManager` 기반 single-process non-blocking TCP loop로 처리한다.
- authoritative simulation은 `ticklab`과 동일한 `MatchEngine` 구조를 복제해 사용한다.
- 바이너리 이름은 `arenaserv`다.
