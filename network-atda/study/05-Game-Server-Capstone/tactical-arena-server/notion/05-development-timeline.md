# 05 개발 타임라인

이 문서는 `Tactical Arena Server`를 처음 재현하는 학생을 위한 가장 중요한 가이드다. 이 프로젝트는 범위가 넓기 때문에, 빌드와 테스트만 통과시키는 것보다 TCP/UDP 구조, 봇 데모, DB 결과까지 한 번에 확인하는 순서가 훨씬 중요하다.

## 준비
- C++20 컴파일러 (`clang++` 또는 `g++`)
- `cmake`
- Boost.Asio 헤더
- SQLite3 개발 패키지
- `python3`
- 작업 위치: 저장소 루트 `/Users/woopinbell/work/book-task-3/network-atda`

## 단계 1. 문제와 공개 문서부터 읽는다
먼저 아래 파일을 읽는다.
- [`../problem/README.md`](../problem/README.md)
- [`../problem/code/control-protocol.txt`](../problem/code/control-protocol.txt)
- [`../problem/data/schema.sql`](../problem/data/schema.sql)
- [`../cpp/README.md`](../cpp/README.md)
- [`../docs/concepts/architecture.md`](../docs/concepts/architecture.md)

여기서 확인할 질문:
- TCP와 UDP를 왜 분리했는가
- authoritative server가 무엇인가
- 어떤 테스트가 어떤 계층을 검증하는가

## 단계 2. 가장 먼저 전체 자동 검증을 실행한다
아래 명령으로 빌드와 테스트를 한 번에 수행한다.

```bash
make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test
```

기대 결과:
- `cmake` configure/build가 성공한다.
- `ctest` 단위 테스트가 통과한다.
- `integration_test.py`가 reconnect, forfeit, out-of-order UDP 시나리오를 통과한다.
- `load_smoke_test.py`가 부하 스모크를 통과한다.

## 단계 3. 바이너리와 소스 구조를 연결해 본다
자동 검증이 통과했다면 아래 파일을 짧게 확인한다.
- [`../cpp/src/arena_server.cpp`](../cpp/src/arena_server.cpp)
- [`../cpp/src/state.cpp`](../cpp/src/state.cpp)
- [`../cpp/src/protocol.cpp`](../cpp/src/protocol.cpp)
- [`../problem/script/integration_test.py`](../problem/script/integration_test.py)

이 단계에서 볼 포인트:
- TCP 세션과 UDP endpoint가 어디서 만나는가
- `MatchState::step()`이 어떤 순서로 한 틱을 처리하는가
- integration test가 어떤 시나리오를 공식 검증으로 삼는가

## 단계 4. 봇 데모로 실제 흐름을 본다
아래 명령으로 로컬 데모를 실행한다.

```bash
make -C study/05-Game-Server-Capstone/tactical-arena-server/problem run-bot-demo
```

기대 결과:
- 서버가 올라오고 두 봇이 로그인, 방 참가, 준비를 끝낸다.
- `MATCH_START` 이후 매치가 진행된다.
- 결과가 출력되고 DB 파일이 생성된다.

## 단계 5. DB와 발표 자료로 결과를 다시 확인한다
데모 뒤에는 아래 경로를 확인한다.
- `../problem/data/arena.sqlite3` 파일 생성 여부
- [`../docs/presentation/README.md`](../docs/presentation/README.md)
- [`../docs/presentation/assets/logs/`](../docs/presentation/assets/logs/)

로컬에 `sqlite3` CLI가 있으면 아래처럼 확인할 수 있다.

```bash
sqlite3 study/05-Game-Server-Capstone/tactical-arena-server/problem/data/arena.sqlite3 '.tables'
```

기대 결과:
- `players`, `player_stats`, `match_history` 테이블을 확인할 수 있다.
- 발표 자료와 로그로 데모 흐름을 다시 비교할 수 있다.

## 단계 6. 부하 스모크를 따로 다시 돌린다
아래 명령으로 부하 검증만 다시 실행할 수 있다.

```bash
make -C study/05-Game-Server-Capstone/tactical-arena-server/problem load-test
```

기대 결과:
- 로컬 서버 프로세스와 다중 봇 워커가 함께 동작한다.
- 최소한의 동시성/안정성 검증이 다시 통과한다.

## 단계 7. 실패하면 가장 먼저 볼 곳
- 빌드 실패면 Boost/SQLite 경로와 `cpp/CMakeLists.txt`를 먼저 본다.
- 포트 충돌이면 기본 TCP/UDP 포트 사용 여부를 확인한다.
- reconnect 문제가 보이면 `integration_test.py`의 `scenario_resume_same_player`와 서버의 token/resume 흐름을 함께 본다.
- DB가 비어 있으면 `record_match()` 경로와 sqlite 파일 경로를 먼저 확인한다.
- 관련 근거는 [`02-debug-log.md`](02-debug-log.md)에 정리했다.

## 단계 8. 완료 판정
아래 조건을 만족하면 이 프로젝트는 재현한 것으로 본다.
- `make test`가 통과한다.
- `run-bot-demo`를 직접 실행했다.
- sqlite DB 파일과 테이블을 확인했다.
- TCP/UDP 분리 이유, strand 기반 동시성, reconnect 검증 방식을 설명할 수 있다.
