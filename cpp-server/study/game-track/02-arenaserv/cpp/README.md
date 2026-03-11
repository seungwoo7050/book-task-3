# arenaserv C++ 구현

상태: `verified`  
기준일: `2026-03-11`

## 빌드와 테스트

```sh
make clean && make
make test
```

## 엔트리포인트

- [src/main.cpp](src/main.cpp): 서버 시작점

## 핵심 구현 파일

- [src/Server.cpp](src/Server.cpp): 연결, queue, rejoin 처리
- [src/MatchEngine.cpp](src/MatchEngine.cpp): authoritative simulation 로직
- [src/EventManager.cpp](src/EventManager.cpp): non-blocking event loop
- [include/inc/Server.hpp](include/inc/Server.hpp): 서버 설정과 상태 저장 구조

## 검증 파일

- [tests/test_arenaserv.py](tests/test_arenaserv.py): multi-client smoke test
