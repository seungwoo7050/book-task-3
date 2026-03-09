# msglab Docs

## Key Concepts

- trailing parameter는 마지막 하나만 전체 공백 문자열을 보존한다.
- parser는 partial line을 버리지 않고 다음 read cycle까지 남겨야 한다.
- channel validation과 nickname validation은 실행기보다 parser/validator 레이어에서 먼저 드러내는 편이 낫다.

## Reference Pointers

- `legacy/src/Message.cpp`
- `legacy/src/Parser.cpp`
- `legacy/src/inc/macros.hpp`
