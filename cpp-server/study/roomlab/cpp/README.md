# roomlab C++ 구현

상태: `verified`  
2026-03-10 기준 `make clean && make test`를 다시 확인했다.

## 이 구현이 맡는 범위

- raw TCP IRC registration
- room create/join/part lifecycle
- `PRIVMSG`, `NOTICE` 전달
- `PING`/`PONG`, `QUIT`, duplicate nick rejection

## 아직 다루지 않는 것

- `TOPIC`, `MODE`, `KICK`, `INVITE`, `CAP`
- TLS, SASL, services integration
- 제품 수준의 persistence와 운영 기능

## 빌드와 테스트

```sh
make clean && make
make test
```

## 코드 읽기 포인트

- [src/Connection.cpp](src/Connection.cpp): 연결별 상태 저장
- [src/Executor.cpp](src/Executor.cpp): core command 처리
- [src/execute_join.cpp](src/execute_join.cpp): room lifecycle
- [tests/test_roomlab.py](tests/test_roomlab.py): registration과 broadcast smoke test

## 포트폴리오로 옮길 때 보여 줄 증거

- duplicate nick과 room broadcast를 재현하는 테스트 캡처
- registration 전후로 허용 명령이 달라지는 상태 전이 표
- `ircserv`에서 어떤 고급 명령을 추가했는지 연결해 설명한 문서
