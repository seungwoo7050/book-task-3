# msglab 문제

## 문제

줄 단위 메시지를 안전하게 frame으로 자르고, parser가 구조화해야 할 정보와 validation이 맡아야 할 책임을 분리해야 한다.

## 성공 기준

- `\r\n` 또는 `\n` 경계를 기준으로 메시지를 분리한다.
- optional prefix를 인식한다.
- command token을 대문자로 정규화한다.
- trailing parameter를 `:<text>` 규칙 그대로 보존한다.
- nickname과 channel 이름의 유효성을 검사한다.

## 현재 근거

- [../cpp/include/inc/Message.hpp](../cpp/include/inc/Message.hpp)
- [../cpp/src/Parser.cpp](../cpp/src/Parser.cpp)
- [../cpp/tests/test_parser.cpp](../cpp/tests/test_parser.cpp)
