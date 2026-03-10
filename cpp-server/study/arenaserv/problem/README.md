# arenaserv 문제 재구성

이 문서는 현재 저장소의 구현, 테스트, 보존된 기록을 바탕으로 다시 정리한 학습용 문제 설명이다. 목표는 제품 전체를 만드는 것이 아니라, authoritative game server의 핵심 계약을 가장 작은 capstone으로 보여 주는 것이다.

## 학습 목표

- pure TCP 환경에서 session continuity와 reconnect를 다룬다.
- room queue, ready, in-round, finished를 하나의 상태 머신으로 설계한다.
- snapshot, hit, elimination, round end를 authoritative 이벤트로 노출한다.

## 구현해야 할 것

- `HELLO`, `QUEUE`, `READY`, `INPUT`, `PING`, `REJOIN`, `LEAVE`
- `WELCOME`, `ROOM`, `COUNTDOWN`, `SNAPSHOT`, `HIT`, `ELIM`, `ROUND_END`, `ERROR`
- 20x20 bounded tile arena, 2~4인 room, HP 3, 단일 action `FIRE`
- 10초 reconnect grace

## 산출물

- authoritative TCP arena server
- bot/script 기반 2인, 3인, 4인 smoke test

## 범위에서 제외하는 것

- UDP, client prediction, rollback
- room shard, persistence, metrics
- 외부 매치메이킹과 운영 배포

## 현재 저장소에서 확인할 수 있는 근거

- [../cpp/src/Server.cpp](../cpp/src/Server.cpp): 네트워크 루프와 session 처리
- [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp): authoritative simulation
- [../cpp/tests/test_arenaserv.py](../cpp/tests/test_arenaserv.py): multi-client smoke test
- [../notion-archive/00-problem-framing.md](../notion-archive/00-problem-framing.md): 이전 문제 정의 메모 백업
