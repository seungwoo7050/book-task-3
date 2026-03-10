# Tactical Arena Server

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | 이 저장소에서 누적한 네트워크 학습을 하나의 설명 가능한 서버로 묶기 위해 직접 설계한 신규 capstone 프로젝트 |
| 정식 검증 | `make -C study/Game-Server-Capstone/tactical-arena-server/problem test` |

## 한 줄 요약

`C++20 + Boost.Asio + SQLite + CMake/CTest` 기반으로 구현한 `2~4인 authoritative tactical arena server`입니다.

## 왜 이 프로젝트가 필요한가

앞선 트랙에서 배운 TCP/UDP, 신뢰 전송, 진단 도구, deterministic test 패턴을 하나의 서버 설계로 통합해 설명하는 단계가 필요했기 때문에 추가한 capstone입니다.

## 이런 학습자에게 맞습니다

- 여러 네트워크 개념이 실제 서버 설계에서 어떻게 만나는지 보고 싶은 학습자
- 학습용 레포를 설명 가능한 포트폴리오 서버 프로젝트로 확장하고 싶은 학습자

## 지금 바로 읽는 순서

1. `problem/README.md` - 서버 범위와 canonical 검증 명령을 먼저 확인합니다.
2. `cpp/README.md` - 빌드 흐름과 구현 범위를 확인합니다.
3. `docs/README.md` - 아키텍처, 프로토콜, persistence 문서를 읽습니다.
4. `docs/presentation/README.md` - 발표용 시연 흐름과 캡처 재생성 경로를 확인합니다.
5. `notion/README.md` - 더 깊은 작업 기록과 회고가 필요할 때 참고합니다.

## 제공 자료

- `problem/code/control-protocol.txt`: TCP/UDP wire format 요약
- `problem/data/schema.sql`: SQLite schema 참조본
- `problem/data/arena-map.txt`: 고정 arena 규칙 설명
- `problem/script/integration_test.py`: reconnect, forfeit, UDP ordering integration harness
- `problem/script/load_smoke_test.py`: 8 bots / 2 rooms smoke harness

## 실행과 검증

- 서버 실행: `make -C study/Game-Server-Capstone/tactical-arena-server/problem run-server`
- 봇 데모: `make -C study/Game-Server-Capstone/tactical-arena-server/problem run-bot-demo`
- 부하 스모크: `make -C study/Game-Server-Capstone/tactical-arena-server/problem load-test`
- 정식 검증: `make -C study/Game-Server-Capstone/tactical-arena-server/problem test`
- 구현 위치: `cpp/src/`
- 테스트 위치: `cpp/tests/`

## 학습 포인트

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

## 포트폴리오로 확장하기

- 시연 캡처, DB 반영, load smoke 결과를 한 페이지에 묶으면 강한 포트폴리오 증거가 됩니다.
- 기능 목록보다 아키텍처 선택 이유와 테스트 설계를 먼저 설명하세요.
- GUI client가 없어도, bot demo와 발표 자료만 정리하면 충분히 설득력 있는 공개 결과물을 만들 수 있습니다.
