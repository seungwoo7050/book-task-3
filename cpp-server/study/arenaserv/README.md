# arenaserv

`arenaserv`는 게임 서버 축의 capstone이다. `eventlab`의 네트워크 루프와 `ticklab`의 authoritative simulation을 다시 합쳐, 2~4인 pure TCP arena server를 하나의 프로젝트로 보여 준다.

## 이 프로젝트가 가르치는 것

- session continuity와 reconnect를 서버 설계의 핵심 질문으로 다루는 방법
- room-based matchmaking과 in-round simulation을 한 state machine으로 묶는 방법
- snapshot, hit, elimination, round end를 네트워크 이벤트로 노출하는 방식

## 현재 범위

- 포함: `HELLO`, `QUEUE`, `READY`, `INPUT`, `REJOIN`, `LEAVE`, room queue, fixed tick combat, snapshot, reconnect grace
- 제외: UDP, prediction, rollback, persistence, external matchmaking

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [cpp/README.md](cpp/README.md)
3. [docs/README.md](docs/README.md)
4. [notion/README.md](notion/README.md)

## 포트폴리오로 확장할 때 보여 줄 것

- ticklab의 엔진이 실제 서버로 붙으면서 어떤 네트워크 책임이 생기는지 비교하기
- [cpp/tests/test_arenaserv.py](cpp/tests/test_arenaserv.py) 기반으로 multi-client smoke test 증거 남기기
- reconnect와 snapshot을 “유저 경험”이 아니라 “서버 상태 연속성” 관점에서 설명하기
