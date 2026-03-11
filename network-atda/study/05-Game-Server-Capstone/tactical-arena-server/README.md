# Tactical Arena Server

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | 이 저장소에서 누적한 네트워크 학습을 하나의 설명 가능한 서버로 묶기 위해 직접 설계한 신규 capstone 프로젝트 |
| 정식 검증 | `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test` |

## 문제가 뭐였나
- 문제 배경: 이 저장소에서 누적한 네트워크 학습을 하나의 설명 가능한 서버로 묶기 위해 직접 설계한 신규 capstone 프로젝트
- 이 단계에서의 역할: 앞선 트랙에서 배운 TCP/UDP, 신뢰 전송, 진단 도구, deterministic test 패턴을 하나의 서버 설계로 통합해 설명하는 단계가 필요했기 때문에 추가한 capstone입니다.

## 제공된 자료
- `problem/code/control-protocol.txt`: TCP/UDP wire format 요약
- `problem/data/schema.sql`: SQLite schema 참조본
- `problem/data/arena-map.txt`: 고정 arena 규칙 설명
- `problem/script/integration_test.py`: reconnect, forfeit, UDP ordering integration harness
- `problem/script/load_smoke_test.py`: 8 bots / 2 rooms smoke harness

## 이 레포의 답
- 한 줄 답: `C++20 + Boost.Asio + SQLite + CMake/CTest` 기반으로 구현한 `2~4인 authoritative tactical arena server`입니다.
- 공개 답안 위치: `cpp/src/`
- 보조 공개 표면: `cpp/tests/`
- 보조 공개 표면: `docs/`
- 읽는 순서:
  1. `problem/README.md` - 문제 조건, 제공 자료, 성공 기준을 먼저 확인합니다.
  2. `cpp/README.md` - 현재 공개 답안 범위와 기준 명령을 확인합니다.
  3. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
  4. `notion/README.md` - 공개 학습 노트이지만 엔트리포인트는 아닙니다.

## 어떻게 검증하나
- 서버 실행: `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem run-server`
- 봇 데모: `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem run-bot-demo`
- 부하 스모크: `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem load-test`
- 정식 검증: `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test`
- 구현 위치: `cpp/src/`
- 테스트 위치: `cpp/tests/`

## 무엇을 배웠나
- line-based TCP control protocol과 binary UDP packet을 함께 설계하는 방법
- room 단위 상태를 strand로 직렬화하는 authoritative simulation 구조
- reconnect window, forfeit, fixed tick, respawn 같은 게임 서버 상태 전이
- SQLite persistence를 deterministic test와 연결하는 방법
- bot demo와 load smoke를 발표 자료로 묶는 방법

## 현재 한계
- production auth, TLS, anti-cheat, spectator, sharding, NAT traversal은 범위 밖입니다.
- `UDP_BIND nonce` 검증은 최소 수준입니다.
- snapshot은 delta compression 없이 full-state 전송입니다.
- GUI client 대신 `arena_bot`, `arena_loadtest`로 검증합니다.
