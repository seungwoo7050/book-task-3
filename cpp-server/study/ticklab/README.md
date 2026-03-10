# ticklab

`ticklab`은 authoritative 게임 서버 쪽으로 넘어가기 전에, transport를 잠시 치워 두고 simulation 자체를 headless로 검증하는 bridge lab이다. 게임 서버 포트폴리오에서 자주 설명해야 하는 질문을 가장 작은 단위로 떼어 본다.

## 이 프로젝트가 가르치는 것

- fixed-step simulation과 countdown 기반 상태 전이
- input sequence 검증과 stale 입력 거절
- reconnect grace와 snapshot 재생성 같은 session continuity 개념

## 현재 범위

- 포함: room queue, ready countdown, tick advance, snapshot, reconnect grace, hit/elimination/draw 판정
- 제외: socket I/O, client prediction, rollback, room sharding

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [cpp/README.md](cpp/README.md)
3. [docs/README.md](docs/README.md)
4. [notion/README.md](notion/README.md)

## 포트폴리오로 확장할 때 보여 줄 것

- authoritative 판정을 transport와 분리해 먼저 검증한 이유
- deterministic test가 왜 게임 서버 설명에서 강한 증거가 되는지
- 이후 `arenaserv`에서 어떤 네트워크 책임이 추가되는지 연결해서 설명하기
