# arenaserv 개념 메모

이 디렉터리는 simulation을 서버로 올릴 때 새로 생기는 책임을 정리한다. 핵심은 사용자 경험이 아니라 서버 상태 연속성 관점에서 reconnect와 snapshot을 설명하는 것이다.

## 먼저 볼 질문

- ticklab에서 검증한 규칙 중 무엇이 그대로 올라오고 무엇이 새로 생기는가
- room queue, countdown, in-round, finished를 어떻게 한 상태 머신으로 다룰 것인가
- reconnect를 끊어진 소켓 복구가 아니라 세션 연속성 문제로 보면 어떤 설계가 필요한가

## 읽기 포인트

- [../cpp/src/Server.cpp](../cpp/src/Server.cpp)
- [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp)
- [../cpp/tests/test_arenaserv.py](../cpp/tests/test_arenaserv.py)

## 다음 단계

- 같은 저장소의 다른 capstone 비교는 [../../../irc-track/02-ircserv/README.md](../../../irc-track/02-ircserv/README.md)
