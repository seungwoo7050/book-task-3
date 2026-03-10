# ticklab C++ 구현

상태: `verified`  
2026-03-10 기준 `make clean && make test`를 다시 확인했다.

## 이 구현이 맡는 범위

- authoritative room state machine
- fixed-step countdown과 round tick
- input validation과 stale sequence rejection
- reconnect grace와 snapshot regeneration
- deterministic transcript-driven test

## 아직 다루지 않는 것

- 네트워크 I/O
- 복잡한 projectile physics
- rollback, prediction, multi-room scaling

## 빌드와 테스트

```sh
make clean && make
make test
```

## 코드 읽기 포인트

- [include/inc/MatchEngine.hpp](include/inc/MatchEngine.hpp): 핵심 타입과 인터페이스
- [src/MatchEngine.cpp](src/MatchEngine.cpp): tick advance, hit, elimination, reconnect 처리
- [tests/test_ticklab.cpp](tests/test_ticklab.cpp): deterministic 검증 시나리오

## 포트폴리오로 옮길 때 보여 줄 증거

- sequence rejection과 reconnect grace를 재현하는 테스트 캡처
- authoritative 판정이 왜 서버 한 곳에 있어야 하는지 설명한 다이어그램
- `arenaserv`로 확장되면서 네트워크 층이 어떻게 덧붙는지 비교한 메모
