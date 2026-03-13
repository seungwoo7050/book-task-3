# arenaserv Source-First Blog

`arenaserv`은 `ticklab`과 `rollbacklab`의 engine 규칙을 다시 설명하는 문서가 아니다. 오히려 이미 검증된 simulation과 correction 규칙을 TCP 서버에 올릴 때, timed event loop와 session bridge가 어떤 책임을 새로 떠안는지 보여 주는 capstone에 가깝다. 같은 규칙을 쓴다는 점은 같지만, transport를 붙이는 순간 새로 생기는 문제는 전혀 다르다.

이 시리즈는 그 차이를 source-first로 다시 읽는다. 근거는 [`problem/README.md`](../../../game-track/03-arenaserv/problem/README.md), [`cpp/README.md`](../../../game-track/03-arenaserv/cpp/README.md), [`docs/README.md`](../../../game-track/03-arenaserv/docs/README.md), 실제 소스, 테스트, 그리고 직접 실행한 CLI뿐이다. 특히 simulation core는 `ticklab`에서, correction 맥락은 `rollbacklab`에서 이미 검증한 뒤 여기로 올라왔다는 사실이 이 문서의 출발점이 된다.

## 검증 명령

```sh
cd /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/03-arenaserv/cpp
make clean && make test
```

최근 확인 결과:

- `python3 tests/test_arenaserv.py`
- `arenaserv smoke passed.`

## 읽기 순서

- [00-series-map.md](00-series-map.md)
- [evidence-ledger.md](evidence-ledger.md)
- [structure-plan.md](structure-plan.md)
- [10-server-surface-and-session-handshake.md](10-server-surface-and-session-handshake.md)
- [20-queue-ready-and-engine-bridge.md](20-queue-ready-and-engine-bridge.md)
- [30-input-rejoin-and-room-events.md](30-input-rejoin-and-room-events.md)

## 핵심 근거 파일

- [`cpp/include/inc/EventManager.hpp`](../../../game-track/03-arenaserv/cpp/include/inc/EventManager.hpp)
- [`cpp/src/EventManager.cpp`](../../../game-track/03-arenaserv/cpp/src/EventManager.cpp)
- [`cpp/src/Server.cpp`](../../../game-track/03-arenaserv/cpp/src/Server.cpp)
- [`cpp/src/MatchEngine.cpp`](../../../game-track/03-arenaserv/cpp/src/MatchEngine.cpp)
- [`cpp/tests/test_arenaserv.py`](../../../game-track/03-arenaserv/cpp/tests/test_arenaserv.py)
