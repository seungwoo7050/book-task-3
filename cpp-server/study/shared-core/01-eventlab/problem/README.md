# eventlab 문제

## 문제

non-blocking TCP 서버의 최소 event loop를 구현하고, 연결 수명주기를 다른 도메인 규칙 없이 관찰할 수 있어야 한다.

## 성공 기준

- 지정한 포트에서 listening socket을 연다.
- 여러 클라이언트를 accept하고 read/write 이벤트를 처리한다.
- 줄 단위 텍스트 프로토콜에서 `PING <token>`에 `PONG <token>`으로 응답한다.
- 일반 입력은 `ECHO <line>`으로 되돌린다.
- idle connection에 keep-alive를 보내고 응답이 없으면 정리한다.

## 현재 근거

- [../cpp/src/Server.cpp](../cpp/src/Server.cpp)
- [../cpp/src/EventManager.cpp](../cpp/src/EventManager.cpp)
- [../cpp/tests/test_eventlab.py](../cpp/tests/test_eventlab.py)
