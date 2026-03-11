# ticklab — 지식 인덱스: tick 기반 시뮬레이션의 세 가지 원칙

작성일: 2026-03-09

## 1. Authoritative server는 입력을 "도착 시점"이 아니라 "tick 경계"에서 소비한다

roomlab 같은 이벤트 드리븐 서버에서는 메시지가 도착하면 즉시 처리한다. `JOIN #lab`을 받으면 바로 채널에 가입시킨다. 하지만 tick 기반 서버에서는 다르다.

plyer의 입력(`INPUT <seq> <dx> <dy> <facing> <fire>`)이 도착하면, 서버는 이것을 `pending_input`에 저장만 한다. 실제로 적용되는 것은 다음 `advance_one_tick()` 호출 시다. 이렇게 하면 같은 tick 안에서 모든 플레이어의 입력이 동시에 적용되므로, 입력 도착 순서에 따른 불공정이 사라진다.

코드에서: `submit_input()`은 `participant.pending_input`에 저장만 하고, `advance_one_tick()` → `process_inputs()`에서 실제로 좌표를 갱신한다.

이 개념은 `arenaserv`에서도 동일하다. 차이점은 `arenaserv`에서는 tick이 100ms timer event에 의해 트리거된다는 것뿐이다.

## 2. Reconnect는 transport continuity가 아니라 session continuity 문제다

소켓이 끊기면 TCP 연결은 사라진다. 하지만 게임 세션은 살아 있을 수 있다. `ticklab`에서의 reconnect는 이 구분을 명확히 한다:

- `disconnect_player()`: `connected = false`, `disconnect_tick = global_tick_`으로 표시만 한다. participant 데이터는 삭제하지 않는다.
- `advance_one_tick()` → `expire_disconnected_players()`: 매 tick마다 disconnected 플레이어를 확인하고, `global_tick_ - disconnect_tick > grace_ticks`이면 세션을 만료시킨다.
- `rejoin_player()`: grace 안에 호출되면 `connected = true`로 복구하고 현재 상태(WELCOME, ROOM, SNAPSHOT)를 재전송한다.

핵심은 "소켓이 끊겼다 ≠ 세션이 끝났다"라는 것이다. grace window가 이 두 개념 사이의 시간을 만들어준다.

## 3. Snapshot은 디버깅 출력이 아니라 state recovery 계약이다

매 tick 생성되는 snapshot JSON은 두 가지 용도가 있다:

1. **정상 플레이**: 클라이언트에게 현재 세계 상태(각 플레이어의 위치, HP, alive 여부, 투사체 위치)를 알려준다.
2. **재접속 복구**: `rejoin_player()`가 현재 snapshot을 재전송함으로써, 재접속한 클라이언트가 즉시 게임 상태를 복원한다.

이것이 "계약"인 이유: snapshot에 포함되는 필드가 변경되면, 클라이언트 측의 파싱 로직도 함께 바꿔야 한다. ticklab에서 schema를 고정해두면, `arenaserv`에서 같은 schema를 copy할 때 호환성이 보장된다.

## 참고 자료

| 자료 | 경로 | 왜 봤는가 | 무엇을 알게 되었는가 |
| --- | --- | --- | --- |
| Transcript fixture | `study/ticklab/problem/data/arena-transcript.txt` | deterministic 시나리오 고정 | countdown, hit, round end가 한 파일로 재현 가능하다 |
| Test source | `study/ticklab/cpp/tests/test_ticklab.cpp` | 검증 범위 확인 | stale sequence, rejoin, draw timeout이 핵심 검증 포인트 |
| MatchEngine impl | `study/ticklab/cpp/src/MatchEngine.cpp` | phase/state/event 흐름 확인 | lobby → countdown → in_round → finished 경로가 명확해야 하고, `maybe_finish_round()`의 호출 위치가 중요하다 |
