# eventlab 개념 노트

## 먼저 잡아야 할 질문

- readiness 기반 I/O는 blocking I/O와 무엇이 다른가
- 새 연결은 언제 read 대상으로 등록해야 안전한가
- keep-alive는 transport 기능이 아니라 애플리케이션 계약으로도 설계할 수 있는가

## 코드 읽기 포인트

- [../cpp/src/EventManager.cpp](../cpp/src/EventManager.cpp): 이벤트 등록과 반환 방식
- [../cpp/src/Server.cpp](../cpp/src/Server.cpp): accept, recv, send, disconnect 분기
- [../cpp/tests/test_eventlab.py](../cpp/tests/test_eventlab.py): 현재 검증 순서

## 흔한 오해

- event loop를 이해하려면 IRC 기능까지 한 번에 읽어야 하는 것은 아니다.
- keep-alive는 꼭 정밀 타이머부터 도입해야 하는 주제가 아니다.
- 간단한 smoke test라도 연결 수명주기 전체를 검증하면 충분히 강한 증거가 된다.

## 다음 단계로 이어지는 지점

`eventlab`에서 확보한 것은 런타임 기반이다. 입력을 더 구조적으로 다루고 싶다면 다음으로 [../msglab/README.md](../msglab/README.md)를 읽으면 된다.
