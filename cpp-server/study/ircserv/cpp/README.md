# C++17 Implementation

상태: `verified`

## Problem Scope Covered

- pure TCP IRC server
- `roomlab` 범위의 core commands
- `CAP`, `TOPIC`, `MODE`, `KICK`, `INVITE`
- `005 ISUPPORT` advertisement

## Build Command

```sh
make clean && make
```

## Test Command

```sh
make test
```

## Known Gaps

- TLS, SASL, operator services는 없다.
- IRCv3 capability negotiation은 최소 `CAP LS 302`만 다룬다.
- production deployment concern은 이 트랙 범위 밖이다.

## Implementation Notes

- WebSocket, game, store, metrics 코드는 제거했다.
- 바이너리 이름은 `ircserv`다.
- smoke test는 `CAP`, `MODE +i`, `INVITE`, `TOPIC`, `KICK`, `PING/PONG`까지 검증한다.
