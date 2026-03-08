# Tactical Arena Server 문제 사양

## 개요

이 capstone은 지금까지 학습한 TCP/UDP 소켓, 신뢰 전송, reconnect, persistence 개념을 하나의 채용용 결과물로 묶는 C++ 게임 서버 과제다.

## 목표

- TCP 제어 채널과 UDP 실시간 채널을 분리한 authoritative session server를 구현한다.
- 2~4인 FFA tactical arena match를 fixed tick으로 시뮬레이션한다.
- SQLite에 계정/전적/매치 결과를 저장한다.
- bot client와 load smoke까지 포함해 저장소 단독 검증이 가능해야 한다.

## match 시작 규칙

- room 인원은 `2~4`
- room 생성 시 `max=<2|3|4>`로 목표 인원을 고정한다.
- 실제 매치 시작은 `players.size() == max_players`이고, 전원이 `READY=1`일 때만 허용한다.
- 이 규칙은 4인 방 smoke에서 뒤늦게 들어온 joiner가 `room_unavailable`에 걸려 대기하는 상황을 피하기 위해 canonical 동작으로 고정했다.

## canonical 명령

- 검증: `make test`
- 서버 실행: `make run-server`
- 봇 데모: `make run-bot-demo`
- 부하 스모크: `make load-test`

## 제공 자료

- `data/schema.sql`: SQLite schema 참조본
- `data/arena-map.txt`: 고정 arena 규칙 설명
- `code/control-protocol.txt`: TCP/UDP 프로토콜 요약
- `script/*.py`: integration/load harness

## 범위 제한

- production auth, TLS, anti-cheat, sharding, spectator mode는 제외한다.
- GUI client는 만들지 않는다.
- UDP는 unreliable 그대로 두고 custom reliable layer는 만들지 않는다.
- `arena_loadtest`는 외부 프로세스 래퍼가 아니라 in-process bot worker를 사용한다.
