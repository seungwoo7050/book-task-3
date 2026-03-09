# eventlab Problem

이 문서는 원본 과제 문서가 없는 상태에서 `legacy/` 코드를 바탕으로 재구성한 문제 설명이다.

## Reconstructed Prompt

C++17로 non-blocking TCP 서버를 만든다. 서버는 다음을 만족해야 한다.

- 지정한 포트에서 listening socket을 연다.
- 여러 클라이언트를 동시에 accept하고 read/write 이벤트를 처리한다.
- 줄 단위 텍스트 프로토콜을 사용한다.
- `PING <token>` 입력에 `PONG <token>`으로 응답한다.
- 일반 입력은 `ECHO <line>`으로 되돌린다.
- idle connection에는 keep-alive `PING`을 보내고, 응답이 없으면 끊는다.

## Deliverables

- event loop abstraction을 사용하는 C++17 서버
- 다중 연결 smoke test

## Provenance

| source | why it matters |
| --- | --- |
| `legacy/src/EventManager.cpp` | kqueue/epoll 추상화의 직접 출처 |
| `legacy/src/inc/EventManager.hpp` | 이벤트 타입과 API 표면의 출처 |
| `legacy/src/Server.cpp` | accept/read/write/keep-alive 흐름의 출처 |
| `legacy/src/main.cpp` | signal 처리 방식의 출처 |
| `legacy/src/utils.cpp` | socket send/recv helper의 출처 |
