# msglab

## 이 lab이 푸는 문제

문자열 처리 버그가 네트워크 버그처럼 보이면 뒤쪽 서버 lab 전체가 흐려진다. `msglab`은 parser와 validation을 네트워크 I/O에서 떼어 내어, 입력 경계만 독립적으로 검증할 수 있게 만든다.

## 내가 만든 답

- `Message` 모델과 `Parser` 유틸리티로 line framing을 분리한다.
- prefix, command, params, trailing parameter를 구조화한다.
- nickname/channel validation과 partial line 보존을 transcript 테스트로 검증한다.

## 범위 밖

- socket read/write
- IRC command 실행기
- room state와 connection lifetime

## 검증 방법

- 상태: `verified`
- 기준일: `2026-03-11`
- 위치: [cpp/README.md](cpp/README.md)

```sh
cd cpp
make clean && make test
```

## 핵심 파일

- [problem/README.md](problem/README.md)
- [cpp/include/inc/Message.hpp](cpp/include/inc/Message.hpp)
- [cpp/src/Parser.cpp](cpp/src/Parser.cpp)
- [cpp/tests/test_parser.cpp](cpp/tests/test_parser.cpp)

## Source-First Blog

- 실제 소스와 테스트만으로 다시 읽는 chronology는 [../../blog/shared-core/02-msglab/README.md](../../blog/shared-core/02-msglab/README.md)에서 이어진다.

## 다음 단계

- parser 결과를 실제 상태 전이와 합치는 답은 [../../irc-track/01-roomlab/README.md](../../irc-track/01-roomlab/README.md)
