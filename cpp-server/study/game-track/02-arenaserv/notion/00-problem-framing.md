# arenaserv 문제 프레이밍

## 왜 이 프로젝트가 game-server capstone인가

`arenaserv`는 복잡한 그래픽이나 배포 환경을 보여 주는 프로젝트가 아니다. 이 저장소에서 capstone이 되는 이유는, authoritative simulation과 네트워크 session continuity를 한 서버 안에서 설득력 있게 보여 주기 때문이다.

## 지금 풀어야 하는 질문

- reconnect는 왜 단순 편의 기능이 아니라 상태 연속성 설계의 핵심인가
- room queue, ready, in-round, finished를 어떤 state machine으로 묶을 것인가
- snapshot과 combat event를 어떤 수준까지 공개 계약으로 드러낼 것인가

## 성공 기준

- [../cpp/tests/test_arenaserv.py](../cpp/tests/test_arenaserv.py)가 2인, 3인, 4인 시나리오를 검증한다.
- [../cpp/src/Server.cpp](../cpp/src/Server.cpp)와 [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp)를 읽으면 네트워크와 판정 경계가 보인다.
- ticklab 대비 무엇이 실제 서버 책임으로 추가됐는지 설명할 수 있다.

## 포트폴리오 관점에서 중요하게 볼 것

- reconnect와 snapshot regeneration
- room state machine
- multi-client smoke test 증거
