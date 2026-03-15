# Tactical Arena Server Blog

이 문서 묶음은 `tactical-arena-server`를 "게임 서버 capstone"이라는 큰 말보다 "TCP control, UDP realtime, room-strand simulation, SQLite persistence, 검증 harness를 하나의 설명 가능한 시스템으로 어떻게 묶었는가"라는 질문으로 다시 읽는다. 현재 구현은 control protocol parser, binary UDP packet codec, room-local `MatchState`, SQLite repository, scripted bot demo, load smoke를 모두 한 저장소 안에 둔다. 따라서 이 capstone의 핵심은 기능 개수보다, 서로 다른 네트워크 학습 축을 통합해도 여전히 deterministic하게 검증되는 구조를 만드는 데 있다.

이번 재작성은 기존 blog 본문이 아니라 다음 근거만 사용했다.

- 문제 정의: `study/05-Game-Server-Capstone/tactical-arena-server/problem/README.md`
- 구현 경계: `README.md`, `cpp/README.md`, `cpp/src/*.cpp`
- 테스트 근거: `cpp/tests/*.cpp`, `problem/script/integration_test.py`, `load_smoke_test.py`, `run_bot_demo.sh`
- 실제 검증: 2026-03-14 재실행한 `make -C network-atda/study/05-Game-Server-Capstone/tactical-arena-server/problem test`
- 보조 실행: `make -C .../tactical-arena-server/problem run-bot-demo`

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-development-timeline.md`](./10-development-timeline.md)
3. [`01-evidence-ledger.md`](./01-evidence-ledger.md)
4. [`02-structure.md`](./02-structure.md)

## 이번에 다시 확인한 검증 상태

- 정식 검증 명령: `make -C network-atda/study/05-Game-Server-Capstone/tactical-arena-server/problem test`
- 결과:
  - `CTest 3/3 passed`
  - `integration_test ok`
  - `load_smoke_test ok`
- integration surface:
  - full match completion
  - resume same player
  - disconnect forfeit
  - out-of-order UDP input handling
- load surface:
  - `2 rooms x 4 bots`
- 보조 실행:
  - `run-bot-demo`에서 `demo-alpha`, `demo-beta` 둘 다 `MATCH_RESULT winner=1 scoreboard=1:0:0,2:0:0` 출력

## 지금 남기는 한계

- production auth, TLS, anti-cheat, sharding, spectator, NAT traversal은 범위 밖이다.
- `UDP_BIND` nonce 검증은 최소 수준이고, snapshot은 delta compression 없이 full-state 전송이다.
- GUI client가 아니라 scripted bot과 load harness를 통해서만 검증한다.
