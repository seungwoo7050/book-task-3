# ticklab 문제 프레이밍

## 왜 simulation을 먼저 떼어 보는가

게임 서버를 바로 소켓 위에 올리면 네트워크 문제와 게임 규칙 문제가 한꺼번에 보인다. `ticklab`은 그 혼선을 줄이기 위해, authoritative simulation을 headless 엔진으로 먼저 검증한다.

## 지금 풀어야 하는 질문

- fixed-step state advance는 어떤 장점을 주는가
- stale input는 어디서 걸러야 하는가
- reconnect와 snapshot은 왜 같은 문장 안에서 다뤄야 하는가

## 성공 기준

- [../cpp/tests/test_ticklab.cpp](../cpp/tests/test_ticklab.cpp)가 countdown, input sequence, hit, elimination, draw, reconnect grace를 검증한다.
- [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp)를 읽으면 phase 전이와 판정 경계가 보인다.
- 이후 `arenaserv`에서 네트워크 층이 붙어도 핵심 판정 로직을 같은 질문으로 설명할 수 있다.

## 포트폴리오 관점에서 중요하게 볼 것

- deterministic test를 어떻게 설계했는가
- reconnect를 “세션 연속성”으로 설명할 수 있는가
- authoritative 판단이 왜 서버 한 곳에 모여야 하는가
