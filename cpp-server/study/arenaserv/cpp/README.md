# arenaserv C++ 구현

상태: `verified`  
2026-03-10 기준 `make clean && make test`를 다시 확인했다.

## 이 구현이 맡는 범위

- pure TCP authoritative arena server
- session token 발급과 reconnect grace
- single-room queue, ready, countdown, in-round, finished state machine
- snapshot, hit, elimination, round end broadcast
- 2인, 3인, 4인 smoke test

## 아직 다루지 않는 것

- UDP, client prediction, rollback
- room shard, persistence, metrics, external matchmaking
- 여러 active room 동시 운영

## 빌드와 테스트

```sh
make clean && make
make test
```

## 코드 읽기 포인트

- [src/Server.cpp](src/Server.cpp): 연결, queue, rejoin 처리
- [src/MatchEngine.cpp](src/MatchEngine.cpp): authoritative simulation 로직
- [src/EventManager.cpp](src/EventManager.cpp): non-blocking event loop
- [tests/test_arenaserv.py](tests/test_arenaserv.py): multi-client smoke test

## 포트폴리오로 옮길 때 보여 줄 증거

- reconnect grace와 snapshot regeneration을 재현하는 테스트 캡처
- ticklab 대비 서버 쪽으로 올라오며 추가된 책임 목록
- authoritative state machine을 한 장의 상태 다이어그램으로 정리한 설명
