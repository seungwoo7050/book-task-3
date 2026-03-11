# ticklab C++ 구현

상태: `verified`  
기준일: `2026-03-11`

## 빌드와 테스트

```sh
make clean && make
make test
```

## 엔트리포인트

- [tests/test_ticklab.cpp](tests/test_ticklab.cpp): 엔진 공개 표면을 직접 호출하는 검증 시작점

## 핵심 구현 파일

- [include/inc/MatchEngine.hpp](include/inc/MatchEngine.hpp): 핵심 타입과 인터페이스
- [src/MatchEngine.cpp](src/MatchEngine.cpp): tick advance, hit, elimination, reconnect 처리
- [tests/test_ticklab.cpp](tests/test_ticklab.cpp): 엔진 상태 전이를 직접 검증하는 fixture

## 검증 파일

- [tests/test_ticklab.cpp](tests/test_ticklab.cpp): deterministic 검증 시나리오
