# ircserv 접근 기록

## 먼저 정한 정체성

`ircserv`에서 가장 중요한 질문은 "이 프로젝트가 이전 구현의 복원인가, 아니면 커리큘럼의 통합 capstone인가"였다. 이 질문에 대한 답이 애매하면 범위가 계속 커진다.

이번 버전은 분명히 두 번째를 택했다. 즉 `ircserv`는 `eventlab`, `msglab`, `roomlab`에서 나눈 경계를 다시 한 서버로 합치는 capstone이다.

## 실제로 고정한 구조

- core server 흐름은 `roomlab` 위에 둔다.
- advanced IRC command는 [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp)와 [../cpp/src/Channel.cpp](../cpp/src/Channel.cpp)에 집중시킨다.
- smoke test는 [../cpp/tests/test_irc_join.py](../cpp/tests/test_irc_join.py)에서 세 클라이언트 역할을 통해 실제 호환성 경로를 검증한다.

## 왜 세 클라이언트를 쓰는가

`alice`, `bob`, `carol` 세 역할이 있어야 다음이 분명해진다.

- operator 역할
- 일반 member 역할
- invite를 받고 합류하는 guest 역할

이 셋이 있어야 `MODE +i`, `INVITE`, `KICK`, 재입장 거절 같은 시나리오를 한 smoke test에서 설득력 있게 묶을 수 있다.

## 일부러 하지 않은 선택

- full IRCv3 capability negotiation
- TLS, SASL, operator services
- 게임 관련 확장이나 운영 배포 주제

이것들은 전부 가치 있지만, 지금 capstone의 목적은 "IRC 축을 한 프로젝트로 통합해 보이는 것"이지 기능 최대화가 아니다.

## 이 선택의 장점과 대가

장점:

- `roomlab`과의 차이를 분명하게 설명할 수 있다.
- command surface를 늘리더라도 책임 경계가 완전히 흐려지지 않는다.
- 학생이 자기 포트폴리오에서 "왜 이 범위까지를 capstone으로 잡았는가"를 설명하기 쉬워진다.

대가:

- 현대 IRC 전체 구현이라고 부를 수는 없다.
- 호환성도 최소 범위만 다룬다.
- smoke test는 강하지만 exhaustive compliance suite는 아니다.

## 학생이 가져가면 좋은 기준

- capstone은 기능 수가 아니라 통합 방식으로 설명하는 편이 강하다.
- subset 프로젝트와의 비교 표가 문서 설명력을 크게 올린다.
- 실제 클라이언트 시나리오를 그대로 테스트로 옮기면 README 신뢰도가 높아진다.

## 읽기 추천 경로

1. [../cpp/src/Channel.cpp](../cpp/src/Channel.cpp)
2. [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp)
3. [../cpp/src/Server.cpp](../cpp/src/Server.cpp)
4. [../cpp/tests/test_irc_join.py](../cpp/tests/test_irc_join.py)
