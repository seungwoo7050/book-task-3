# eventlab Source-First Blog

`eventlab`은 이 저장소에서 가장 먼저 읽을 만한 서버 실험이다. 여기서 풀고 싶은 문제는 단순하다. IRC나 게임 규칙을 얹기 전에, 연결을 받고 읽고 쓰고 끊는 최소 non-blocking TCP runtime이 어디까지여야 하는가를 먼저 고정해 두자는 것이다.

이 시리즈는 그 과정을 소스와 테스트만으로 다시 따라간다. 근거는 [`problem/README.md`](../../../shared-core/01-eventlab/problem/README.md), [`cpp/README.md`](../../../shared-core/01-eventlab/cpp/README.md), [`docs/README.md`](../../../shared-core/01-eventlab/docs/README.md), 실제 소스, 그리고 직접 실행한 CLI뿐이다. 정확한 저장 시각은 남아 있지 않아서 chronology는 `Phase` 단위로 복원했지만, 각 phase가 어디서 시작되고 어떤 테스트 장면에서 닫히는지는 코드로 바로 따라갈 수 있다.

## 검증 명령

```sh
cd /Users/woopinbell/work/book-task-3/cpp-server/study/shared-core/01-eventlab/cpp
make clean && make test
```

최근 확인 결과:

- `python3 tests/test_eventlab.py`
- `eventlab smoke passed.`

## 읽기 순서

- [00-series-map.md](00-series-map.md)
- [evidence-ledger.md](evidence-ledger.md)
- [structure-plan.md](structure-plan.md)
- [10-runtime-surface-and-event-loop.md](10-runtime-surface-and-event-loop.md)
- [20-line-protocol-and-keepalive.md](20-line-protocol-and-keepalive.md)
- [30-smoke-verification-and-boundaries.md](30-smoke-verification-and-boundaries.md)

## 핵심 근거 파일

- [`cpp/include/inc/EventManager.hpp`](../../../shared-core/01-eventlab/cpp/include/inc/EventManager.hpp)
- [`cpp/src/EventManager.cpp`](../../../shared-core/01-eventlab/cpp/src/EventManager.cpp)
- [`cpp/src/Server.cpp`](../../../shared-core/01-eventlab/cpp/src/Server.cpp)
- [`cpp/tests/test_eventlab.py`](../../../shared-core/01-eventlab/cpp/tests/test_eventlab.py)

