# msglab C++ 구현

상태: `verified`  
2026-03-10 기준 `make clean && make test`를 다시 확인했다.

## 이 구현이 맡는 범위

- IRC line parsing
- prefix, command, params, trailing extraction
- nickname/channel validation
- arena command에도 재사용할 수 있는 generic parsing helper

## 아직 다루지 않는 것

- network I/O
- numeric reply builder 전체의 library 분리
- command execution과 state mutation

## 빌드와 테스트

```sh
make clean && make
make test
```

## 코드 읽기 포인트

- [include/inc/Message.hpp](include/inc/Message.hpp): parser 결과 구조
- [src/Parser.cpp](src/Parser.cpp): line split, command normalization, validation helper
- [tests/test_parser.cpp](tests/test_parser.cpp): transcript-style parser test

## 포트폴리오로 옮길 때 보여 줄 증거

- parser가 partial line을 어떻게 보존하는지 설명하는 예시
- validation을 parser 층에서 드러내면 어떤 버그를 더 빨리 잡는지에 대한 테스트 사례
- 네트워크 코드 없이도 충분히 강한 테스트 세트를 만들 수 있다는 점
