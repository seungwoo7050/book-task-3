# roomlab 접근 기록

## 가장 먼저 정한 질문

`roomlab`을 시작할 때 가장 중요한 질문은 "작은 IRC 서버를 보여 주는가"가 아니라 "어디까지를 이 lab의 공식 범위로 삼을 것인가"였다. 이 경계를 잘못 잡으면 capstone과 차이가 흐려진다.

## 실제로 비교한 선택지

### 선택지 A. 더 큰 서버 구조를 거의 그대로 들고 와서 기능만 숨긴다

이 방법은 구현량이 적다. 하지만 읽는 사람 입장에서는 곧바로 문제가 생긴다.

- 코드 안에 범위 밖 기능의 흔적이 너무 많이 남는다.
- "이 필드는 지금 쓰이나"를 계속 확인해야 한다.
- lab이 아니라 축소판 제품처럼 보인다.

### 선택지 B. core IRC subset만 공식 범위로 남긴다

이 방법을 택했다. 그래서 command surface를 `PASS`, `NICK`, `USER`, `JOIN`, `PART`, `PRIVMSG`, `NOTICE`, `PING`, `PONG`, `QUIT`로 제한했다.

이 선택으로 얻은 장점은 분명했다.

- registration state machine을 한 번에 설명할 수 있다.
- room lifecycle이 어떤 자료구조와 cleanup 규칙을 요구하는지 선명하게 보인다.
- `ircserv`에서 무엇이 추가되는지가 비교 가능해진다.

## 구조를 어떻게 나눴는가

- [../cpp/src/Connection.cpp](../cpp/src/Connection.cpp): 연결별 상태
- [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp): core command 처리
- [../cpp/src/execute_join.cpp](../cpp/src/execute_join.cpp): room create, join, part
- [../cpp/tests/test_roomlab.py](../cpp/tests/test_roomlab.py): multi-client smoke test

핵심은 "room lifecycle을 한 파일로 분리해 읽는 사람이 상태 전이를 따라가기 쉽게 만든다"는 점이었다.

## 테스트를 어떻게 설계했는가

이 lab에서 단순히 JOIN이 되는지만 보면 부족하다. smoke test는 적어도 다음 여섯 가지를 함께 확인해야 한다고 봤다.

1. registration 완료
2. duplicate nick rejection
3. JOIN과 PART
4. channel broadcast
5. QUIT cleanup broadcast
6. not-on-channel error

이 시나리오가 함께 있어야 "작은 서버지만 상태 전이는 충분히 검증된다"라고 말할 수 있다.

## 일부러 하지 않은 선택

- `TOPIC`, `MODE`, `KICK`, `INVITE`, `CAP`는 여기 넣지 않았다.
- parser 책임을 다시 이 lab에 흡수하지 않았다.
- 서비스 계층, persistence, 운영 기능을 넣지 않았다.

이것들은 모두 중요한 주제지만, 지금 질문은 "등록과 room lifecycle을 실제 서버에서 보여 주는 것"이다.

## 학생이 가져가면 좋은 기준

- subset 프로젝트일수록 "무엇을 안 다루는가"를 적극적으로 적는다.
- 상태 전이는 command 목록보다 자료구조 정리와 cleanup 순서로 설명하는 편이 강하다.
- capstone으로 가는 사다리를 만들고 싶다면, 현재 lab의 범위를 더 넓히기보다 비교 가능하게 유지하는 편이 좋다.

## 읽기 추천 경로

1. [../cpp/src/Connection.cpp](../cpp/src/Connection.cpp)
2. [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp)
3. [../cpp/src/execute_join.cpp](../cpp/src/execute_join.cpp)
4. [../cpp/tests/test_roomlab.py](../cpp/tests/test_roomlab.py)
