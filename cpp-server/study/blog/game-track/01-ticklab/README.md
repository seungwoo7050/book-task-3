# ticklab Source-First Blog

`ticklab`은 게임 서버 문서지만, 소켓 이야기를 거의 하지 않는다. 여기서 먼저 고정하고 싶은 것은 transport가 아니라 authoritative simulation의 핵심 규칙이다. room queue, ready, countdown, fixed tick, projectile, reconnect grace 같은 판단을 네트워크 없이 먼저 확인해 두면, 뒤의 capstone이 무엇을 새로 더하는지 훨씬 맑게 보인다.

이 시리즈는 그 과정을 source-first로 다시 읽는다. 근거는 [`problem/README.md`](../../../game-track/01-ticklab/problem/README.md), [`cpp/README.md`](../../../game-track/01-ticklab/cpp/README.md), [`docs/README.md`](../../../game-track/01-ticklab/docs/README.md), 실제 소스, 테스트, 그리고 직접 실행한 CLI뿐이다. chronology는 `Phase` 단위로 복원했지만, `MatchEngine`이 어떻게 phase machine에서 reconnect policy까지 커지는지는 코드 흐름 그대로 드러난다.

## 검증 명령

```sh
cd /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/01-ticklab/cpp
make clean && make test
```

최근 확인 결과:

- `./ticklab_tests`
- `ticklab tests passed.`

## 읽기 순서

- [00-series-map.md](00-series-map.md)
- [evidence-ledger.md](evidence-ledger.md)
- [structure-plan.md](structure-plan.md)
- [10-engine-surface-and-room-phases.md](10-engine-surface-and-room-phases.md)
- [20-input-ticks-and-projectiles.md](20-input-ticks-and-projectiles.md)
- [30-rejoin-timeout-and-verification.md](30-rejoin-timeout-and-verification.md)

## 핵심 근거 파일

- [`cpp/include/inc/MatchEngine.hpp`](../../../game-track/01-ticklab/cpp/include/inc/MatchEngine.hpp)
- [`cpp/src/MatchEngine.cpp`](../../../game-track/01-ticklab/cpp/src/MatchEngine.cpp)
- [`cpp/tests/test_ticklab.cpp`](../../../game-track/01-ticklab/cpp/tests/test_ticklab.cpp)
- [`problem/data/arena-transcript.txt`](../../../game-track/01-ticklab/problem/data/arena-transcript.txt)

