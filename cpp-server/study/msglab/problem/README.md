# msglab Problem

이 문서는 원본 과제 문서가 없는 상태에서 `legacy/` 코드를 바탕으로 재구성한 문제 설명이다.

## Reconstructed Prompt

C++17로 IRC message parser를 작성한다. parser는 다음을 지원해야 한다.

- line stream에서 `\r\n` 또는 `\n` 경계를 찾아 메시지를 분리한다.
- optional prefix를 인식한다.
- command token을 대문자로 정규화한다.
- trailing parameter를 `:<text>` 규칙으로 보존한다.
- nickname과 channel 이름의 유효성을 검사한다.

## Deliverables

- `Message` 모델
- `Parser` 유틸리티
- golden transcript와 validator unit tests

## Provenance

| source | why it matters |
| --- | --- |
| `legacy/src/Message.cpp` | message tokenization 로직의 출처 |
| `legacy/src/Parser.cpp` | frame split과 string helper의 출처 |
| `legacy/src/inc/Message.hpp` | message data model의 출처 |
| `legacy/src/inc/Parser.hpp` | parser public API의 출처 |
| `legacy/src/inc/macros.hpp` | numeric reply formatting 규칙을 읽는 참고 자료 |
