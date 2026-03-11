# ticklab 문제

## 문제

authoritative simulation의 핵심 판단을 네트워크 없이 먼저 검증할 수 있어야 한다.

## 성공 기준

- room queue와 ready 기반 countdown을 처리한다.
- monotonic input sequence를 검증한다.
- fixed tick마다 state를 advance하고 snapshot을 생성한다.
- hit, elimination, round timeout draw를 판정한다.
- reconnect grace window와 snapshot 재전송을 처리한다.

## 현재 근거

- [../cpp/include/inc/MatchEngine.hpp](../cpp/include/inc/MatchEngine.hpp)
- [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp)
- [../cpp/tests/test_ticklab.cpp](../cpp/tests/test_ticklab.cpp)
