# ticklab 접근 기록

## 처음 고정한 질문

`ticklab`에서 가장 먼저 정해야 했던 것은 "바로 서버를 만들 것인가, 아니면 simulation만 먼저 검증할 것인가"였다. 이 질문에 답하지 못하면 `ticklab`과 `arenaserv`의 경계가 사라진다.

## 실제로 비교한 선택지

### 선택지 A. 처음부터 네트워크 서버로 만든다

겉으로 보기에는 자연스럽다. 최종 목표가 TCP 기반 game server이기 때문이다. 하지만 이 선택은 너무 많은 실패 원인을 한곳에 몰아넣는다.

- 소켓 lifecycle
- reconnect 타이밍
- send buffer flush
- tick advance와 판정 로직

이 모든 것이 동시에 있으면 테스트가 깨졌을 때 어디부터 봐야 할지 흐려진다.

### 선택지 B. headless simulation engine을 먼저 만든다

이 방법을 택했다. 핵심은 [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp)의 public API를 [../cpp/tests/test_ticklab.cpp](../cpp/tests/test_ticklab.cpp)에서 직접 호출해, 네트워크 변수를 제거한 상태로 시뮬레이션만 검증하는 것이다.

이 선택으로 얻은 장점은 분명했다.

- authoritative 판정 로직을 고립시켜 읽을 수 있다.
- reconnect grace와 snapshot regeneration을 네트워크 부가 기능이 아니라 엔진 책임으로 설명할 수 있다.
- 이후 `arenaserv`에서 네트워크를 붙여도 "무엇이 새로 추가됐는가"를 분리해 볼 수 있다.

## 구체적으로 고정한 설계

- single room으로 범위를 제한한다.
- countdown과 grace window는 wall-clock이 아니라 tick 수로 표현한다.
- snapshot은 문자열 기반 상태 복구 계약으로 본다.
- 입력 검증은 seq 단조 증가와 최소 movement rule에 집중한다.

이 선택들은 모두 "authoritative 구조를 먼저 보여 준다"는 목표를 강화한다.

## 일부러 하지 않은 선택

- socket I/O를 같이 넣지 않았다.
- projectile physics를 복잡하게 키우지 않았다.
- rollback과 prediction을 도입하지 않았다.

이 주제들은 모두 중요하지만, 지금 질문은 실시간 네트워크 기술이 아니라 authoritative simulation의 경계다.

## 학생이 가져가면 좋은 기준

- 최종 제품과 같은 모양이 아니어도, 더 좋은 학습 단위를 먼저 만들 수 있다.
- deterministic test가 가능해지는 구조는 그 자체로 큰 설계 이점이다.
- reconnect를 "세션 복구"로 먼저 설명하면 나중에 네트워크 설계도 훨씬 선명해진다.

## 읽기 추천 경로

1. [../cpp/include/inc/MatchEngine.hpp](../cpp/include/inc/MatchEngine.hpp)
2. [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp)
3. [../cpp/tests/test_ticklab.cpp](../cpp/tests/test_ticklab.cpp)
