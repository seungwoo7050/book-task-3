# eventlab C++ 구현

상태: `verified`  
2026-03-10 기준 `make clean && make test`를 다시 확인했다.

## 이 구현이 맡는 범위

- single-process non-blocking TCP server
- accept/read/write cycle
- line-based `ECHO`, `PING`/`PONG`, `QUIT`
- idle keep-alive와 disconnect 정리

## 아직 다루지 않는 것

- IRC parser와 command dispatcher
- channel state와 multi-room 관리
- 제품 수준의 protocol negotiation

## 빌드와 테스트

```sh
make clean && make
make test
```

## 코드 읽기 포인트

- [src/main.cpp](src/main.cpp): signal 처리와 서버 시작점
- [src/Server.cpp](src/Server.cpp): 연결 수명주기와 프로토콜 처리
- [src/EventManager.cpp](src/EventManager.cpp): readiness event 추상화
- [tests/test_eventlab.py](tests/test_eventlab.py): 두 클라이언트 smoke test

## 포트폴리오로 옮길 때 보여 줄 증거

- `PING`/`PONG`, `QUIT`, keep-alive가 실제로 동작하는 테스트 로그
- 서버가 왜 최소 텍스트 프로토콜만으로도 학습 가치가 있는지 설명하는 그림
- 이후 `roomlab`이나 `ircserv`로 넘어갈 때 추가될 책임 목록
