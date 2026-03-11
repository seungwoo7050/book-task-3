# ircserv — 분리했던 세 층을 다시 합쳐 하나의 서버를 만든다

작성일: 2026-03-08

## 여기까지 오는 데 세 개의 lab이 필요했다

`eventlab`에서 이벤트 루프를 분리했다. `msglab`에서 IRC line parser를 분리했다. `roomlab`에서 registration과 room lifecycle이라는 state machine을 분리했다. 세 lab은 각각 하나의 계층만 다루었고, 그 덕분에 한 번에 하나의 관심사에만 집중할 수 있었다.

그런데 실제 IRC 서버는 이 세 계층이 하나의 프로세스 안에서 동시에 돌아간다. `ircserv`는 이 세 계층을 다시 합치는 과제다. 그리고 합치는 과정에서, `roomlab`이 의도적으로 제외했던 IRC 기능들을 다시 활성화한다.

## 이 capstone이 추가하는 것

`roomlab`의 10개 명령(PASS, NICK, USER, JOIN, PART, PRIVMSG, NOTICE, PING, PONG, QUIT) 위에 다음을 추가한다:

- **`CAP LS 302`** — 최소 capability advertisement. IRC 클라이언트가 연결 시 서버 기능을 물어보는 표준 절차.
- **`005 ISUPPORT`** — 서버가 지원하는 제약(닉네임 길이, 채널 개수 제한, 채널 타입 등)을 알려주는 numeric.
- **`TOPIC`** — 채널 토픽 설정/조회.
- **`MODE`** — 채널 모드 변경 (+i invite-only, +t topic restricted, +k key, +o operator, +l limit).
- **`KICK`** — 채널에서 사용자를 강제 퇴장.
- **`INVITE`** — invite-only 채널에 사용자를 초대.

핵심은 "기능을 최대한 많이 넣는 것"이 아니라, **"앞서 분리한 개념이 실제 서버로 어떻게 통합되는지"를 보여주는 것**이다.

## 포함한 것과 제외한 것

포함:
- cross-platform event loop (kqueue/epoll)
- raw IRC line protocol (CRLF 기반)
- channel operator privilege
- invite-only channel
- topic/mode/kick/invite
- minimal capability negotiation

제외:
- WebSocket — 이 저장소에서 다루지 않음
- React frontend — 이 저장소에서 다루지 않음
- game logic — `ticklab`/`arenaserv`의 영역
- MySQL/Redis persistence — 범위 밖
- metrics와 운영 배포 — 범위 밖
- TLS, SASL, operator services — RFC 완전 구현이 목표가 아님

## 성공 기준

1. `make clean && make && make test`가 통과한다.
2. 세 클라이언트(alice, bob, carol)가 registration을 완료한다.
3. `CAP LS 302`에 대한 응답이 온다.
4. `005 ISUPPORT`가 보인다.
5. alice가 `MODE #ops +i`로 invite-only를 설정한다.
6. alice가 `INVITE carol #ops`를 보내고, carol이 `JOIN #ops`에 성공한다.
7. alice가 `TOPIC #ops :control room`을 설정하고 carol이 수신한다.
8. alice가 `KICK #ops bob :bye`를 보내고 bob이 퇴장된다.
9. kick된 bob이 invite-only 채널에 재입장을 시도하면 `473 ERR_INVITEONLYCHAN`이 온다.
10. `PING/PONG`이 동작한다.

## 참고한 자료

| 자료 | 경로 | 왜 봤는가 | 무엇을 알게 되었는가 |
| --- | --- | --- | --- |
| Legacy README | `legacy/README.md` | pure IRC 부분의 경계 확인 | 제품 전체에서 순수 IRC 핵심과 확장 기능을 구분할 수 있었다 |
| Legacy Executor | `legacy/src/Executor.cpp` | advanced IRC command 흐름 확인 | TOPIC/MODE/KICK/INVITE가 이미 구현되어 있어 다시 활성화할 수 있었다 |
| Legacy Server loop | `legacy/src/Server.cpp` | event loop와 keep-alive 흐름 확인 | 제품 수준의 lifecycle 관리를 pure TCP로 축소할 수 있었다 |
| Legacy Channel model | `legacy/src/Channel.cpp` | operator/invite/mode state 확인 | channel state bit가 MODE/INVITE/KICK의 기반이 된다 |
