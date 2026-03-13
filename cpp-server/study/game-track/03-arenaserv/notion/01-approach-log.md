# arenaserv 접근 기록

## 가장 먼저 고정한 질문

`arenaserv`에서 가장 중요한 질문은 "ticklab의 엔진을 어떻게 서버에 붙일 것인가"였다. 이 질문에 답하지 못하면 `ticklab`의 학습 가치도, `arenaserv`의 capstone 정체성도 흐려진다.

## 실제로 비교한 선택지

### 선택지 A. simulation과 네트워크를 처음부터 한 덩어리로 다시 만든다

이 방법은 결과물만 보면 깔끔해 보일 수 있다. 하지만 그러면 match rule bug와 socket bug가 다시 한곳에 섞인다. `ticklab`을 먼저 만든 이유가 사라진다.

### 선택지 B. 검증된 simulation 구조를 유지하고 서버 책임만 얹는다

이 방법을 택했다. [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp)는 authoritative simulation을 맡고, [../cpp/src/Server.cpp](../cpp/src/Server.cpp)는 소켓, 세션, 명령 해석, 이벤트 flush를 맡는다.

이 선택의 핵심은 "코드 재사용"보다 "책임 경계 유지"에 있다.

## tick scheduler를 어떻게 붙였는가

여기서 중요한 구현 판단이 하나 더 있었다.

- 별도 스레드에서 tick을 돌리면 동기화 문제가 생긴다.
- single-threaded event loop 안에서 timeout 기반으로 tick을 밀면 구조가 단순해진다.

이번 버전은 두 번째를 택했다. 그래서 네트워크와 tick advance를 한 루프 안에서 설명할 수 있다.

## reconnect를 어떻게 설계했는가

reconnect는 단순 토큰 인증으로 끝나지 않는다. 이 프로젝트에서는 token ownership과 socket ownership을 분리해 생각하는 편이 훨씬 중요했다.

- disconnect 시 세션 상태는 남길 수 있다.
- rejoin 시 새 fd를 세션에 다시 연결해야 한다.
- grace window를 넘기면 세션 자체를 만료시켜야 한다.

이 설계가 있어야 reconnect를 "편의 기능"이 아니라 상태 연속성 설계로 설명할 수 있다.

## smoke test를 왜 넓게 잡았는가

[../cpp/tests/test_arenaserv.py](../cpp/tests/test_arenaserv.py)는 2인 duel만 보는 테스트가 아니다.

- duplicate nick
- within-grace rejoin
- expired rejoin
- 3인 lobby
- 4인 lobby
- room overflow
- draw timeout

이 시나리오를 모두 넣어야 room state machine을 충분히 설명할 수 있다고 봤다.

## 일부러 하지 않은 선택

- UDP, prediction, rollback
- 여러 room shard와 metrics
- 제품 수준의 복잡한 게임 규칙

이것들은 분명 중요한 주제지만, 현재 capstone의 목적은 pure TCP authoritative server의 핵심 계약을 명확히 보여 주는 것이다.

## 학생이 가져가면 좋은 기준

- capstone에서도 "무엇을 재사용하고 무엇을 새로 붙였는가"를 분리해서 설명한다.
- reconnect는 반드시 상태 연속성 언어로 설명한다.
- multi-client smoke test는 가능한 한 서로 다른 종료 조건을 함께 포함한다.

## 읽기 추천 경로

1. [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp)
2. [../cpp/src/Server.cpp](../cpp/src/Server.cpp)
3. [../cpp/tests/test_arenaserv.py](../cpp/tests/test_arenaserv.py)
