# ticklab — 개발 타임라인: headless engine을 만들어 시뮬레이션만 먼저 고정한다

작성일: 2026-03-09

이 문서는 ticklab의 전체 개발 과정을 시간순으로 복원한다. 소스코드에서는 드러나지 않는 의사결정, 파일 생성 순서, 테스트 설계 과정을 기록한다.

---

## Phase 0: 환경과 도구

ticklab은 네트워크를 사용하지 않으므로, 이전 lab들보다 도구가 적다.

```
c++ --version        # Apple clang, C++17
make --version       # GNU Make
```

| 도구 | 용도 | 비고 |
| --- | --- | --- |
| Apple Clang (c++) | C++17 컴파일 | `-Wall -Wextra -Werror -std=c++17 -MMD -MP` (pthread 불필요) |
| GNU Make | 빌드 시스템 | `make clean && make && make test` |

nc나 Python은 사용하지 않는다. 테스트가 C++ 직접 호출이기 때문이다.

---

## Phase 1: legacy 분석과 설계 결정

### Legacy에서 가져온 것

legacy에는 `GameRoom.cpp`와 `GameLogic.cpp`가 있었다. 이것들을 직접 가져오지는 않았다. 대신 **아이디어만 참고하고 새로 작성했다**.

이유: legacy의 게임 로직은 WebSocket, Store, Metrics 등과 얽혀 있어서 분리하기가 어려웠다. 그리고 ticklab의 목표가 "headless engine"이므로, 네트워크 의존성이 전혀 없는 클래스를 처음부터 설계하는 편이 나았다.

### 핵심 상수 결정

```cpp
const int MatchEngine::board_width = 20;
const int MatchEngine::board_height = 20;
const int MatchEngine::max_players = 4;
const int MatchEngine::min_players = 2;
const int MatchEngine::max_hp = 3;
const int MatchEngine::countdown_steps = 3;
const int MatchEngine::grace_ticks = 100;
const int MatchEngine::max_round_ticks = 30;
```

이 상수들은 코드를 작성하기 전에 먼저 결정했다. 특히 `grace_ticks = 100`과 `max_round_ticks = 30`은 테스트에서 직접 사용되므로, 테스트 시나리오와 함께 설계해야 했다.

---

## Phase 2: MatchEngine.hpp 설계

파일 구조를 보면 ticklab은 소스 파일이 하나뿐이다:

```
study/ticklab/cpp/
├── Makefile
├── include/inc/
│   └── MatchEngine.hpp
├── src/
│   └── MatchEngine.cpp
└── tests/
    └── test_ticklab.cpp
```

MatchEngine 클래스의 public API를 먼저 설계했다:

- `register_player(nick, &token, &error)` — 플레이어 등록, token 발급
- `queue_player(token, &error)` — room 큐에 진입
- `ready_player(token, &error)` — 준비 완료
- `submit_input(token, input, &error)` — 입력 제출
- `advance_one_tick()` — tick 전진
- `disconnect_player(token)` — 연결 끊김 표시
- `rejoin_player(token, &error)` — 재접속
- `drain_events()` — 이벤트 수확
- `leave_player(token, &error)` — 완전 퇴장

모든 상태 변경 함수에 `Error` out 파라미터를 두어, 실패 시 에러 코드로 원인을 구분할 수 있게 했다.

---

## Phase 3: 내부 타입 설계

MatchEngine 안에 네 개의 내부 타입을 두었다:

1. **Error** — `code`와 `message` 문자열 쌍. `empty()`로 에러 유무 판별
2. **Input** — `seq`, `dx`, `dy`, `facing`, `fire`. 클라이언트 입력의 구조화된 표현
3. **Participant** — 플레이어 상태 전체: token, nick, connected, in_room, ready, alive, hp, x, y, facing, last_seq, pending_input, disconnect_tick
4. **Projectile** — 투사체: owner_token, x, y, vx, vy

그리고 Room phase를 enum으로:
```cpp
enum class Phase { Lobby, Countdown, InRound, Finished };
```

---

## Phase 4: transcript fixture 작성

코드 구현과 동시에, 테스트용 시나리오 파일을 작성했다:

```
# arena-transcript.txt
HELLO alpha
HELLO bravo
QUEUE alpha
QUEUE bravo
READY alpha
READY bravo
TICK
TICK
TICK
INPUT alpha 1 0 0 E 1
TICK
TICK
INPUT alpha 2 0 0 E 1
TICK
TICK
INPUT alpha 3 0 0 E 1
TICK
TICK
```

이 파일은 두 플레이어가 등록 → 큐 → 준비 → 카운트다운(3 tick) → alpha가 3번 FIRE하여 bravo를 제거하는 시나리오다. alpha의 투사체가 동쪽으로 발사되어 bravo에게 3번 적중하면(HP 3 → 0), `ROUND_END alpha`가 나와야 한다.

---

## Phase 5: MatchEngine.cpp 구현

구현 순서:

1. **register_player / queue_player / ready_player** — lobby phase, token 발급, 큐 진입, countdown 시작 조건
2. **start_countdown / start_round** — countdown_remaining 감소, InRound 전환
3. **submit_input** — stale sequence guard (`seq <= last_seq`), orthogonal movement 검증, pending_input 저장
4. **advance_one_tick** — global_tick 증가, expire_disconnected, countdown 처리, round tick: process_inputs → move_projectiles → emit snapshot → maybe_finish_round
5. **process_inputs** — pending_input 적용: 좌표 이동, FIRE 시 projectile 생성
6. **move_projectiles** — 투사체 이동, 보드 밖 제거, hit 판정 (HP 감소, HIT 이벤트)
7. **maybe_finish_round** — 생존자 수 또는 round_tick 체크, ROUND_END emit
8. **disconnect_player / rejoin_player** — grace window 기반 세션 관리
9. **snapshot_json** — JSON 문자열 생성 (players + projectiles 배열)

---

## Phase 6: 테스트 작성

네 개의 테스트 함수를 작성했다:

### test_transcript_fixture
- `arena-transcript.txt` 파일을 한 줄씩 읽으며 MatchEngine API 호출
- 마지막에 drain_events()로 COUNTDOWN 3, ROOM in_round, HIT, ROUND_END alpha 확인

### test_stale_sequence_and_validation
- 카운트다운 이후 seq=1 입력 → 같은 seq=1 입력 → `stale_sequence` 에러 확인
- 대각선 이동 (dx=1, dy=1) → `invalid_input` 에러 확인

### test_rejoin_grace_window
- disconnect → 50 tick → rejoin → 성공 확인
- disconnect → 101 tick (grace_ticks + 1) → rejoin → `expired_session` 에러 확인

### test_draw_timeout
- 두 플레이어 등록, 카운트다운 완료 후 아무 행동 없이 30 tick → `ROUND_END draw` 확인

---

## Phase 7: Makefile 작성

```makefile
NAME := ticklab_tests
SRCS := src/MatchEngine.cpp tests/test_ticklab.cpp
```

이전 lab들(`eventlabd`, `roomlabd`)과 달리, 바이너리 이름이 `_tests`로 끝난다. 서버가 아니라 테스트 실행 파일이기 때문이다. `make test`는 `./ticklab_tests`를 직접 실행한다.

---

## 최종 빌드와 확인

```bash
make clean && make && make test
# → ticklab tests passed.
```

소스 파일 1개, 테스트 파일 1개, fixture 파일 1개. 이 저장소에서 가장 작은 프로젝트지만, `arenaserv` 구현의 핵심 자산이 된다.
