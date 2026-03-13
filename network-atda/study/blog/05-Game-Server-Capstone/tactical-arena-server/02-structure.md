# Tactical Arena Server structure guide

## 이 글의 중심 질문

- 제어 채널, authoritative simulation, persistence, 검증 하네스를 한 서버 안에서 어떻게 맞물리게 했는가?
- 한 줄 답: C++20 + Boost.Asio + SQLite + CMake/CTest` 기반으로 구현한 `2~4인 authoritative tactical arena server`입니다.

## 권장 흐름

1. 서버 표면과 실행 경로를 먼저 고정하기
2. control protocol, match step, persistence를 같은 서버 흐름으로 묶기
3. 통합 검증과 남은 범위를 정리하기

## 꼭 살릴 근거

- `problem/Makefile`의 공개 target과 `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test`
- `study/05-Game-Server-Capstone/tactical-arena-server/cpp/src/state.cpp`의 `MatchState::step`
- `study/05-Game-Server-Capstone/tactical-arena-server/problem/script/integration_test.py`의 `def scenario_full_match`

## 리라이트 주의점

- `Tactical Arena Server`를 개념 강의처럼 풀지 말고, 실제 파일과 CLI 순서로 보여 준다.
- 전체 로그를 덤프하지 말고 판단을 바꾼 줄만 남긴다.
- 마지막에는 production auth, TLS, anti-cheat, spectator, sharding, NAT traversal은 범위 밖입니다. 같은 남은 경계를 사람 말로 다시 정리한다.
