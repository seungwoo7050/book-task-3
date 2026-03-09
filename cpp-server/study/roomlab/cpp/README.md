# C++17 Implementation

상태: `verified`

## Problem Scope Covered

- raw TCP IRC registration
- room create/join/part lifecycle
- `PRIVMSG`/`NOTICE` delivery
- `PING`/`PONG`, `QUIT`, duplicate nick rejection

## Build Command

```sh
make clean && make
```

## Test Command

```sh
make test
```

## Known Gaps

- `TOPIC`, `MODE`, `KICK`, `INVITE`, `CAP`는 intentionally unsupported다.
- TLS, SASL, services integration은 없다.

## Implementation Notes

- WebSocket/game/store/metrics 흔적은 제거했다.
- 바이너리 이름은 `roomlabd`다.
- 테스트는 두 클라이언트 이상을 붙여 registration, broadcast, error path를 확인한다.
