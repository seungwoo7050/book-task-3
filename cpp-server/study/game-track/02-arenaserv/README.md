# arenaserv

## 이 lab이 푸는 문제

게임 서버 capstone을 설명할 때 화려한 기능보다 중요한 것은 authoritative 상태와 세션 연속성을 어디까지 설계하고 검증했는가다. `arenaserv`는 `eventlab`의 런타임과 `ticklab`의 simulation을 다시 합쳐, pure TCP capstone을 최소 범위로 보여 준다.

## 내가 만든 답

- `HELLO`, `QUEUE`, `READY`, `INPUT`, `REJOIN`, `LEAVE`를 처리하는 pure TCP 서버를 만든다.
- room queue, countdown, in-round, finished를 하나의 상태 머신으로 묶는다.
- snapshot, hit, elimination, round end, reconnect grace를 multi-client smoke test로 검증한다.

## 범위 밖

- UDP, client prediction, rollback
- room shard, persistence, metrics, external matchmaking
- 여러 active room 동시 운영

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
- [cpp/src/Server.cpp](cpp/src/Server.cpp)
- [cpp/src/MatchEngine.cpp](cpp/src/MatchEngine.cpp)
- [cpp/tests/test_arenaserv.py](cpp/tests/test_arenaserv.py)

## Source-First Blog

- 실제 소스와 테스트만으로 다시 읽는 chronology는 [../../blog/game-track/02-arenaserv/README.md](../../blog/game-track/02-arenaserv/README.md)에서 이어진다.

## 다음 단계

- 같은 저장소의 다른 capstone은 [../../irc-track/02-ircserv/README.md](../../irc-track/02-ircserv/README.md)
