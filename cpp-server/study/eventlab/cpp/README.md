# C++17 Implementation

상태: `verified`

## Problem Scope Covered

- single-process non-blocking TCP server
- accept/read/write cycle
- line-based echo and `PING`/`PONG`
- idle keep-alive ping and disconnect

## Build Command

```sh
make clean && make
```

## Test Command

```sh
make test
```

## Known Gaps

- IRC command parsing은 하지 않는다.
- channel state는 없다.
- application protocol은 lab용 최소 텍스트 규약만 제공한다.

## Implementation Notes

- `EventManager`는 `legacy/`의 cross-platform 추상화를 재사용한다.
- keep-alive timeout은 smoke test를 위해 짧게 설정했다.
- 바이너리 이름은 `eventlabd`다.
