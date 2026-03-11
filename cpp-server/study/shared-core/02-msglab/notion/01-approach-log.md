# msglab 접근 기록

## 처음 세운 원칙

이 lab은 반드시 "서버를 띄우지 않아도 parser를 믿을 수 있다"는 상태까지 가야 했다. 이 원칙 하나가 이후 선택을 거의 다 결정했다.

## 실제로 비교한 선택지

### 선택지 A. 이전 버전 parser를 거의 그대로 가져와서 의존성만 맞춘다

가장 빠른 길이다. 하지만 이 접근은 parser가 서버 상수와 다른 계층의 흔적을 계속 끌고 다니게 만든다. 그러면 `msglab`은 parser 과제가 아니라 "서버 일부를 떼어낸 과제"처럼 보이기 쉽다.

### 선택지 B. parser가 자기 규칙을 스스로 정의하는 독립 lab로 만든다

이 방법을 택했다. [../cpp/src/Parser.cpp](../cpp/src/Parser.cpp)와 [../cpp/include/inc/Message.hpp](../cpp/include/inc/Message.hpp)만으로 line split, command normalization, validation을 읽을 수 있게 두었다.

이 선택으로 얻은 장점은 분명했다.

- parser를 네트워크와 분리해 빠르게 테스트할 수 있다.
- 이후 `roomlab`과 `ircserv`에서도 같은 책임 경계를 유지할 수 있다.
- 학생이 "문자열 문제"와 "상태 전이 문제"를 따로 생각하게 도와준다.

## validator를 어디에 둘 것인가

여기서 두 번째 중요한 선택이 있었다.

- validator를 executor 쪽에 두면 registration 시점과 더 자연스럽게 붙는 것처럼 보인다.
- 하지만 invalid token은 가능한 빨리 드러나는 편이 학습에 유리하다.

그래서 이번 버전에서는 nickname, channel 이름 같은 최소 규칙을 parser 가까이에 둔다. 이 덕분에 parser lab이 너무 비어 보이지 않고, 에러 위치도 더 빨리 좁힐 수 있다.

## 테스트를 어떻게 설계했는가

[../cpp/tests/test_parser.cpp](../cpp/tests/test_parser.cpp)는 단순한 happy path 모음이 아니다. 적어도 네 층으로 나누어 읽는 편이 좋다.

1. prefix와 trailing parameter parsing
2. validator 통과와 실패 케이스
3. partial line 보존
4. 실제 상위 lab이 쓸 transcript command mapping

이렇게 나누면 parser 버그가 생겼을 때 어느 층이 깨졌는지 바로 좁힐 수 있다.

## 일부러 하지 않은 선택

- executor를 같이 넣지 않았다.
- socket I/O fixture를 만들지 않았다.
- numeric reply builder 전체를 이 lab의 범위로 잡지 않았다.

이것들은 모두 의미 있는 주제지만, 현재 질문보다 범위를 크게 만든다.

## 학생이 가져가면 좋은 기준

- parser 과제를 독립시켰다면, 그 이유가 코드 구조에 실제로 보여야 한다.
- validation은 "어디서 에러를 더 빨리 드러낼 수 있는가" 기준으로 배치하는 편이 좋다.
- transcript 테스트는 단순 문자열 비교가 아니라 책임 경계 검증 도구다.

## 읽기 추천 경로

1. [../cpp/include/inc/Message.hpp](../cpp/include/inc/Message.hpp)
2. [../cpp/src/Parser.cpp](../cpp/src/Parser.cpp)
3. [../cpp/tests/test_parser.cpp](../cpp/tests/test_parser.cpp)
