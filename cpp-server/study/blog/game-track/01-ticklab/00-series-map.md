# ticklab series map

이 시리즈는 `ticklab`을 "게임 로직 일부"가 아니라 transport 없이 authoritative simulation을 먼저 고정하는 lab으로 다시 읽기 위한 지도다.

## 이 프로젝트가 답하는 질문

- room queue, ready, countdown, in-round, finished 같은 상태 전이를 network 없이 먼저 어떻게 검증할까
- stale input rejection, projectile hit, reconnect grace를 엔진 레벨에서 먼저 막으면 서버 capstone은 무엇에 집중할 수 있을까

## 읽는 순서

1. [10-chronology-engine-surface-and-room-phases.md](10-chronology-engine-surface-and-room-phases.md)
2. [20-chronology-input-ticks-and-projectiles.md](20-chronology-input-ticks-and-projectiles.md)
3. [30-chronology-rejoin-timeout-and-verification.md](30-chronology-rejoin-timeout-and-verification.md)

## 참조한 실제 파일

- `study/game-track/01-ticklab/README.md`
- `study/game-track/01-ticklab/problem/README.md`
- `study/game-track/01-ticklab/problem/data/arena-transcript.txt`
- `study/game-track/01-ticklab/cpp/README.md`
- `study/game-track/01-ticklab/cpp/Makefile`
- `study/game-track/01-ticklab/cpp/include/inc/MatchEngine.hpp`
- `study/game-track/01-ticklab/cpp/src/MatchEngine.cpp`
- `study/game-track/01-ticklab/cpp/tests/test_ticklab.cpp`
- `study/game-track/01-ticklab/docs/README.md`

## Canonical CLI

```bash
cd study/game-track/01-ticklab/cpp
make clean && make test
```

## Git Anchor

- `2026-03-09 73372bd Add project: backend-fastapi, backend-spring, cpp-server`
- `2026-03-10 7dc71a8 docs: enhance cpp-server`
- `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`

## 추론 원칙

- chronology는 `MatchEngine` public API와 transcript fixture가 먼저 드러내는 room phase를 기준으로 잡고, 이후 input validation, projectile/hit 처리, rejoin grace로 확장한다.
- 이 문서는 socket이나 event loop를 설명하지 않고, 엔진이 혼자서 어디까지 authoritative rule을 고정하는지에만 집중한다.

