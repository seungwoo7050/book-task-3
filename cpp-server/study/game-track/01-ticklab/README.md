# ticklab

## 이 lab이 푸는 문제

게임 서버를 바로 소켓 위에 올리면 네트워크 문제와 규칙 문제가 함께 보인다. `ticklab`은 authoritative simulation을 headless 엔진으로 먼저 고정해, 게임 규칙 자체를 transport 없이 검증할 수 있게 만든다.

## 내가 만든 답

- fixed-step match engine을 만든다.
- stale input rejection, reconnect grace, snapshot regeneration을 엔진 레벨에서 처리한다.
- deterministic transcript 테스트로 상태 전이를 검증한다.

## 범위 밖

- socket I/O
- client prediction과 rollback
- multi-room shard와 persistence

## 검증 방법

- 상태: `verified`
- 기준일: `2026-03-11`
- 위치: [cpp/README.md](cpp/README.md)

```sh
cd cpp
make clean && make test
```

## 핵심 파일

- [problem/README.md](problem/README.md)
- [cpp/include/inc/MatchEngine.hpp](cpp/include/inc/MatchEngine.hpp)
- [cpp/src/MatchEngine.cpp](cpp/src/MatchEngine.cpp)
- [cpp/tests/test_ticklab.cpp](cpp/tests/test_ticklab.cpp)

## Source-First Blog

- 실제 소스와 테스트만으로 다시 읽는 chronology는 [../../blog/game-track/01-ticklab/README.md](../../blog/game-track/01-ticklab/README.md)에서 이어진다.

## 다음 단계

- 다음 단계는 [../02-rollbacklab/README.md](../02-rollbacklab/README.md)에서 late input correction과 rollback을 붙이는 것이다.
