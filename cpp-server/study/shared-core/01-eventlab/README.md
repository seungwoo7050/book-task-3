# eventlab

## 이 lab이 푸는 문제

네트워크 서버 학습을 시작할 때 event loop, parser, 상태 전이를 한 번에 붙이면 지금 깨진 것이 어느 층의 문제인지 알기 어렵다. `eventlab`은 그 혼선을 줄이기 위해 연결을 받고 읽고 쓰고 끊는 최소 런타임만 먼저 다룬다.

## 내가 만든 답

- single-process non-blocking TCP 서버를 만든다.
- `ECHO`, `PING`/`PONG`, `QUIT`, keep-alive만으로 연결 수명주기를 검증한다.
- 두 클라이언트 smoke test로 accept/read/write/disconnect 흐름을 확인한다.

## 범위 밖

- IRC parser와 command dispatch
- channel state와 registration
- authoritative simulation과 게임 규칙

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
- [cpp/src/Server.cpp](cpp/src/Server.cpp)
- [cpp/src/EventManager.cpp](cpp/src/EventManager.cpp)
- [cpp/tests/test_eventlab.py](cpp/tests/test_eventlab.py)

## Source-First Blog

- 실제 소스와 테스트만으로 다시 읽는 chronology는 [../../blog/shared-core/01-eventlab/README.md](../../blog/shared-core/01-eventlab/README.md)에서 이어진다.

## 다음 단계

- 입력을 구조화하는 답을 보려면 [../02-msglab/README.md](../02-msglab/README.md)
