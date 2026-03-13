# arenaserv series map

이 시리즈는 `arenaserv`를 "게임 서버 하나"가 아니라, `eventlab`의 runtime과 `ticklab`의 simulation을 다시 합친 pure TCP capstone으로 다시 읽기 위한 지도다.

## 이 프로젝트가 답하는 질문

- token-based session handshake, room queue, countdown, in-round snapshot을 TCP server 안에서 어떻게 묶을까
- rejoin grace와 stale input rejection을 engine 쪽에 두면서도 multi-client smoke test로 무엇을 끝까지 검증할 수 있을까

## 읽는 순서

1. [10-chronology-server-surface-and-session-handshake.md](10-chronology-server-surface-and-session-handshake.md)
2. [20-chronology-queue-ready-and-engine-bridge.md](20-chronology-queue-ready-and-engine-bridge.md)
3. [30-chronology-input-rejoin-and-room-events.md](30-chronology-input-rejoin-and-room-events.md)
4. [40-chronology-multi-client-verification-and-boundaries.md](40-chronology-multi-client-verification-and-boundaries.md)

## 참조한 실제 파일

- `study/game-track/02-arenaserv/README.md`
- `study/game-track/02-arenaserv/problem/README.md`
- `study/game-track/02-arenaserv/cpp/README.md`
- `study/game-track/02-arenaserv/cpp/Makefile`
- `study/game-track/02-arenaserv/cpp/include/inc/Server.hpp`
- `study/game-track/02-arenaserv/cpp/include/inc/EventManager.hpp`
- `study/game-track/02-arenaserv/cpp/include/inc/MatchEngine.hpp`
- `study/game-track/02-arenaserv/cpp/src/Server.cpp`
- `study/game-track/02-arenaserv/cpp/src/MatchEngine.cpp`
- `study/game-track/02-arenaserv/cpp/tests/test_arenaserv.py`
- `study/game-track/02-arenaserv/docs/README.md`

## Canonical CLI

```bash
cd study/game-track/02-arenaserv/cpp
make clean && make test
```

## Git Anchor

- `2026-03-09 73372bd Add project: backend-fastapi, backend-spring, cpp-server`
- `2026-03-10 7dc71a8 docs: enhance cpp-server`
- `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`

## 추론 원칙

- chronology는 `Server::handle_line`이 여는 command surface를 먼저, 그다음 `pump_ticks`와 `dispatch_engine_events`가 engine을 socket world로 연결하는 흐름을 읽고, 이후 rejoin/input failure path와 smoke verification 순으로 복원한다.
- `MatchEngine.cpp`는 이미 `ticklab`에서 읽었다는 전제를 두고, 여기서는 "같은 엔진이 서버 상태와 어떻게 결합되는가"를 중심으로만 참조한다.

