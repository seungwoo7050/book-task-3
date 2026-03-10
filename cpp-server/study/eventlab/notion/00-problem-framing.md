# eventlab 문제 프레이밍

## 왜 이 lab이 먼저 필요한가

네트워크 서버를 처음 공부할 때 가장 흔한 실수는 프로토콜과 상태 전이를 너무 빨리 붙이는 것이다. 그러면 버그가 났을 때 지금 깨진 것이 event loop인지, parser인지, 상태 머신인지 구분하기 어렵다. `eventlab`은 그 혼란을 막기 위해 “연결 수명주기만 먼저 본다”는 목표로 시작한다.

## 지금 풀어야 하는 질문

- 서버는 새 연결을 언제 받고 언제 읽고 언제 끊는가
- non-blocking I/O에서 한 클라이언트가 느릴 때 다른 연결은 어떻게 보호되는가
- keep-alive는 어떤 수준에서 설계하는 것이 학습에 가장 도움이 되는가

## 성공 기준

- [../cpp/tests/test_eventlab.py](../cpp/tests/test_eventlab.py)가 두 클라이언트 접속, `ECHO`, `PING`/`PONG`, `QUIT`, keep-alive를 검증한다.
- [../cpp/src/Server.cpp](../cpp/src/Server.cpp)를 읽으면 accept, read, write, disconnect 경계가 눈에 보인다.
- 이후 `roomlab`으로 올라갈 때 “여기까지는 런타임 문제였다”라고 말할 수 있다.

## 미리 알고 있으면 좋은 것

- blocking vs non-blocking socket
- readiness 기반 이벤트 모델
- `accept`, `recv`, `send`, `close`의 기본 동작

## 포트폴리오 관점에서 남길 만한 질문

- 연결 수명주기를 한 장으로 설명할 수 있는가
- keep-alive를 왜 이 lab에서 이 정도까지만 다뤘는가
- smoke test가 어떤 동작 증거를 제공하는가
