# C++17 Implementation

상태: `verified`

## Problem Scope Covered

- IRC line parsing
- generic line parsing for arena commands
- prefix/command/params/trailing extraction
- nickname/channel validation
- transcript-style parser tests and arena input validation helpers

## Build Command

```sh
make clean && make
```

## Test Command

```sh
make test
```

## Known Gaps

- network I/O는 포함하지 않는다.
- numeric reply builder 전체를 별도 library로 분리하지는 않았다.

## Implementation Notes

- parser는 partial line을 보존한다.
- arena command는 `HELLO`, `INPUT`, `REJOIN` 같은 generic command로 파싱하고, 의미 검증은 별도 helper로 둔다.
- 테스트 바이너리 이름은 `msglab_tests`다.
