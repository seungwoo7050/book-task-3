# Tactical Arena Server 문제 안내

## 이 문서의 역할

이 문서는 `Tactical Arena Server`를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 구현 세부와 공개 구현 경로는 상위 프로젝트 README가 연결하는 경로를 따라가면 됩니다.

## 문제 목표

지금까지 학습한 TCP/UDP 소켓, 상태 관리, persistence 개념을 하나의 authoritative game server로 묶어, 단독 저장소만으로 빌드·테스트·시연이 가능한 capstone을 만듭니다.

## 구현해야 할 동작

### 제어 채널과 실시간 채널 분리

- TCP는 로그인, 로비, 방 생성, ready, reconnect 같은 제어 흐름을 담당합니다.
- UDP는 입력과 snapshot 전송 같은 실시간 트래픽을 담당합니다.

### Authoritative simulation

- 서버가 fixed tick으로 매치를 authoritative하게 시뮬레이션합니다.
- room 단위 상태는 직렬화된 실행 맥락에서만 수정합니다.

### 매치 시작 규칙

- 방 인원은 `2~4`명입니다.
- `players.size() == max_players`이고 모든 플레이어가 `READY=1`일 때만 매치를 시작합니다.

### Persistence

- 계정/전적/매치 결과를 SQLite에 저장합니다.
- 저장 결과는 테스트와 발표 자료에서 다시 확인 가능해야 합니다.

### 검증 가능성

- bot client와 load smoke를 포함해 저장소 단독 검증이 가능해야 합니다.
- 정식 검증은 unit + integration + load smoke를 한 번에 실행합니다.

## 제공 자료와 실행 환경

- 프로토콜 요약: `code/control-protocol.txt`
- DB schema: `data/schema.sql`
- arena 규칙: `data/arena-map.txt`
- integration/load harness: `script/*.py`

## 제약과 해석 기준

- production auth, TLS, anti-cheat, sharding, spectator mode는 이번 범위에서 제외합니다.
- GUI client는 만들지 않습니다.
- UDP 위에 별도의 custom reliable layer는 만들지 않습니다.
- `arena_loadtest`는 외부 프로세스 래퍼 대신 in-process bot worker를 사용합니다.

## 성공 기준

| 항목 | 내용 |
| :--- | :--- |
| 기능 통합 | TCP/UDP 분리, authoritative simulation, reconnect, persistence가 하나의 서버로 통합됩니다. |
| 재현성 | `make test` 한 번으로 unit + integration + load smoke를 재현합니다. |
| 설명 가능성 | 문제 정의, 설계, 검증, 한계를 문서로 설명할 수 있습니다. |
| 발표 가능성 | bot demo와 캡처 자료를 바로 재생성할 수 있습니다. |
| 코드 품질 | CMake/CTest 기반의 읽기 쉬운 C++ 구조를 유지합니다. |
