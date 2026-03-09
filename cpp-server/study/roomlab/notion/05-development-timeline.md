# roomlab — 개발 타임라인: event loop + parser → state machine

작성일: 2026-03-09

이 문서는 roomlab의 전체 개발 과정을 시간순으로 복원한다. 소스코드에서는 드러나지 않는 의사결정, 파일 생성 순서, 도구 사용 내역을 기록한다.

---

## Phase 0: 환경과 도구

roomlab은 eventlab, msglab과 동일한 환경에서 시작한다. 별도의 패키지 설치는 없었다.

```
c++ --version        # Apple clang, C++17
python3 --version    # smoke test runner
make --version       # GNU Make
```

| 도구 | 용도 | 비고 |
| --- | --- | --- |
| Apple Clang (c++) | C++17 컴파일 | `-Wall -Wextra -Werror -std=c++17 -MMD -MP -pthread` |
| GNU Make | 빌드 시스템 | `make clean && make && make test` |
| Python 3 | smoke test | socket 기반 multi-client 시나리오 |
| nc (netcat) | 수동 테스트 | 초기 registration 흐름 수동 확인 |

---

## Phase 1: legacy 분석과 범위 결정

roomlab은 다른 lab과 달리 완전히 새로 작성하지 않았다. legacy IRC 서버 코드가 이미 존재했고, 거기서 core subset을 추출하는 방식을 택했다.

### 어떤 파일을 가져올 것인가

legacy 코드를 훑으면서 다음과 같이 분류했다:

| 파일 | 판단 | 이유 |
| --- | --- | --- |
| `EventManager.cpp/.hpp` | **재사용** | eventlab에서 검증 완료, 이벤트 루프는 동일 |
| `Connection.cpp/.hpp` | **추출** | registration flag, channel membership 관리 코드 보존, 비-IRC 필드 제거 |
| `Channel.cpp/.hpp` | **추출** | room lifecycle 핵심, mode flag는 비활성 상태로 보존 |
| `Executor.cpp/.hpp` | **추출** | 10개 core command handler만 남기고 나머지 제거 |
| `execute_join.cpp` | **추출** | JOIN/PART 및 JOIN 0 logic 보존, key/invite/limit 체크는 비활성 |
| `Server.cpp/.hpp` | **추출** | event loop integration, connection lifecycle, WebSocket/game 제거 |
| `Message.cpp/.hpp` | **재사용** | msglab에서 검증된 구조 |
| `Parser.cpp/.hpp` | **재사용** | msglab에서 검증된 파서 |
| `main.cpp` | **새로 작성** | signal handling, 인자 검증 (`<port> <password>`) |
| `debug.cpp/.hpp` | **재사용** | 디버그 출력 유틸리티 |
| `utils.cpp/.hpp` | **재사용** | legacy 유틸리티 |
| `macros.hpp` | **추출** | numeric reply 매크로, 사용하지 않는 매크로 제거 |

핵심 판단: "재사용"은 파일을 그대로 복사한 것, "추출"은 파일을 가져온 뒤 내부에서 불필요한 코드를 제거한 것이다.

---

## Phase 2: 파일 구조 확립

```
study/roomlab/cpp/
├── Makefile
├── include/inc/
│   ├── Channel.hpp
│   ├── Connection.hpp
│   ├── EventManager.hpp
│   ├── Executor.hpp
│   ├── Message.hpp
│   ├── Parser.hpp
│   ├── Server.hpp
│   ├── debug.hpp
│   ├── macros.hpp
│   └── utils.hpp
├── src/
│   ├── Channel.cpp
│   ├── Connection.cpp
│   ├── EventManager.cpp
│   ├── Executor.cpp
│   ├── Message.cpp
│   ├── Parser.cpp
│   ├── Server.cpp
│   ├── debug.cpp
│   ├── execute_join.cpp
│   ├── main.cpp
│   └── utils.cpp
└── tests/
    └── test_roomlab.py
```

소스 파일 11개, 헤더 10개. 이전 lab들(eventlab 4개, msglab 3개)에 비해 규모가 크지만, 이는 state machine 자체의 복잡도를 반영한다.

---

## Phase 3: legacy 정리 — 무엇을 제거했는가

이 phase가 roomlab 개발의 핵심이었다. 코드를 새로 작성하는 것이 아니라, 기존 코드에서 범위 밖의 것들을 정밀하게 제거하는 작업이었다.

### Executor에서 제거한 command handler

- `_execute_topic()` — TOPIC 명령 처리
- `_execute_mode()` — MODE 명령 처리 (channel mode 변경)
- `_execute_kick()` — KICK 명령 처리
- `_execute_invite()` — INVITE 명령 처리

### Channel에서 비활성화된 필드 (코드에 남아 있으나 runtime에 도달하지 않음)

- `state` (mode bitmask) — MODE command 없이는 항상 0
- `invitedb` — INVITE command 없이 항상 비어 있음
- `key` — MODE +k 없이 항상 빈 문자열
- `topic`, `topic_setter`, `topic_time` — TOPIC 없이 사용되지 않음
- `limit` — MODE +l 없이 항상 0

이것들을 삭제하지 않은 이유: `execute_join.cpp`의 key/invite/limit 체크 코드가 이 필드들을 참조한다. 해당 조건 분기는 flag가 0이므로 절대 true가 되지 않지만, 코드를 삭제하면 `ircserv`에서 다시 추가해야 한다. "비활성이지만 구조적으로 유효한 코드"를 유지하는 편을 택했다.

### Server에서 제거한 것

- WebSocket upgrade 경로
- 게임 세션 관리 코드
- metrics 수집 코드

---

## Phase 4: Registration state machine 구현 확인

Registration 흐름을 수동으로 검증:

```bash
make clean && make
./roomlabd 6671 password &

# 터미널에서 nc로 수동 테스트
nc 127.0.0.1 6671
PASS password
NICK testuser
USER testuser 0 * :Test User
# → 001, 002, 003, 004, 005 numeric reply 확인
```

확인한 사항:
- PASS 전에 NICK을 보내면 `ERR_NOTREGISTERED` 반환
- 잘못된 password로 PASS를 보내면 `ERR_PASSWDMISMATCH` 후 connection doom
- 이미 사용 중인 nick으로 NICK을 보내면 `ERR_NICKNAMEINUSE` 반환
- USER 완료 후 welcome 시퀀스(001-005) 전송 확인

---

## Phase 5: Room lifecycle 구현 확인

```bash
# 두 개의 터미널에서 동시에 nc로 접속
# Terminal 1: alice
nc 127.0.0.1 6671
PASS password
NICK alice
USER alice 0 * :alice
JOIN #lab

# Terminal 2: bob
nc 127.0.0.1 6671
PASS password
NICK bob
USER bob 0 * :bob
JOIN #lab
# → alice에게 ":bob JOIN #lab" 브로드캐스트 확인

# alice가 메시지 전송
PRIVMSG #lab :hello
# → bob에게 ":alice PRIVMSG #lab :hello" 수신 확인
```

---

## Phase 6: Smoke test 작성

수동 테스트가 통과한 후, 6개의 시나리오를 자동화한 `test_roomlab.py`를 작성했다:

1. alice, bob 등록 (PASS → NICK → USER → 001 확인)
2. alice JOIN #lab → bob JOIN #lab
3. alice → bob channel broadcast (PRIVMSG)
4. bob → alice direct notice (NOTICE)
5. dup 소켓으로 alice nick 시도 → 433 ERR_NICKNAMEINUSE 확인
6. alice QUIT :gone away → bob에게 QUIT broadcast 확인
7. dup이 채널에 가입하지 않은 상태에서 PART → 442 ERR_NOTONCHANNEL 확인

```bash
make test
# → roomlab smoke passed.
```

테스트는 세 개의 소켓(alice, bob, dup)을 동시에 열어 multi-client 시나리오를 커버한다. `recv_until()` 함수로 타임아웃이 있는 기대값 매칭을 수행한다.

---

## Phase 7: QUIT vs disconnect 검증

smoke test에서 QUIT broadcast는 확인했지만, EOF disconnect(소켓을 그냥 닫는 경우)도 코드 리뷰로 검증했다:

- `Server::_run_event_loop()`의 read handler에서 `event.eof`를 감지하면 `Executor::to_doom()`을 broadcast 없이 호출
- doomed connection은 send buffer를 비운 뒤 `_disconnect()`에서 인덱스 정리 및 소켓 close
- 이 경로에서 채널 멤버에게 별도 통보가 없는 것이 의도된 동작임을 확인

---

## 최종 빌드와 확인

```bash
make clean && make && make test
# → roomlab smoke passed.
```

바이너리: `roomlabd`, 사용법: `./roomlabd <port> <password>`

11개의 소스 파일이 컴파일되고, Python smoke test가 6개 시나리오를 통과하면 roomlab은 완성이다.
