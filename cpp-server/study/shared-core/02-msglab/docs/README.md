# msglab 개념 메모

이 디렉터리는 parser 문제를 다시 소개하지 않는다. 대신 parser를 독립 lab으로 떼었을 때 어떤 책임 경계가 생기는지 정리한다.

## 먼저 볼 질문

- trailing parameter는 왜 마지막 하나만 공백을 보존하는가
- partial line을 버리지 않으면 어떤 종류의 버그를 피할 수 있는가
- validator를 parser 근처에 두면 executor는 얼마나 단순해지는가

## 읽기 포인트

- [../cpp/src/Parser.cpp](../cpp/src/Parser.cpp)
- [../cpp/include/inc/Message.hpp](../cpp/include/inc/Message.hpp)
- [../cpp/tests/test_parser.cpp](../cpp/tests/test_parser.cpp)

## 다음 단계

- parser 결과를 연결 상태와 합치는 흐름은 [../../../irc-track/01-roomlab/README.md](../../../irc-track/01-roomlab/README.md)
