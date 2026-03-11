# eventlab 개념 메모

이 디렉터리는 `eventlab`의 문제를 다시 소개하는 곳이 아니라, 왜 런타임을 이렇게 잘라서 설명했는지 정리하는 곳이다.

## 먼저 볼 질문

- readiness 기반 I/O는 blocking I/O와 무엇이 다른가
- keep-alive를 애플리케이션 계약으로 다루면 어떤 경계가 생기는가
- smoke test만으로도 연결 수명주기를 어디까지 검증할 수 있는가

## 읽기 포인트

- [../cpp/src/EventManager.cpp](../cpp/src/EventManager.cpp)
- [../cpp/src/Server.cpp](../cpp/src/Server.cpp)
- [../cpp/tests/test_eventlab.py](../cpp/tests/test_eventlab.py)

## 다음 단계

- 입력 경계를 이어서 보려면 [../../02-msglab/README.md](../../02-msglab/README.md)
