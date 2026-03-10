# eventlab

`eventlab`은 이 커리큘럼의 출발점이다. IRC 명령이나 게임 규칙을 넣기 전에, 서버가 연결을 받고 읽고 쓰고 끊는 최소 단위를 먼저 떼어 내어 관찰한다.

## 이 프로젝트가 가르치는 것

- non-blocking socket과 event loop의 기본 연결 구조
- accept, read, write, disconnect가 한 루프 안에서 어떻게 이어지는지
- keep-alive를 애플리케이션 계층 heartbeat로 다루는 방법

## 현재 범위

- 포함: listening socket, 다중 연결 처리, `PING`/`PONG`, `ECHO`, idle disconnect
- 제외: IRC parser, channel state, 게임 규칙, 운영 배포 주제

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [cpp/README.md](cpp/README.md)
3. [docs/README.md](docs/README.md)
4. [notion/README.md](notion/README.md)

## 포트폴리오로 확장할 때 보여 줄 것

- 이벤트 루프가 연결 수명주기를 어떻게 관리하는지 한 장의 다이어그램으로 설명하기
- [cpp/tests/test_eventlab.py](cpp/tests/test_eventlab.py) 같은 smoke test를 근거로 “동작 증거”를 남기기
- `roomlab`이나 `ircserv`로 올라가기 전에 어떤 책임을 여기서 끝냈는지 분명하게 적기
