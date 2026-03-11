# eventlab C++ 구현

상태: `verified`  
기준일: `2026-03-11`

## 빌드와 테스트

```sh
make clean && make
make test
```

## 엔트리포인트

- [src/main.cpp](src/main.cpp): signal 처리와 서버 시작점

## 핵심 구현 파일

- [src/Server.cpp](src/Server.cpp): 연결 수명주기와 프로토콜 처리
- [src/EventManager.cpp](src/EventManager.cpp): readiness event 추상화
- [include/inc/EventManager.hpp](include/inc/EventManager.hpp): 이벤트 관리자 공개 표면

## 검증 파일

- [tests/test_eventlab.py](tests/test_eventlab.py): 두 클라이언트 smoke test
