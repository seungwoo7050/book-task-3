# Tactical Arena Server

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 원본 성격 | `legacy` 직접 이관이 아닌 신규 capstone |
| 정식 검증 | `make -C study/Game-Server-Capstone/tactical-arena-server/problem test` |

## 한 줄 요약

`C++20 + Boost.Asio + SQLite + CMake/CTest` 기반으로 구현한 `2~4인 authoritative tactical arena server`다.

## 문제 요약

TCP는 로그인, 로비, 방 생성, ready, reconnect 같은 제어 흐름을 담당하고, UDP는 실시간 입력과 snapshot 전송을 담당한다. 서버는 fixed tick으로 authoritative simulation을 수행하고, 매치 결과와 누적 전적만 SQLite에 저장한다.

## 이 프로젝트를 여기 둔 이유

기존 `study/` 트랙은 프로토콜 구현과 진단 도구를 단계적으로 학습하게 하지만, 그 지식을 하나의 서버 아키텍처로 설명하는 최종 과제가 없었다. 이 프로젝트는 그 공백을 메우는 capstone이다.

## 제공 자료

- `problem/code/control-protocol.txt` - TCP/UDP wire format 요약
- `problem/data/schema.sql` - SQLite schema 참조본
- `problem/data/arena-map.txt` - 고정 arena 규칙
- `problem/script/integration_test.py` - reconnect, forfeit, UDP ordering integration harness
- `problem/script/load_smoke_test.py` - 8 bots / 2 rooms smoke harness

## 학습 포인트

- line-based TCP control protocol과 binary UDP packet을 함께 설계하는 방법
- room 단위 상태를 strand로 직렬화하는 authoritative simulation 구조
- reconnect window, forfeit, fixed tick, respawn 같은 게임 서버 상태 전이
- SQLite persistence를 deterministic test와 연결하는 방법
- bot demo와 load smoke를 포트폴리오 설명 자료로 묶는 방법

## 실행과 검증

- 서버 실행: `make -C study/Game-Server-Capstone/tactical-arena-server/problem run-server`
- bot 데모: `make -C study/Game-Server-Capstone/tactical-arena-server/problem run-bot-demo`
- load smoke: `make -C study/Game-Server-Capstone/tactical-arena-server/problem load-test`
- 정식 검증: `make -C study/Game-Server-Capstone/tactical-arena-server/problem test`
- 구현 위치: `cpp/src/`
- 테스트 위치: `cpp/tests/`

## 현재 범위와 한계

로컬 단일 프로세스 서버, local dev login, 2~4인 FFA arena 범위까지만 다룬다. production auth, TLS, anti-cheat, spectator, sharding, NAT traversal은 v1 범위 밖이다.

- 현재 한계: `UDP_BIND nonce`는 예약 필드로 전달되지만 endpoint 검증은 최소 수준이다.
- 현재 한계: snapshot은 delta compression 없이 full-state 전송이다.
- 현재 한계: GUI client 대신 `arena_bot`과 `arena_loadtest`로만 검증한다.

## Public / Private 경계

- `problem/`은 공개 사양과 canonical 검증 래퍼만 둔다.
- `cpp/`는 공개 구현, CMake 설정, CTest만 둔다.
- `docs/`는 아키텍처, 프로토콜, simulation, persistence, load report 같은 durable notes만 둔다.
- `notion/`은 문제 framing, 접근 로그, 디버깅, 회고, 지식 인덱스를 담는 Notion 업로드용 기술 노트다.

## Provenance

- 신규 capstone으로 설계했다.
- 개념 출처는 이 저장소의 `Application-Protocols-and-Sockets`, `Reliable-Transport`, `Network-Diagnostics-and-Routing` 트랙에서 축적한 소켓, 신뢰 전송, ICMP/TTL, deterministic test 패턴이다.
