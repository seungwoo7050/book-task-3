# Tactical Arena Server — TCP와 UDP가 만나는 곳

## 캡스톤의 의미

소켓 프로그래밍부터 신뢰 전송까지 9개 프로젝트를 거치며 쌓은 지식의 종착점이다. HTTP 서버에서 배운 TCP 소켓 관리, UDP Pinger에서 배운 데이터그램 처리, ICMP에서 배운 바이너리 패킷 구조, Reliable Transport에서 배운 시퀀스 번호와 타이머 — 이 모든 것이 하나의 게임 서버 아키텍처 안에서 만난다.

## 이중 채널 설계

게임 서버의 핵심 결정은 프로토콜 선택이다. 이 서버는 TCP와 UDP를 동시에 사용한다:

- **TCP**: 로그인, 방 생성/참가, 레디, 매치 시작 통지, 결과 통보 — 반드시 전달되어야 하는 제어 메시지
- **UDP**: 플레이어 입력(이동, 조준, 발사, 대시), 서버 스냅샷 — 최신 데이터만 의미 있는 실시간 데이터

TCP와 UDP를 분리하는 이유는 교과서적이다. TCP의 head-of-line blocking은 실시간 게임에서 치명적이고, UDP의 비신뢰성은 제어 흐름에서 치명적이다. 각 프로토콜의 장점만 취하는 것이 게임 네트워킹의 정석이다.

## TCP 제어 프로토콜

텍스트 기반 라인 프로토콜을 설계했다. 형식은 `VERB key=value key=value\n`. HTTP의 단순화된 버전이라고 볼 수 있다.

클라이언트 명령:
- `LOGIN name=<name>` — 계정 생성 또는 기존 계정으로 로그인
- `LIST_ROOMS` — 현재 방 목록 조회
- `CREATE_ROOM name=<name> max=<2|3|4>` — 방 생성
- `JOIN_ROOM room=<id>` — 방 참가
- `READY value=<0|1>` — 준비 상태 토글
- `RESUME token=<token>` — 끊어진 세션 복구

서버 이벤트:
- `LOGIN_OK` — 인증 성공 및 누적 전적 반환
- `MATCH_START` — 매치 시작, UDP 포트와 스폰 좌표 전달
- `MATCH_RESULT` — 승자와 스코어보드

`parse_control_line()`은 한 줄을 파싱해서 `ControlMessage{verb, fields}` 구조체로 변환한다. 알 수 없는 verb이나 필수 필드 누락 시 `ERROR` 응답을 보낸다.

## UDP 바이너리 프로토콜

UDP 패킷은 바이트 레벨에서 설계했다. 세 종류:

1. **InputPacket** (20바이트): 이동 벡터(i8 × 2), 조준 벡터(i16 × 2), fire/dash 플래그, 시퀀스 번호
2. **SnapshotPacket** (가변): 서버 틱, 엔티티 배열(플레이어별 x/y/hp/kills/deaths/alive)
3. **HeartbeatPacket** (헤더만): UDP endpoint 등록 및 유지

`encode_*`와 `decode_*` 함수 쌍으로 직렬화/역직렬화한다. version 필드로 향후 호환성을 확보했고, `PacketKind` 열거형으로 패킷 타입을 구분한다.

## Authoritative 시뮬레이션

서버가 진실의 원천(source of truth)이다. 클라이언트는 입력만 보내고, 서버가 물리 연산을 수행한다.

`MatchState` 클래스가 전체 매치 상태를 관리한다:
- `PlayerRuntime`: 위치, HP, 생존 여부, 킬/데스, 쿨다운 타이머, 탈주 여부
- `Projectile`: 위치, 속도 벡터, 만료 시각
- `step(now_ms)`: 한 틱의 시뮬레이션 — 입력 적용 → 투사체 이동/충돌 → 리스폰 처리 → 탈주 감지 → 종료 판정

20Hz 고정 틱으로 돌아간다(50ms 간격). 10Hz마다 스냅샷을 UDP로 전송한다. 이 tick_hz/snapshot_hz 분리는 네트워크 대역폭과 시뮬레이션 정밀도의 트레이드오프다.

## 방과 매치의 상태 머신

`RoomContext`는 방 하나의 생명주기를 담는다:

1. **로비**: 플레이어 입장/퇴장, 레디 토글
2. **매치 시작 조건**: `players.size() == max_players` AND 전원 `READY=1`
3. **매치 진행**: `MatchState` 생성, 틱 타이머 스케줄링, UDP endpoint 관리
4. **매치 종료**: 결과 DB 저장, 방 해체, 플레이어 상태 초기화

방의 모든 작업은 `boost::asio::strand`에서 실행된다. strand는 해당 방의 이벤트를 직렬화하여, 멀티스레드 환경에서도 방 내부 상태에 대한 동시 접근을 방지한다. 전역 상태(`players_`, `rooms_`, `matches_`)는 `std::mutex`로 보호한다.

## Reconnect 메커니즘

TCP 연결이 끊어져도 게임이 즉시 끝나지 않는다. `resume_window_ms`(기본 20초) 이내에 `RESUME token=<token>`으로 재접속하면:

1. 기존 세션 상태 복구
2. `MatchState::mark_reconnected()` 호출
3. 현재 스폰 위치와 함께 `MATCH_START` 재전송
4. UDP endpoint 재등록 대기

타임아웃이 지나면 `forfeit` 처리된다. `mark_disconnected()`가 호출되고, `resume_window_ms` 초과 시 해당 플레이어는 매치에서 퇴장 처리된다.

## SQLite Persistence

`SqliteRepository`가 세 테이블을 관리한다:

- `players`: 계정 (name 유니크)
- `player_stats`: 누적 전적 (wins, losses, kills, deaths)
- `match_history`: 매치 기록 (시작/종료 시각, 승자, 결과 blob)

`login_or_create()`는 이름으로 조회 → 없으면 INSERT → 있으면 last_login_at 갱신. `record_match()`는 매치 종료 시 전적 업데이트와 히스토리 INSERT를 트랜잭션으로 수행한다.

production 인증이나 비밀번호는 범위 밖이다 — 이것은 네트워크 프로그래밍 학습용 서버이므로, 이름만으로 로그인하는 "local dev login"을 사용한다.

## 빌드 시스템

CMake + C++20. 의존성은 Boost(헤더 전용, Asio)와 SQLite3. 

`arena_core` 정적 라이브러리에 `protocol.cpp`, `state.cpp`, `repository.cpp`를 묶고, 세 개의 실행 파일이 이를 링크한다:
- `arena_server`: 서버 본체
- `arena_bot`: 단일 봇 클라이언트
- `arena_loadtest`: 다중 봇 부하 테스트

## 테스트 전략

세 계층:

1. **CTest 단위 테스트**: `test_protocol.cpp` (직렬화/파싱), `test_state.cpp` (시뮬레이션 로직), `test_repository.cpp` (DB 연산) — 네트워크 없이 순수 로직 검증
2. **Integration test** (`integration_test.py`): 실제 서버 프로세스를 띄우고 TCP/UDP로 시나리오 수행 — reconnect, forfeit, UDP ordering
3. **Load smoke test** (`load_smoke_test.py`): 8 bots / 2 rooms 동시 실행으로 동시성과 안정성 검증

`make test`가 세 계층을 순차 실행한다.

## 이 프로젝트가 보여주는 것

단순히 "게임 서버를 만들었다"가 아니다. 이 프로젝트는:
- TCP와 UDP의 적절한 역할 분담을 이해하고 있음을 보여준다
- strand 기반 동시성 모델로 멀티스레드 서버를 안전하게 구축할 수 있음을 보여준다
- 바이너리 프로토콜 설계와 텍스트 프로토콜 설계를 모두 할 수 있음을 보여준다
- 상태 머신, reconnect, persistence까지 갖춘 실용적 서버를 빌드부터 테스트까지 자동화할 수 있음을 보여준다

9개 프로젝트에서 조각조각 배운 것들이 하나의 시스템 안에서 작동하는 것을 확인하는 것 — 그것이 캡스톤의 의미다.
