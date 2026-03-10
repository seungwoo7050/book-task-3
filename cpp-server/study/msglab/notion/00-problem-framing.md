# msglab 문제 프레이밍

## 왜 parser를 먼저 떼어 보는가

네트워크 프로그램에서 문자열 처리 버그는 연결 버그처럼 보일 때가 많다. `msglab`은 그 혼선을 줄이기 위해, parser와 validator를 독립된 학습 대상으로 분리한다.

## 지금 풀어야 하는 질문

- 줄 경계는 어디서 자르고 어디까지 보존해야 하는가
- parser가 할 일과 executor가 할 일은 어디서 갈라지는가
- 작은 fixture만으로 parser를 믿을 수 있게 만들려면 무엇이 필요할까

## 성공 기준

- [../cpp/tests/test_parser.cpp](../cpp/tests/test_parser.cpp)가 line split, prefix, command, trailing, validation을 검증한다.
- [../cpp/src/Parser.cpp](../cpp/src/Parser.cpp)를 읽으면 parser 책임과 validation 책임이 보인다.
- 이후 `roomlab`에서 네트워크 코드가 parser 문제를 대신 설명하지 않게 된다.

## 포트폴리오 관점에서 중요하게 볼 것

- parser를 독립시킨 이유
- transcript 테스트를 어떻게 설계했는지
- partial line 보존이 왜 필요한지
