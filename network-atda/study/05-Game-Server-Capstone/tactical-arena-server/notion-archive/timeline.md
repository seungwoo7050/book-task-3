# Tactical Arena Server — 개발 타임라인

## Phase 0: 환경 구축

```bash
# C++20 컴파일러 확인
clang++ --version   # macOS
g++ --version       # Linux

# 의존성 설치 (macOS)
brew install cmake boost sqlite3

# 의존성 설치 (Ubuntu)
sudo apt install cmake libboost-dev libsqlite3-dev

# 확인
cmake --version
python3 --version   # integration/load test용
```

## Phase 1: 프로젝트 구조 생성

```bash
mkdir -p cpp/{src,include/arena,tests}
mkdir -p problem/{code,data,script}
```

**CMakeLists.txt 작성**:
- `cmake_minimum_required(VERSION 3.20)`
- `project(tactical_arena_server LANGUAGES CXX)`
- C++20 표준
- `find_package`: Threads, SQLite3
- `find_path`: Boost.Asio 헤더 (macOS: `/opt/homebrew/include`)
- `arena_core` 정적 라이브러리 → 3개 실행 파일 링크
- CTest 활성화 → 3개 테스트 바이너리

```bash
cmake -S cpp -B cpp/build
cmake --build cpp/build
```

## Phase 2: 프로토콜 레이어 (`protocol.hpp/cpp`)

### TCP 텍스트 프로토콜
- `ControlMessage{verb, fields}` 구조체
- `parse_control_line()`: `"VERB key=val key=val\n"` → 구조체
- `format_control_line()`: 구조체 → 라인 문자열
- `slugify()`: 방 이름 정규화
- `make_resume_token()`: player_id + nonce로 토큰 생성

### UDP 바이너리 프로토콜
- `PacketKind` enum: input(1), snapshot(2), heartbeat(3)
- `InputPacket`: 20바이트 고정 — version, kind, match_id, player_id, sequence, move_x/y, aim_x/y, fire, dash
- `SnapshotPacket`: 가변 — 헤더 + EntitySnapshot 배열
- `HeartbeatPacket`: 헤더만
- `encode_*/decode_*` 함수 쌍

### 단위 테스트
```bash
cmake --build cpp/build --target test_protocol
./cpp/build/test_protocol
# → 패킷 직렬화/역직렬화 왕복 검증
```

## Phase 3: 시뮬레이션 레이어 (`state.hpp/cpp`)

### ArenaConfig
- tick_hz=20, snapshot_hz=10
- match_duration_ms=90000
- 아레나 크기 1000×1000
- 플레이어 속도, 대시 배수, 쿨다운, 투사체 설정

### PlayerRuntime 내부 상태
```
position (x, y), HP(100), alive, forfeited, connected
cooldown: dash_ready_at_ms, fire_ready_at_ms
stats: kills, deaths
respawn: respawn_at_ms
```

### MatchState::step(now_ms)
1. `apply_inputs()` — 이동, 대시(쿨다운 확인), 발사(투사체 생성)
2. `update_projectiles()` — 이동, 충돌 판정, 만료 제거
3. `respawn_players()` — 사망 후 3초 경과 시 리스폰
4. `apply_forfeit_timeouts()` — disconnect + resume_window 초과 시 forfeit
5. `should_finish()` — 시간 초과 또는 생존자 1명

### 단위 테스트
```bash
cmake --build cpp/build --target test_state
./cpp/build/test_state
# → 시뮬레이션 로직 (충돌, 리스폰, 포기, 종료) 테스트
```

## Phase 4: Persistence 레이어 (`repository.hpp/cpp`)

### SQLite 스키마
```sql
CREATE TABLE players (id, name UNIQUE, created_at, last_login_at);
CREATE TABLE player_stats (player_id PK, games_played, wins, losses, kills, deaths);
CREATE TABLE match_history (id, started_at, ended_at, winner_player_id, result_blob);
```

### SqliteRepository
- `initialize()`: 테이블 생성 (IF NOT EXISTS)
- `login_or_create(name)`: SELECT → INSERT if missing → UPDATE last_login_at
- `record_match()`: match_history INSERT + player_stats UPDATE (트랜잭션)
- `load_profile()`: 전적 조회
- mutex로 스레드 안전성 확보

### 단위 테스트
```bash
cmake --build cpp/build --target test_repository
./cpp/build/test_repository
# → CRUD 검증 (in-memory 또는 임시 파일 DB)
```

## Phase 5: 서버 본체 (`arena_server.cpp`)

### Boost.Asio 아키텍처
- `io_context` + N 스레드 (기본 4)
- `tcp::acceptor` — async_accept → TcpSession 생성
- `udp::socket` — async_receive_from → 패킷 라우팅
- `signal_set(SIGINT, SIGTERM)` — 정상 종료

### TcpSession
- `enable_shared_from_this`로 수명 관리
- `boost::asio::streambuf` + `async_read_until('\n')` → 라인 단위 읽기
- `strand`로 세션별 직렬화
- write_queue + `async_write` 체인

### 상태 관리
```
state_mutex_ 보호:
  players_: unordered_map<player_id, PlayerSessionState>
  rooms_:   unordered_map<room_id, shared_ptr<RoomContext>>
  matches_: unordered_map<match_id, shared_ptr<RoomContext>>
  tokens_:  unordered_map<token, player_id>
```

### 명령 핸들러 구현 순서
1. PING/PONG
2. LOGIN → login_or_create() → LOGIN_OK
3. LIST_ROOMS, CREATE_ROOM, JOIN_ROOM, LEAVE_ROOM
4. READY → try_start_match()
5. UDP_BIND → arm nonce
6. RESUME → reconnect flow

### 매치 시작 → 틱 루프
```
try_start_match():
  조건: players.size() == max_players && 전원 READY
  → MatchState 생성 (스폰 좌표 할당)
  → MATCH_START 브로드캐스트
  → schedule_tick()

schedule_tick():
  steady_timer.expires_after(50ms)
  → match_state.step(now_ms)
  → 스냅샷 주기마다 UDP 브로드캐스트
  → 재귀 스케줄링 또는 finish_match()
```

### 초기 테스트
```bash
# 서버 실행
cd problem
make run-server
# → 127.0.0.1:39001 (TCP), :39002 (UDP)

# 별도 터미널에서 telnet 테스트
telnet 127.0.0.1 39001
> LOGIN name=test
< LOGIN_OK player=1 token=... wins=0 losses=0 kills=0 deaths=0
> LIST_ROOMS
< ROOM_LIST rooms=
```

## Phase 6: Bot 클라이언트 (`arena_bot.cpp`)

- TCP 소켓으로 LOGIN → CREATE_ROOM or JOIN_ROOM → READY
- MATCH_START 수신 → UDP_BIND → UDP InputPacket 전송 루프
- MATCH_RESULT 수신 → 종료

```bash
make -C problem run-bot-demo
# → run_bot_demo.sh: 서버 시작 → 2 bots → 매치 진행 → 결과 출력
```

## Phase 7: Load Test (`arena_loadtest.cpp`)

- in-process 다중 봇 워커
- 8 bots / 2 rooms 동시 실행

```bash
make -C problem load-test
# → load_smoke_test.py: 서버 시작 → loadtest 실행 → 결과 파싱
```

## Phase 8: Integration Test (`integration_test.py`)

```bash
python3 problem/script/integration_test.py cpp/build
# → reconnect 시나리오
# → forfeit 시나리오
# → UDP ordering 검증
```

## Phase 9: 전체 검증

```bash
make -C problem test
# 1. CTest (test_protocol, test_state, test_repository)
# 2. integration_test.py
# 3. load_smoke_test.py
```

## 최종 파일 구조

```
tactical-arena-server/
├── cpp/
│   ├── CMakeLists.txt                    ← 빌드 설정
│   ├── include/arena/
│   │   ├── protocol.hpp                  ← 프로토콜 헤더
│   │   ├── state.hpp                     ← 시뮬레이션 헤더
│   │   └── repository.hpp                ← DB 헤더
│   ├── src/
│   │   ├── arena_server.cpp              ← 서버 본체 (~1000줄)
│   │   ├── protocol.cpp                  ← 직렬화/파싱
│   │   ├── state.cpp                     ← 시뮬레이션 로직
│   │   ├── repository.cpp                ← SQLite 연산
│   │   ├── arena_bot.cpp                 ← 봇 클라이언트
│   │   └── arena_loadtest.cpp            ← 부하 테스트
│   └── tests/
│       ├── test_protocol.cpp             ← 프로토콜 단위 테스트
│       ├── test_state.cpp                ← 시뮬레이션 단위 테스트
│       └── test_repository.cpp           ← DB 단위 테스트
├── problem/
│   ├── Makefile                          ← run-server / test / load-test
│   ├── code/control-protocol.txt         ← 프로토콜 사양
│   ├── data/
│   │   ├── schema.sql                    ← SQLite 스키마
│   │   └── arena-map.txt                 ← 아레나 규칙
│   └── script/
│       ├── integration_test.py           ← 통합 테스트
│       ├── load_smoke_test.py            ← 부하 스모크
│       ├── run_bot_demo.sh               ← 봇 데모
│       ├── presentation_capture.py       ← 프레젠테이션용
│       └── presentation_load_capture.py  ← 프레젠테이션용
├── docs/
└── notion/                               ← 이 문서
```
