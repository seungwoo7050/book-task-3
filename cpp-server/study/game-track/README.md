# game-track

## 이 트랙이 푸는 문제

authoritative 게임 서버를 설명할 때는 simulation 규칙과 네트워크 세션 연속성을 분리해서 보여 주는 편이 훨씬 낫다. 이 트랙은 headless simulation과 TCP capstone을 따로 검증해, 무엇이 게임 규칙 문제이고 무엇이 서버 문제인지 분명하게 만든다.

## 내가 만든 답

- [01-ticklab](01-ticklab/README.md)에서 fixed-step simulation, stale input rejection, reconnect grace를 headless 엔진으로 먼저 검증한다.
- [02-rollbacklab](02-rollbacklab/README.md)에서 late input correction, snapshot rollback, resimulation을 transport 없이 먼저 고정한다.
- [03-arenaserv](03-arenaserv/README.md)에서 room queue, snapshot, reconnect를 포함한 pure TCP capstone으로 다시 합친다.

## 포함 lab

| 순서 | lab | 답의 형태 |
| --- | --- | --- |
| 1 | [01-ticklab](01-ticklab/README.md) | deterministic match engine과 unit test |
| 2 | [02-rollbacklab](02-rollbacklab/README.md) | late input correction, rollback, resimulation을 다루는 headless lab |
| 3 | [03-arenaserv](03-arenaserv/README.md) | authoritative TCP arena server와 multi-client smoke test |

## 읽는 순서

1. [01-ticklab/README.md](01-ticklab/README.md)
2. [02-rollbacklab/README.md](02-rollbacklab/README.md)
3. [03-arenaserv/README.md](03-arenaserv/README.md)
4. 공용 런타임을 다시 보려면 [../shared-core/01-eventlab/README.md](../shared-core/01-eventlab/README.md)

## Source-First Blog

- 이 트랙의 chronology 입구는 [../blog/game-track/README.md](../blog/game-track/README.md)다.
