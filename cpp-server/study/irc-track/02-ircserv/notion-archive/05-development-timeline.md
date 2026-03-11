# ircserv — 개발 타임라인: 세 lab의 통합과 advanced IRC 추가

작성일: 2026-03-08

이 문서는 ircserv capstone의 전체 개발 과정을 시간순으로 복원한다. 소스코드에서는 드러나지 않는 의사결정, 파일 생성 순서, 테스트 안정화 과정을 기록한다.

---

## Phase 0: 환경과 도구

roomlab과 동일한 환경이다. 별도 패키지 설치 없음.

```
c++ --version        # Apple clang, C++17
python3 --version    # smoke test runner
make --version       # GNU Make
```

| 도구 | 용도 | 비고 |
| --- | --- | --- |
| Apple Clang (c++) | C++17 컴파일 | `-Wall -Wextra -Werror -std=c++17 -MMD -MP -pthread` |
| GNU Make | 빌드 시스템 | `make clean && make && make test` |
| Python 3 | smoke test | socket 기반 3-client 시나리오 |
| nc (netcat) | 수동 테스트 | CAP, MODE, INVITE, KICK 흐름 수동 확인 |

---

## Phase 1: roomlab에서 시작 — 파일 구조 동일

ircserv의 시작점은 roomlab이다. 같은 11개 소스 파일, 같은 10개 헤더를 복사한 뒤 확장했다.

```
study/ircserv/cpp/
├── Makefile             # NAME := ircserv
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
│   ├── Channel.cpp      # mode flag 활성화
│   ├── Connection.cpp
│   ├── EventManager.cpp
│   ├── Executor.cpp     # TOPIC/MODE/KICK/INVITE handler 추가
│   ├── Message.cpp
│   ├── Parser.cpp
│   ├── Server.cpp       # CAP LS 302 처리 추가
│   ├── debug.cpp
│   ├── execute_join.cpp
│   ├── main.cpp
│   └── utils.cpp
└── tests/
    └── test_irc_join.py  # 11개 시나리오
```

바이너리 이름: `ircserv` (roomlab의 `roomlabd`와 다름)

---

## Phase 2: advanced command handler 추가

roomlab에서 제거했던 command handler들을 Executor에 다시 추가했다:

### `_execute_topic()`
- `MODE +t`가 설정된 채널에서는 operator만 TOPIC 변경 가능
- TOPIC 조회와 설정을 분리 (파라미터 유무에 따라)
- 변경 시 채널 전체에 broadcast

### `_execute_mode()`
- `+i` (invite-only), `+t` (topic restricted), `+k` (key), `+o` (operator grant/revoke), `+l` (limit) 지원
- 각 mode에 필요한 파라미터 검증
- 변경 결과를 채널 전체에 broadcast

### `_execute_kick()`
- operator 권한 검증
- target connection의 `chandb`에서 채널 제거 (stale state 방지)
- `chan->part(targetnode)` 호출로 channel 측 membership 정리
- KICK 이벤트를 채널 전체에 broadcast

### `_execute_invite()`
- invite-only 채널에 대한 operator 권한 검증
- target의 `invitedb`에 추가
- inviter에게 341 RPL_INVITING 전송
- target에게 INVITE 이벤트 전송

---

## Phase 3: Channel mode flag 활성화

roomlab에서 비활성 상태로 남겨두었던 Channel의 mode flag들이 ircserv에서 활성화되었다:

| Flag | 비트 | roomlab 상태 | ircserv 상태 |
| --- | --- | --- | --- |
| `lbit` (client limit) | 1 | 항상 0 | MODE +l로 설정 가능 |
| `ibit` (invite only) | 2 | 항상 0 | MODE +i로 설정 가능 |
| `tbit` (protected topic) | 4 | 항상 0 | MODE +t로 설정 가능 |
| `kbit` (key required) | 8 | 항상 0 | MODE +k로 설정 가능 |

이 변화의 효과: `execute_join.cpp`의 key/invite/limit 체크 코드가 **실제로 동작하기 시작한다**. roomlab에서는 "도달하지 않는 코드"였던 것이 ircserv에서는 "활성 경로"가 된다.

---

## Phase 4: CAP LS 302 추가

registration 흐름 전에 `CAP LS 302`를 처리할 수 있어야 했다. Server의 read handler에서 CAP 명령을 감지하면 빈 capability list로 응답한다:

```
Client → Server: CAP LS 302
Server → Client: :irc CAP * LS :
```

이 최소 구현으로 `irssi` 같은 클라이언트가 연결 시 capability negotiation을 시도해도 정상적으로 진행할 수 있다.

---

## Phase 5: 하위 lab 버그 포팅

roomlab, msglab에서 발견한 버그들을 ircserv에도 동일하게 반영:

1. **prefix parsing 후 token.clear()** — parser가 prefix 읽은 뒤 임시 토큰을 비우지 않는 문제
2. **PING parameter count** — 빈 parameter 접근 방지
3. **nickname validator 인덱스** — 첫 글자/나머지 검증 규칙의 인덱스 오프셋 수정
4. **non-IRC field 제거** — Message/Connection 구조체에서 게임용 필드 제거

---

## Phase 6: Smoke test 작성

11개 시나리오를 하나의 Python 테스트에 담았다. 세 클라이언트(alice, bob, carol)를 동시에 연결:

```python
# 역할 분담
# alice: channel founder, operator — JOIN, MODE, INVITE, TOPIC, KICK 수행
# bob: 일반 member — JOIN, KICK 대상, invite-only 재입장 시도
# carol: invited guest — INVITE 수신 후 JOIN
```

시나리오 순서:
1. CAP LS 302 → 응답 확인
2. alice, bob, carol registration → 005 ISUPPORT 확인
3. alice JOIN #ops → bob JOIN #ops
4. alice MODE #ops +i → broadcast 확인
5. alice INVITE carol #ops → 341 + carol에게 INVITE 이벤트
6. `time.sleep(0.2)` → carol JOIN #ops (invite 후 가입)
7. alice TOPIC #ops :control room → carol에게 broadcast
8. alice PRIVMSG #ops :hello capstone → carol에게 broadcast
9. alice KICK #ops bob :bye → bob에게 KICK 이벤트
10. `time.sleep(0.2)` → bob JOIN #ops → 473 ERR_INVITEONLYCHAN
11. alice PING capstone → PONG 응답

---

## Phase 7: 테스트 안정화

두 가지 타이밍 문제를 수정:

1. **INVITE 직후 JOIN**: carol이 INVITE를 수신한 직후 JOIN을 보내면 간헐적 실패 → `time.sleep(0.2)` 삽입
2. **KICK 직후 재입장**: bob이 KICK된 직후 JOIN을 보내면 이전 출력의 버퍼 잔여물로 매칭 오류 → `time.sleep(0.2)` 삽입 + recv deadline 8초로 확대

두 수정 모두 서버 로직 변경이 아니라 테스트 안정화다.

---

## Phase 8: KICK stale state 수정

테스트 안정화 과정에서 발견된 **유일한 서버 버그**:

- KICK 처리에서 `chan->part(targetnode)`는 channel 측 membership을 정리하지만, target connection의 `chandb`를 정리하지 않았다.
- 수정: `targetnode->chandb.erase(channame)`을 `chan->part()` 전에 명시적으로 추가

---

## 최종 빌드와 확인

```bash
make clean && make && make test
# → ircserv capstone smoke passed.
```

바이너리: `ircserv`, 사용법: `./ircserv <port> <password>`

11개 소스 파일이 컴파일되고, Python smoke test가 11개 시나리오를 통과하면 ircserv capstone은 완성이다.
