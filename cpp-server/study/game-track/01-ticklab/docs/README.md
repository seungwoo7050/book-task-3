# ticklab 개념 메모

이 디렉터리는 simulation을 왜 네트워크보다 먼저 고정했는지 설명한다. 핵심은 게임 규칙 문제와 서버 문제를 같은 실패 원인으로 보지 않게 만드는 데 있다.

## 먼저 볼 질문

- fixed-step simulation이 왜 authoritative 판단에 유리한가
- stale input rejection을 어디서 해야 하는가
- reconnect grace를 세션 연속성 문제로 보면 어떤 테스트가 필요한가

## 읽기 포인트

- [../cpp/include/inc/MatchEngine.hpp](../cpp/include/inc/MatchEngine.hpp)
- [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp)
- [../cpp/tests/test_ticklab.cpp](../cpp/tests/test_ticklab.cpp)

## 다음 단계

- 네트워크 책임이 추가된 버전은 [../../02-arenaserv/README.md](../../02-arenaserv/README.md)
