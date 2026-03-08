# C++ Implementation

## Scope

- Full BOJ 5430 problem scope
- Maintained as a comparison implementation under the repository C++ retention policy

## Build Command

- `make -C ../problem run-cpp`

## Test Command

- `make -C ../problem run-cpp`
- `make -C ../problem run-py` 결과와 fixture 출력이 일치해야 한다.

## Current Status

- verified

## Known Gaps

- Dedicated C++ automated test target is not separate from the fixture runner.
- macOS에서는 compiler override가 필요할 수 있다.

## Implementation Notes

- 이 구현은 gold 문제와 cross-check anchor(`1753`, `1197`)에만 유지한다.
- shared fixture는 `../problem/data/`를 사용한다.
