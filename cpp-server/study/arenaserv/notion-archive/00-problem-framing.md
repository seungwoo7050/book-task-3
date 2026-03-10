# arenaserv — 검증된 시뮬레이션 엔진 위에 TCP 서버를 얹다

작성일: 2026-03-09

## 이 capstone의 위치

이 저장소의 6개 프로젝트를 순서대로 보면:

1. `eventlab` — event loop를 고립시켜 본다
2. `msglab` — IRC line parser를 고립시켜 본다
3. `roomlab` — registration + room lifecycle state machine을 본다
4. `ticklab` — authoritative tick simulation을 네트워크 없이 검증한다
5. `ircserv` — 1+2+3을 합쳐 pure IRC 서버를 만든다
6. **`arenaserv`** — 1+4를 합쳐 authoritative game server를 만든다

`ircserv`가 "프로토콜과 상태 머신의 완성"을 보여주는 capstone이라면, `arenaserv`는 **"실시간 시뮬레이션과 네트워크의 통합"**을 보여주는 capstone이다. room queue, countdown, fixed-tick 시뮬레이션, 투사체 충돌, reconnect grace — 이 모든 것이 하나의 TCP 서버 안에서 돌아간다.

## 이 서버가 하는 일

```sh
./arenaserv <port>
```

클라이언트는 다음 명령을 보낼 수 있다:
- **HELLO \<nick\>** — 닉네임으로 등록, session token 발급
- **QUEUE** — room 대기열에 진입
- **READY** — 준비 완료 (2명 이상 준비 시 countdown 시작)
- **INPUT \<seq\> \<dx\> \<dy\> \<facing\> \<fire\>** — 매 tick에 적용될 입력
- **REJOIN \<token\>** — 끊어진 세션에 재접속
- **LEAVE** — 완전 퇴장
- **PING \<payload\>** — 연결 확인 (no-op)

서버가 보내는 이벤트:
- **WELCOME \<token\>** — 등록/재접속 확인
- **ROOM \<id\> \<phase\>** — room 상태 변경
- **COUNTDOWN \<n\>** — 카운트다운 단계
- **SNAPSHOT \<tick\> \<json\>** — 매 tick 세계 상태
- **HIT \<target\>** — 투사체 적중
- **ELIM \<target\>** — 제거
- **ROUND_END \<winner|draw\>** — 라운드 종료
- **ERROR \<code\> \<message\>** — 규칙 위반

## 포함한 것과 제외한 것

포함:
- pure TCP, single-process non-blocking event loop
- 2~4인 room-based match
- fixed tick (100ms interval) authoritative simulation
- 20×20 grid, HP 3, FIRE action
- reconnect grace (10초 = 100 tick × 100ms)
- session token 기반 세션 관리

제외:
- UDP — pure TCP만 사용
- rollback / client prediction — 서버 authoritative 모델
- persistence / metrics — 범위 밖
- frontend / web transport — 범위 밖
- multi-room sharding — single room으로 충분

## 성공 기준

네 가지 smoke test 시나리오가 모두 통과해야 한다:

1. **Duel + Rejoin**: 2인 duel에서 HIT → ELIM → ROUND_END 경로 확인 + duplicate nick 거절 + within-grace rejoin 성공 + expired rejoin 실패 + invalid input 거절 + stale sequence 거절
2. **3인 lobby**: 3인 queue → ready → countdown → snapshot 시작
3. **4인 lobby + overflow**: 4인 queue → 5번째 client가 `room_full` 에러 수신
4. **Draw timeout**: 아무도 행동하지 않으면 max_round_ticks 후 `ROUND_END draw`

## 참고한 자료

| 자료 | 경로 | 왜 봤는가 | 무엇을 알게 되었는가 |
| --- | --- | --- | --- |
| Legacy EventManager | `legacy/src/EventManager.cpp` | TCP event loop 기반 확인 | single-process non-blocking loop를 재사용할 수 있다 |
| Ticklab MatchEngine | `study/ticklab/cpp/src/MatchEngine.cpp` | simulation core 재사용 | headless에서 검증한 규칙을 네트워크에 직접 얹을 수 있다 |
| Portfolio checklist | `legacy/docs/portfolio-checklist.md` | 시연 요구사항 확인 | 이벤트 증거가 있는 데모 시나리오가 필요하다 |
