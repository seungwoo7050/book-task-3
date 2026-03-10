# msglab 디버그 노트

이 문서는 현재 구현 기준으로, parser에서 특히 눈에 안 띄는 실패 지점을 다시 정리한 백업 노트다. 더 긴 작업 기록은 [../notion-archive/](../notion-archive/)에 남겨 두었다.

## 사례 1. prefix가 있으면 command가 엉뚱해지는 문제

### 증상

prefix가 없는 입력은 잘 되는데, `:nick!user@host PRIVMSG #cpp :hello` 같은 입력에서 command mapping이 이상해진다.

### 왜 위험한가

parser에서 command가 잘못 분류되면 그 위에 쌓이는 모든 executor와 상태 전이가 잘못된 전제 위에 놓인다. 작은 버그처럼 보여도 신뢰도를 크게 깎는다.

### 지금 확인할 파일

- [../cpp/src/Message.cpp](../cpp/src/Message.cpp)
- [../cpp/tests/test_parser.cpp](../cpp/tests/test_parser.cpp)

prefix를 읽은 뒤 임시 상태가 다음 토큰에 섞이지 않는지 보는 것이 핵심이다.

## 사례 2. partial line을 버리면 stream parser가 아닌 것이 된다

### 증상

입력이 여러 줄로 끊겨 들어올 때, 마지막 incomplete fragment가 사라져 다음 read cycle에서 이어지지 않는다.

### 왜 위험한가

이 문제는 짧은 단위 테스트만 보면 잘 안 드러난다. 하지만 실제 네트워크 입력은 항상 완전한 줄 단위로만 도착하지 않는다. partial line을 버리면 나중에 roomlab과 ircserv에서 parser를 다시 의심하게 된다.

### 지금 확인할 파일

- [../cpp/src/Parser.cpp](../cpp/src/Parser.cpp)
- [../cpp/tests/test_parser.cpp](../cpp/tests/test_parser.cpp)

현재 구현은 완전한 line만 소비하고, 마지막 fragment는 남겨 두는 방향으로 읽는 것이 좋다.

## 사례 3. parser가 다른 계층 상수와 구조를 끌고 다니는 문제

### 증상

parser만 떼어 놓은 것처럼 보이는데, 실제로는 서버 계층의 상수나 별도 프로토콜 구조 없이는 설명이 안 된다.

### 왜 위험한가

이 경우 `msglab`은 독립 과제가 아니라 서버 일부가 된다. 문서와 실제 구조가 다른 이야기를 하게 된다.

### 지금 확인할 파일

- [../cpp/src/Parser.cpp](../cpp/src/Parser.cpp)
- [../cpp/include/inc/Message.hpp](../cpp/include/inc/Message.hpp)

parser가 자기 규칙을 스스로 설명할 수 있어야 한다는 점을 계속 점검하는 것이 좋다.

## 다시 막히면 따를 순서

1. 입력을 frame 단위로 잘 자르는지 본다.
2. prefix와 command가 올바르게 정규화되는지 본다.
3. trailing과 validation이 기대한 에러를 내는지 본다.
