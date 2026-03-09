# arenaserv — 접근 방식: ticklab core를 복제하되 import하지 않는다

작성일: 2026-03-09

## 핵심 결정: copy vs import

`arenaserv`를 시작할 때 가장 중요한 결정은 `ticklab`의 `MatchEngine`을 어떻게 가져올 것인가였다.

### 접근 A: ticklab 없이 바로 서버를 만든다

장점은 코드 수가 줄어든다는 것이다. 하지만 단점이 치명적이었다 — match rule bug와 socket bug가 한 곳에 섞인다. "투사체가 안 맞는 건 물리 로직 때문인가, 아니면 네트워크에서 입력이 유실된 것인가?"를 구분할 수 없다.

### 접근 B: ticklab core를 복제해 네트워크에 연결한다

이 방법을 택했다. `ticklab`에서 네 개의 테스트로 검증한 `MatchEngine`을 그대로 복사해서 `arenaserv/cpp/src/MatchEngine.cpp`에 넣었다. **import(헤더 참조)가 아니라 copy(파일 복사)**다.

copy를 택한 이유: 이 저장소에서 각 프로젝트는 독립적으로 `make clean && make && make test`가 돌아야 한다. ticklab에 대한 빌드 의존성을 만들면 이 독립성이 깨진다. 학습 우선 구조에서는 코드 중복보다 concept boundary의 선명함이 더 중요하다.

대가: `ticklab`에서 `MatchEngine` 버그를 수정하면, `arenaserv`에도 동일한 수정을 반영해야 한다. 이건 수동으로 관리해야 하는 부분이다.

## 아키텍처: 두 개의 핵심 클래스

`arenaserv`의 구조는 의외로 단순하다. 핵심 클래스가 두 개다:

1. **MatchEngine** — ticklab에서 복제한 시뮬레이션 엔진. room phase, player state, projectile, tick advance, snapshot 생성을 담당한다.
2. **Server** — EventManager 위에 올린 TCP 서버. 소켓 읽기/쓰기, 명령 파싱, MatchEngine API 호출, 이벤트 flush를 담당한다.

IRC 서버(roomlab/ircserv)와 달리 `Connection`, `Channel`, `Executor`, `Parser` 같은 중간 계층이 없다. 프로토콜이 단순하기 때문이다 — CRLF로 구분된 한 줄 명령을 파싱하고, MatchEngine의 적절한 함수를 호출하면 끝이다.

## tick scheduler: single-threaded loop에서 시뮬레이션 돌리기

가장 까다로운 세부 결정이었다. 게임 서버에서 tick은 일정한 간격(여기서는 100ms)으로 실행되어야 한다. 두 가지 방법이 있다:

1. **별도 스레드에서 timer를 돌린다**: tick 스레드와 네트워크 스레드 사이에 동기화가 필요하다.
2. **event loop의 timeout을 짧게 잡아서, 타임아웃마다 tick을 확인한다**: single-threaded로 가능하다.

2번을 택했다. `EventManager::retrieve_events()`에 timeout parameter(50ms)를 전달하고, event가 없어도 50ms마다 리턴한다. `pump_ticks()`가 `current_millis() - last_tick_ms >= tick_interval_ms`를 확인하고, 조건이 맞으면 `engine.advance_one_tick()`을 호출한다. 밀린 tick이 여러 개면 while loop에서 한 번에 따라잡는다.

이렇게 하면 별도 스레드 없이, 동기화 없이, single-threaded loop에서 시뮬레이션이 돌아간다.

## reconnect 설계

reconnect는 `REJOIN <token>` 명령으로 처리된다. 핵심은 **token ownership과 socket ownership의 분리**다:

- `disconnect()`: 소켓을 닫고 `token_to_fd`에서 fd 매핑을 제거하지만, MatchEngine 내부의 Participant 데이터는 유지한다. `engine.disconnect_player(token)`을 호출해 `connected = false`와 `disconnect_tick`만 표시한다.
- `REJOIN <token>`: 새 소켓에서 온 명령이다. `engine.rejoin_player(token)`을 호출하고, 성공하면 새 fd를 `token_to_fd`에 매핑한다.

grace window(10초 = 100 tick × 100ms)가 지나면 MatchEngine의 `expire_disconnected_players()`가 세션을 만료시키고, 이후 REJOIN은 `expired_session` 에러를 반환한다.
