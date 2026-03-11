# msglab C++ 구현

상태: `verified`  
기준일: `2026-03-11`

## 빌드와 테스트

```sh
make clean && make
make test
```

## 엔트리포인트

- [tests/test_parser.cpp](tests/test_parser.cpp): parser 공개 표면을 직접 호출하는 검증 시작점

## 핵심 구현 파일

- [include/inc/Message.hpp](include/inc/Message.hpp): parser 결과 구조
- [include/inc/Parser.hpp](include/inc/Parser.hpp): parser helper 선언
- [src/Parser.cpp](src/Parser.cpp): line split, 정규화, validation helper

## 검증 파일

- [tests/test_parser.cpp](tests/test_parser.cpp): transcript-style parser test
