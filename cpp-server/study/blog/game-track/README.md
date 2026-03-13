# game-track blog

이 트랙의 blog 시리즈는 authoritative game server를 설명할 때 simulation 규칙과 network session continuity를 왜 분리해서 읽어야 하는지 프로젝트 단위로 복원한다. chronology는 공통으로 `problem/README.md`, `cpp/Makefile`, `cpp/include/inc`, `cpp/src`, `cpp/tests`, `docs/README.md`를 읽고, `ticklab -> arenaserv` 순서가 그대로 의존관계를 드러내도록 구성했다.

## 프로젝트

| 프로젝트 | blog | 원 프로젝트 |
| --- | --- | --- |
| ticklab | [README.md](01-ticklab/README.md) | [../../game-track/01-ticklab/README.md](../../game-track/01-ticklab/README.md) |
| arenaserv | [README.md](02-arenaserv/README.md) | [../../game-track/02-arenaserv/README.md](../../game-track/02-arenaserv/README.md) |

## 읽는 순서

1. [ticklab](01-ticklab/README.md)로 headless simulation, stale input rejection, reconnect grace를 먼저 본다.
2. [arenaserv](02-arenaserv/README.md)로 queue, countdown, tick pump, rejoin bridge가 TCP server 안에서 어떻게 합쳐지는지 본다.
3. 공용 런타임을 다시 보려면 [../shared-core/README.md](../shared-core/README.md), 다른 capstone 비교는 [../irc-track/README.md](../irc-track/README.md)로 이동한다.

## source-first 메모

- `ticklab`과 `arenaserv`는 `MatchEngine` 이름을 공유하므로 chronology도 "엔진 단독 검증"과 "엔진을 서버로 올린 뒤 새로 생기는 책임"을 의도적으로 분리한다.
- 이 트랙은 화려한 게임 기능보다 `authoritative state`, `reconnect grace`, `snapshot regeneration`을 핵심 증거로 삼는다.
- 현재 git anchor는 저장소 단위뿐이라, 세부 흐름은 `arena-transcript.txt`, `MatchEngine` API, multi-client smoke test 시나리오를 기준으로 보수적으로 복원한다.

