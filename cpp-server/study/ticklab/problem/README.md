# ticklab 문제 재구성

이 문서는 현재 저장소의 구현, 테스트, 보존된 기록을 바탕으로 다시 정리한 학습용 문제 설명이다. 핵심은 “게임 서버의 중요한 판단을 네트워크 없이 먼저 검증한다”는 데 있다.

## 학습 목표

- authoritative simulation을 fixed-step으로 설계한다.
- 입력 시퀀스를 검증해 stale command를 걸러낸다.
- reconnect grace와 snapshot regeneration을 세션 연속성 문제로 다룬다.

## 구현해야 할 것

- room queue와 ready 기반 countdown
- monotonic input sequence 검증
- fixed tick마다 state advance와 snapshot 생성
- hit, elimination, round timeout draw 판정
- reconnect grace window와 snapshot 재전송

## 산출물

- headless C++17 match engine
- deterministic transcript fixture 기반 unit test

## 범위에서 제외하는 것

- socket I/O
- client prediction과 rollback
- 여러 room shard와 persistence

## 현재 저장소에서 확인할 수 있는 근거

- [../cpp/include/inc/MatchEngine.hpp](../cpp/include/inc/MatchEngine.hpp): 엔진의 공개 표면
- [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp): 상태 전이와 판정 로직
- [../cpp/tests/test_ticklab.cpp](../cpp/tests/test_ticklab.cpp): deterministic test
- [../notion-archive/00-problem-framing.md](../notion-archive/00-problem-framing.md): 이전 문제 정의 메모 백업
