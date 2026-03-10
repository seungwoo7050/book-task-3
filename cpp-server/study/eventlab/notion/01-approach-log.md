# eventlab 접근 기록

## 가장 먼저 고정한 질문

`eventlab`에서 제일 먼저 정해야 했던 것은 "이 프로젝트가 서버 제품의 축소판인가, 아니면 event loop를 따로 읽게 해 주는 학습 도구인가"였다. 이 질문에 답하지 못하면 코드도 문서도 계속 흔들린다.

## 실제로 비교한 선택지

### 선택지 A. 기존 서버 구조를 거의 그대로 가져와서 IRC 부분만 덜어낸다

이 방법의 장점은 빠르다. accept, read, write, disconnect, keep-alive가 이미 한 파일 안에 있으니, 필요 없는 분기만 걷어내면 얼핏 그럴듯해 보인다.

하지만 학습용 프로젝트로 보면 단점이 더 컸다.

- event loop를 읽다가 곧바로 IRC 상태 머신의 흔적을 만나게 된다.
- "이 멤버 변수는 지금 쓰이는 것인가"를 계속 추적해야 한다.
- 결과물이 "최소 event loop"가 아니라 "이전 버전 서버의 축소판"처럼 보인다.

### 선택지 B. 이벤트 추상화만 유지하고 상위 서버는 새로 쓴다

이 방법을 택했다. 핵심은 [../cpp/src/EventManager.cpp](../cpp/src/EventManager.cpp) 같은 런타임 기반은 유지하되, [../cpp/src/Server.cpp](../cpp/src/Server.cpp)는 이 lab 질문만 답하게 다시 정리하는 것이다.

이 선택으로 얻은 장점은 분명했다.

- 읽는 사람이 accept, read, write, disconnect 경계를 바로 찾을 수 있다.
- 프로토콜을 `WELCOME`, `ECHO`, `PING`/`PONG`, `BYE`만으로 줄여 런타임 질문에 집중할 수 있다.
- 이후 `roomlab`과 `ircserv`로 갈 때 "여기까지는 event loop 문제였다"라고 선을 그을 수 있다.

### 선택지 C. 서버를 만들지 않고 이벤트 추상화만 단위 테스트한다

이 길도 잠깐 고려했다. 가장 가볍기 때문이다. 하지만 이 선택은 결국 버렸다.

- 커널 이벤트 API는 실제 socket과 함께 봐야 의미가 드러난다.
- accept에서 disconnect까지의 수명주기를 한 번에 관찰할 수 없다.
- 독립 lab처럼 보이더라도, 실제 서버 공부로 이어지는 감각이 약하다.

## 최종적으로 고정한 구조

- 런타임의 중심은 [../cpp/src/EventManager.cpp](../cpp/src/EventManager.cpp)와 [../cpp/src/Server.cpp](../cpp/src/Server.cpp)다.
- 프로토콜은 "연결 수명주기 관찰"에 필요한 최소 표면만 둔다.
- keep-alive는 복잡한 타이머 추상화 대신 현재 구조의 의미를 보여 주는 수준에서만 다룬다.
- 검증은 [../cpp/tests/test_eventlab.py](../cpp/tests/test_eventlab.py) 같은 end-to-end smoke test로 한다.

## 이 선택의 대가

- 정밀 타이머 의미론은 아직 다루지 않는다.
- 운영형 heartbeat 설계로 바로 이어지지는 않는다.
- write backpressure와 같은 주제는 최소 수준만 보여 준다.

하지만 이 대가를 치르더라도, 이 프로젝트가 "무엇을 가르치는가"가 선명해지는 편이 더 중요하다고 판단했다.

## 학생이 가져가면 좋은 기준

- 작은 프로젝트일수록 "무엇을 안 넣었는가"를 분명하게 적는다.
- smoke test는 짧더라도 수명주기 전체를 통과하게 설계한다.
- 다음 프로젝트가 맡을 책임을 현재 프로젝트 안으로 미리 끌어오지 않는다.

## 읽기 추천 경로

1. [../problem/README.md](../problem/README.md)로 범위를 고정한다.
2. [../cpp/src/Server.cpp](../cpp/src/Server.cpp)에서 accept, read, write, disconnect 경계를 읽는다.
3. [../cpp/tests/test_eventlab.py](../cpp/tests/test_eventlab.py)로 그 경계가 실제로 어떻게 검증되는지 대응시킨다.
