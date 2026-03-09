# arenaserv — 개발 타임라인: ticklab engine + EventManager = game server

작성일: 2026-03-09

이 문서는 arenaserv capstone의 전체 개발 과정을 시간순으로 복원한다. 소스코드에서는 드러나지 않는 의사결정, 파일 생성 순서, 네트워크 통합 과정을 기록한다.

---

## Phase 0: 환경과 도구

```
c++ --version        # Apple clang, C++17
python3 --version    # smoke test runner
make --version       # GNU Make
```

| 도구 | 용도 | 비고 |
| --- | --- | --- |
| Apple Clang (c++) | C++17 컴파일 | `-Wall -Wextra -Werror -std=c++17 -MMD -MP -pthread` |
| GNU Make | 빌드 시스템 | `make clean && make && make test` |
| Python 3 | smoke test | 4개 시나리오, 각 시나리오가 별도 서버 인스턴스 사용 |

---

## Phase 1: 아키텍처 결정 — 두 개의 핵심 자산을 합친다

arenaserv의 핵심은 두 가지 기존 자산을 합치는 것이다:

1. **EventManager** — eventlab/roomlab/ircserv에서 검증된 cross-platform event loop
2. **MatchEngine** — ticklab에서 4개 테스트로 검증된 headless simulation engine

합치는 방식: MatchEngine을 ticklab에서 **파일 복사**로 가져오고, EventManager도 적절한 lab에서 복사한다. import(헤더 참조나 라이브러리 링크)가 아니라 copy다.

이 결정의 이유:
- 각 프로젝트가 `make clean && make && make test`로 독립 빌드/테스트 가능해야 한다
- inter-project 빌드 의존성을 만들면 학습 프로젝트로서의 독립성이 깨진다

---

## Phase 2: 파일 구조 확립

```
study/arenaserv/cpp/
├── Makefile             # NAME := arenaserv
├── include/inc/
│   ├── EventManager.hpp
│   ├── MatchEngine.hpp
│   ├── Server.hpp
│   └── utils.hpp
├── src/
│   ├── EventManager.cpp # eventlab에서 복사 (timeout parameter 추가)
│   ├── MatchEngine.cpp  # ticklab에서 복사
│   ├── Server.cpp       # 새로 작성
│   ├── main.cpp         # 새로 작성
│   └── utils.cpp        # legacy에서 복사
└── tests/
    └── test_arenaserv.py # 새로 작성
```

소스 파일 5개. ircserv(11개)나 roomlab(11개)에 비해 적다. IRC 프로토콜의 복잡한 command handler/channel model/connection state가 없기 때문이다.

---

## Phase 3: Server.cpp — 새로 작성한 접착 코드

Server.cpp는 이 capstone에서 **유일하게 새로 작성한 핵심 코드**다. IRC 서버의 Server.cpp와는 구조가 상당히 다르다:

### IRC 서버(roomlab/ircserv)의 Server.cpp
- Connection 객체를 `std::list`로 관리
- nickdb, sockdb, chandb 등 여러 인덱스
- Parser/Executor에 dispatch

### arenaserv의 Server.cpp
- Client 구조체를 `std::map<int, Client>`로 관리 (fd → Client)
- `token_to_fd` 맵으로 session token ↔ socket fd 매핑
- 한 줄 명령을 직접 파싱하여 MatchEngine API 호출
- `pump_ticks()` 로 tick scheduling

차이의 이유: arena 프로토콜이 IRC보다 훨씬 단순하다. CRLF로 구분된 명령이 `HELLO <nick>`, `QUEUE`, `READY`, `INPUT <args>`, `REJOIN <token>`, `LEAVE`, `PING <payload>` 뿐이다. 별도의 Parser/Executor 계층이 필요 없다.

---

## Phase 4: tick scheduler 구현

`pump_ticks()` 함수가 tick scheduling을 담당한다:

```cpp
void Server::pump_ticks()
{
    const std::uint64_t now = current_millis();
    while (this->last_tick_ms + tick_interval_ms <= now)
    {
        this->engine.advance_one_tick();
        this->dispatch_engine_events();
        this->last_tick_ms += tick_interval_ms;
    }
}
```

`tick_interval_ms = 100`이므로 100ms마다 한 번씩 tick이 전진한다.

`EventManager::retrieve_events()`에 timeout=50ms를 전달해서, event가 없어도 50ms마다 리턴한다. 이렇게 하면 event loop의 한 cycle이 최대 50ms이므로, tick이 최대 50ms 늦게 실행될 수 있지만 건너뛰는 일은 없다 (밀린 tick은 while loop에서 따라잡는다).

---

## Phase 5: 이벤트 dispatch 구현

`dispatch_engine_events()`가 MatchEngine의 내부 이벤트 큐를 소켓으로 전달한다:

1. `engine.drain_events()` 호출 → 이벤트 벡터 반환
2. 각 이벤트의 scope 확인:
   - `EventScope::Room` → room에 있는 모든 플레이어에게 전송
   - `EventScope::Single` → 특정 token의 플레이어에게만 전송
3. `token_to_fd` 맵으로 token → fd 변환
4. 해당 client의 send buffer에 이벤트 line을 추가하고 `sendq`에 등록

핵심 결정: state mutation 직후에도 `dispatch_engine_events()`를 호출한다 (debug log 문제 1 참고). 이렇게 하면 QUEUE 직후 `ROOM` 이벤트가 다음 tick을 기다리지 않고 즉시 전송된다.

---

## Phase 6: Reconnect 구현

reconnect 흐름:

1. 클라이언트 연결 끊김 감지 → `disconnect(fd)` 호출
2. `disconnect()`에서:
   - `engine.disconnect_player(token)` — MatchEngine에 연결 끊김 표시
   - `token_to_fd.erase(token)` — fd 매핑 제거
   - 소켓 close, clients 맵에서 제거
3. 새 클라이언트가 `REJOIN <token>` 명령 전송
4. `engine.rejoin_player(token)` 호출:
   - grace 내이면 성공, WELCOME + ROOM + SNAPSHOT 이벤트 생성
   - grace 초과면 실패, `expired_session` 에러 반환
5. 성공 시 새 fd를 `token_to_fd`에 등록

grace window: 100 tick × 100ms = 10초

---

## Phase 7: Smoke test 작성

네 개의 独立 시나리오를 작성했다. 각 시나리오가 별도 포트에서 별도 서버 인스턴스를 실행한다:

### scenario_duel_and_rejoin (port 6680)
- alpha, bravo 등록
- duplicate nick 거절 (`ERROR duplicate_nick`)
- ghost 등록 → 소켓 닫기 → within-grace rejoin 성공 → 10.5초 대기 → expired rejoin 실패
- alpha, bravo QUEUE → READY → countdown → round start
- alpha: invalid input 거절 (`dx=1, dy=1` → `ERROR invalid_input`)
- alpha: stale sequence 거절 (seq=1 두 번 → `ERROR stale_sequence`)
- alpha: 3번 FIRE → HIT × 3 → ELIM → ROUND_END alpha

### scenario_party_lobby (port 6681, 3인)
- 3명 등록 → QUEUE → READY → COUNTDOWN → SNAPSHOT

### scenario_party_lobby (port 6682, 4인 + overflow)
- 4명 등록 → QUEUE → 5번째 client가 `ERROR room_full`
- 4명 READY → COUNTDOWN → SNAPSHOT

### scenario_draw_timeout (port 6683)
- 2명 등록 → QUEUE → READY → round start
- 아무 행동 없이 max_round_ticks 대기 → ROUND_END draw

---

## Phase 8: 버그 수정

### 이벤트 flush 타이밍 (debug log 문제 1)
state mutation 직후 `dispatch_engine_events()` 호출 추가

### fd 매핑 정리 (debug log 문제 2)
`disconnect()`에서 `token_to_fd.erase(token)` 추가

### overflow 테스트 (debug log 문제 3)
4인 시나리오에 5번째 client의 `room_full` 거절 테스트 추가

---

## 최종 빌드와 확인

```bash
make clean && make && make test
# → arenaserv smoke passed.
```

바이너리: `arenaserv`, 사용법: `./arenaserv <port>`

5개의 소스 파일이 컴파일되고, Python smoke test가 4개 시나리오를 통과하면 arenaserv capstone은 완성이다. duel + rejoin 시나리오는 `time.sleep(10.5)` 때문에 실행 시간이 약 15초 정도 걸린다.
