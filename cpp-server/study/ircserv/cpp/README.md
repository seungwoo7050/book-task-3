# ircserv C++ 구현

상태: `verified`  
2026-03-10 기준 `make clean && make test`를 다시 확인했다.

## 이 구현이 맡는 범위

- pure TCP IRC server
- `roomlab` 범위의 core command
- `CAP`, `TOPIC`, `MODE`, `KICK`, `INVITE`
- `005 ISUPPORT` advertisement

## 아직 다루지 않는 것

- TLS, SASL, operator services
- full IRCv3 capability negotiation
- 운영 배포 concern

## 빌드와 테스트

```sh
make clean && make
make test
```

## 코드 읽기 포인트

- [src/Executor.cpp](src/Executor.cpp): advanced IRC command 처리
- [src/Channel.cpp](src/Channel.cpp): mode, invite, operator state
- [src/Server.cpp](src/Server.cpp): event loop와 keep-alive
- [tests/test_irc_join.py](tests/test_irc_join.py): capstone smoke test

## 포트폴리오로 옮길 때 보여 줄 증거

- `CAP`, `MODE +i`, `INVITE`, `TOPIC`, `KICK`가 통과하는 smoke test 로그
- roomlab 대비 추가된 상태 전이와 권한 체크 설명
- “왜 여기까지를 capstone 범위로 잡았는가”에 대한 범위 판단 기록
