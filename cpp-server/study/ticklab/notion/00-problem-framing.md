# ticklab — 게임 서버를 만들기 전에, 게임 엔진을 먼저 분리한다

작성일: 2026-03-09

## 왜 이 lab이 필요한가

`roomlab`까지 오면 "소켓을 읽고, 파싱하고, 서버 상태를 바꾸는" 흐름이 완성된다. 그런데 이 저장소의 마지막 과제인 `arenaserv`는 여기에 한 가지를 더 얹는다 — **고정 tick 기반의 authoritative simulation**이다. 플레이어의 입력을 받아, 매 tick마다 세계 상태를 전진시키고, 투사체 충돌과 승패를 서버가 판정하는 것.

만약 `roomlab` 바로 다음에 `arenaserv`로 넘어가면, 두 가지 종류의 버그가 한 번에 섞인다. 하나는 네트워크 문제(소켓 lifecycle, reconnect, send buffer flush)이고, 다른 하나는 시뮬레이션 문제(tick 순서, 입력 검증, 승패 판정 타이밍)다. 이 두 가지가 동시에 터지면 원인을 분리하기가 매우 어렵다.

그래서 `ticklab`이 존재한다. **소켓 없이, tick과 판정만 고립시켜 보는 bridge lab**이다.

## 이 lab이 만드는 것

headless C++17 simulation engine이다. "headless"라 함은, TCP 서버가 아니라는 뜻이다. 소켓도 없고, event loop도 없다. `MatchEngine` 클래스 하나가 있고, 테스트 코드가 직접 함수를 호출해서 시뮬레이션을 돌린다.

구체적으로 이 엔진이 지원하는 것:

1. **Room queue와 READY 기반 countdown**: 플레이어가 등록하고, 큐에 들어가고, 준비 완료를 보내면 카운트다운이 시작된다.
2. **고정 tick 입력 처리**: `INPUT <seq> <dx> <dy> <facing> <fire>` 형식의 입력을 받되, sequence number가 단조 증가하지 않으면 거절한다.
3. **Authoritative 판정**: 투사체 충돌(HIT), 제거(elimination), 라운드 종료(ROUND_END)를 서버가 결정한다.
4. **Reconnect grace**: 연결이 끊겨도 100 tick 이내에 돌아오면 세션이 유지되고, 현재 snapshot을 재전송받는다.
5. **Deterministic transcript test**: 고정된 입력 시나리오(`arena-transcript.txt`)를 재생하면 항상 같은 이벤트가 나온다.

## 포함한 것과 제외한 것

포함:
- room phase: `lobby` → `countdown` → `in_round` → `finished`
- HP 3, 단일 action `FIRE`
- 20×20 보드, 1타일 orthogonal 이동
- tick-driven snapshot (JSON 문자열)
- reconnect grace (100 ticks)
- max_round_ticks = 30 (draw timeout)

제외:
- 소켓 I/O — `arenaserv`의 영역
- multi-room sharding — 이 단계에서는 single room으로 충분
- persistence — 범위 밖
- client prediction / rollback — 서버 authoritative 모델에서는 불필요
- float physics — 정수 grid로 충분

## 성공 기준

`make clean && make && make test`가 네 가지 테스트를 통과하면 된다:

1. **transcript fixture**: `arena-transcript.txt`를 재생했을 때 COUNTDOWN, ROOM in_round, HIT, ROUND_END가 모두 발생
2. **stale sequence**: 같은 seq를 두 번 보내면 거절
3. **rejoin grace**: 50 tick 이내 재접속은 성공, grace_ticks + 1 이후는 실패
4. **draw timeout**: max_round_ticks만큼 아무도 죽지 않으면 ROUND_END draw

## 참고한 자료

| 자료 | 경로 | 왜 봤는가 | 무엇을 알게 되었는가 |
| --- | --- | --- | --- |
| Legacy GameRoom | `legacy/src/GameRoom.cpp` | room ownership 구조 확인 | room과 match state를 분리해서 보는 것이 유리하다 |
| Legacy GameLogic | `legacy/src/GameLogic.cpp` | 승패 판정 위치 확인 | authoritative 판정은 서버 쪽 단일 상태에서 해야 한다 |
| Game protocol note | `legacy/docs/game-protocol.md` | command/event 형태 참고 | 이벤트 스트림을 명령과 결과로 분리해 적는 방식이 유용하다 |
