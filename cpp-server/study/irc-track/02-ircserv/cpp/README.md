# ircserv C++ 구현

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

- [src/Executor.cpp](src/Executor.cpp): advanced IRC command 처리
- [src/Channel.cpp](src/Channel.cpp): mode, invite, operator state
- [src/Server.cpp](src/Server.cpp): event loop와 keep-alive
- [include/inc/Server.hpp](include/inc/Server.hpp): 서버 설정과 내부 데이터베이스 공개 표면

## 검증 파일

- [tests/test_irc_join.py](tests/test_irc_join.py): capstone smoke test
