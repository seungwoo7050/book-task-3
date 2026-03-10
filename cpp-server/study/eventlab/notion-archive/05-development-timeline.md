# eventlab — 개발 타임라인

작성일: 2026-03-08

이 문서는 `eventlab` 프로젝트의 전체 개발 과정을 시간순으로 기록한다. 소스코드만으로는 알 수 없는 정보 — 어떤 순서로 파일을 만들었고, 어떤 명령을 실행했고, 어떤 판단을 내렸는지 — 를 복원할 수 있도록 하는 것이 목적이다.

---

## Phase 0: 환경 준비

### 전제 조건

- macOS 환경, C++17 지원 컴파일러 (`c++` = Apple Clang)
- Python 3 (smoke test 실행용)
- `legacy/` 디렉토리에 원본 프로젝트가 보존되어 있는 상태

### 디렉토리 생성

```sh
mkdir -p study/eventlab/cpp/src
mkdir -p study/eventlab/cpp/include/inc
mkdir -p study/eventlab/cpp/tests
mkdir -p study/eventlab/docs/concepts
mkdir -p study/eventlab/docs/references
mkdir -p study/eventlab/notion
mkdir -p study/eventlab/problem/code
mkdir -p study/eventlab/problem/data
mkdir -p study/eventlab/problem/script
```

`study/` 아래의 모든 프로젝트는 동일한 디렉토리 템플릿을 따른다. 이 구조는 `docs/study-project-template.md`에 정의되어 있다.

---

## Phase 1: EventManager 재사용 결정과 파일 복사

### 레거시 코드 분석

먼저 `legacy/src/EventManager.cpp`와 `legacy/src/inc/EventManager.hpp`를 읽었다. kqueue(macOS)와 epoll(Linux) 양쪽을 감싸는 추상화가 이미 정리되어 있었다. 이걸 새로 짤 필요는 없었다.

```sh
# 레거시에서 재사용할 파일 복사
cp legacy/src/EventManager.cpp study/eventlab/cpp/src/
cp legacy/src/inc/EventManager.hpp study/eventlab/cpp/include/inc/

# I/O helper도 함께 복사
cp legacy/src/utils.cpp study/eventlab/cpp/src/
cp legacy/src/inc/utils.hpp study/eventlab/cpp/include/inc/
```

### 의식적으로 복사하지 않은 것

- `Server.cpp` — IRC 명령 파서, executor, channel 상태와 결합되어 있어서 그대로 가져오면 lab 목적에 어긋난다.
- `Connection.cpp`, `Channel.cpp`, `Executor.cpp` — 전부 IRC 전용이다.
- `Message.cpp`, `Parser.cpp` — 이후 `msglab`에서 별도로 다룰 것이다.

---

## Phase 2: Server 신규 작성

### Server.hpp 작성

`include/inc/Server.hpp`를 새로 작성했다. 레거시의 Server와 같은 구조적 골격을 따르되, IRC 전용 멤버를 모두 제거했다.

핵심 결정:
- `Client` 구조체: `fd`, `ipaddr`, `recvbuf`, `sendbuf`, `timestamp`, `pinged`, `doomed`
- `timeout = 2초`, `cutoff = 5초` — smoke test를 위해 짧게 설정
- `sendq`는 `std::set<int>` — write readiness를 요청할 fd 모음

### Server.cpp 작성

`src/Server.cpp`를 처음부터 작성했다. 레거시 Server의 event loop 구조를 참고하되, 프로토콜 처리를 최소한으로 줄였다.

구현 순서:
1. **생성자/소멸자**: 포트 유효성 검사, listening socket 열기, 소멸 시 전체 fd 정리
2. **`run()`**: SIGINT 이벤트 등록 → listen socket read 등록 → main loop 진입
3. **`run_event_loop()`**: EventManager에서 이벤트를 가져와 type별로 분기
   - Signal → `interrupt = true`
   - Read + listenfd → accept
   - Read + clientfd → recv → process_input
   - Write → send_packet → flush sendbuf
4. **`keep_alive()`**: event loop cycle 시작 시 idle 검사 — timeout 초과 시 `PING :idle-check` 전송, cutoff 초과 시 disconnect
5. **`handle_line()`**: 프로토콜 핵심 — `QUIT` → BYE, `PING` → PONG, 그 외 → ECHO
6. **`accept_connection()`**, **`disconnect()`**, **`read_packet()`**, **`send_packet()`**, **`process_input()`**, **`queue_reply()`**

### main.cpp 작성

`src/main.cpp`를 작성했다. 레거시의 signal 처리 패턴을 그대로 유지했다.

- `SIGPIPE`, `SIGQUIT`, `SIGTSTP` → `SIG_IGN`
- macOS: `SIGINT`도 `SIG_IGN` (EventManager가 kqueue EVFILT_SIGNAL로 처리)
- Linux: `SIGINT`를 `sigprocmask`로 `SIG_BLOCK` (EventManager가 signalfd로 처리)

```sh
# 이 시점에서의 파일 구조
study/eventlab/cpp/
├── Makefile
├── include/inc/
│   ├── EventManager.hpp
│   ├── Server.hpp
│   └── utils.hpp
├── src/
│   ├── EventManager.cpp
│   ├── Server.cpp
│   ├── main.cpp
│   └── utils.cpp
└── tests/
```

---

## Phase 3: Makefile 작성과 첫 빌드

### Makefile

```makefile
NAME := eventlabd
CXX := c++
CXXFLAGS := -Wall -Wextra -Werror -std=c++17 -MMD -MP -pthread
CPPFLAGS := -I include -I include/inc
```

바이너리 이름을 `eventlabd`로 정했다 — 서버 데몬이라는 의미다.

### 첫 빌드

```sh
cd study/eventlab/cpp
make clean && make
```

첫 빌드에서 EventManager의 kqueue 관련 include가 문제없이 통과하는 것을 확인했다. 이 시점에서 서버를 수동으로 실행해 봤다:

```sh
./eventlabd 6670
```

그리고 다른 터미널에서:

```sh
# 터미널 2
nc localhost 6670
# → WELCOME 127.0.0.1 수신 확인
# hello world 입력
# → ECHO hello world 수신 확인
# PING test 입력
# → PONG test 수신 확인
# QUIT 입력
# → BYE 수신 후 연결 종료 확인
```

이 수동 테스트로 기본 경로가 동작하는 것을 확인한 뒤 smoke test 작성으로 넘어갔다.

---

## Phase 4: Smoke Test 작성

### test_eventlab.py

`tests/test_eventlab.py`를 Python으로 작성했다. 서버를 subprocess로 띄우고, socket으로 연결해서 시나리오를 순차 실행하는 구조다.

테스트 시나리오 순서:
1. 서버 프로세스 시작 (`./eventlabd <port>`)
2. `wait_for_port()` — 서버가 포트를 열 때까지 polling
3. 클라이언트 A, B 동시 접속
4. 양쪽 `WELCOME` 수신 확인
5. A에서 일반 입력 → `ECHO` 수신 확인
6. A에서 `PING keepalive` → `PONG keepalive` 수신 확인
7. 3초 대기 후 A에서 `PING wakeup` 전송 (서버를 깨움)
8. B에서 `PING :idle-check` 수신 확인 (idle keep-alive)
9. A에서 `QUIT` → `BYE` 수신 확인

### keep-alive 테스트의 어려움

7~8번 단계에서 문제가 발생했다. 처음에는 B의 idle을 감지할 수 있도록 단순히 몇 초를 기다렸지만, 서버가 이벤트 없이 잠들어 있어서 keep-alive 검사가 트리거되지 않았다. 해결 방법은 A에서 작은 `PING`을 보내 서버를 깨우는 것이었다. 이 과정은 02-debug-log에 자세히 기록했다.

```sh
# 테스트 실행
cd study/eventlab/cpp
make test
# → eventlab smoke passed.
```

### Makefile의 test target

```makefile
test: $(NAME)
	python3 tests/test_eventlab.py
```

테스트가 성공하면 `eventlab smoke passed.`를 출력하고, 실패하면 에러 메시지와 함께 exit code 1을 반환한다. 서버 프로세스는 테스트 종료 시 SIGINT로 정리된다.

---

## Phase 5: 문서 작성

### 프로젝트 문서

다음 파일들을 순서대로 작성했다:

1. `problem/README.md` — 재구성된 문제 설명
2. `cpp/README.md` — 구현 상태, 빌드/테스트 명령, known gaps
3. `docs/README.md` — 핵심 개념 포인터
4. `README.md` (프로젝트 루트) — 프로젝트 소개와 진입점 링크

### notion/ 문서

개발 과정의 기록으로 다음을 작성했다:

1. `00-problem-framing.md` — 문제 해석과 범위 정의
2. `01-approach-log.md` — 접근 선택지와 결정 과정
3. `02-debug-log.md` — 실제 부딪힌 문제와 해결
4. `03-retrospective.md` — 완료 후 회고
5. `04-knowledge-index.md` — 재사용 가능한 개념과 참고 자료

---

## Phase 6: 최종 검증

```sh
cd study/eventlab/cpp
make clean && make && make test
# → eventlab smoke passed.
```

빌드와 테스트가 모두 통과하는 것을 확인한 뒤, README에 `verified` 상태를 표기했다.

---

## 최종 파일 목록

```
study/eventlab/
├── README.md
├── cpp/
│   ├── Makefile
│   ├── README.md
│   ├── include/inc/
│   │   ├── EventManager.hpp
│   │   ├── Server.hpp
│   │   └── utils.hpp
│   ├── src/
│   │   ├── EventManager.cpp   ← legacy에서 재사용
│   │   ├── Server.cpp         ← 신규 작성
│   │   ├── main.cpp           ← 신규 작성
│   │   └── utils.cpp          ← legacy에서 재사용
│   └── tests/
│       └── test_eventlab.py   ← 신규 작성
├── docs/
│   ├── README.md
│   ├── concepts/
│   └── references/
├── notion/
│   ├── 00-problem-framing.md
│   ├── 01-approach-log.md
│   ├── 02-debug-log.md
│   ├── 03-retrospective.md
│   ├── 04-knowledge-index.md
│   └── 05-development-timeline.md
└── problem/
    ├── README.md
    ├── code/
    ├── data/
    └── script/
```

## 사용한 주요 도구와 명령어 요약

| 도구/명령 | 용도 |
| --- | --- |
| `c++` (Apple Clang) | C++17 컴파일러 |
| `make` | 빌드 자동화 |
| `python3` | smoke test 실행 |
| `nc` (netcat) | 수동 소켓 테스트 |
| `cp` | 레거시 파일 복사 |
| `SIGINT` (Ctrl+C) | 서버 graceful shutdown |
| `kill -SIGINT` / `os.killpg` | 테스트에서 서버 프로세스 종료 |
