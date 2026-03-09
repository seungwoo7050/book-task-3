# roomlab — 이벤트 루프와 파서가 만나 상태 머신이 되는 순간

작성일: 2026-03-09

## 여기까지 오는 데 필요했던 것

`eventlab`에서 이벤트 루프를 고립시켜 봤다. `msglab`에서 IRC line parser를 고립시켜 봤다. 두 lab은 각각 "소켓이 어떻게 읽고 쓰는가"와 "읽어온 텍스트가 어떤 의미를 갖는가"에 답했다.

그런데 한 가지 빠져 있다 — **그 의미를 해석한 뒤, 서버 상태가 어떻게 바뀌는가?** `NICK alice`를 받았으면 "alice"라는 사용자가 등록되어야 하고, `JOIN #lab`을 받았으면 해당 채널에 가입되어야 하고, `QUIT`를 받았으면 모든 채널에서 빠지면서 다른 사용자에게 알려야 한다.

이 질문들은 event loop도 parser도 답하지 못한다. **state machine**이 필요하다. `roomlab`은 이 state machine의 최소 버전을 직접 만들어보는 과제다.

## 문제를 이렇게 정의했다

다음 IRC 명령만 지원하는 C++17 pure TCP 서버를 작성한다:

- 등록: `PASS`, `NICK`, `USER`
- 채널: `JOIN`, `PART`
- 메시지: `PRIVMSG`, `NOTICE`
- 연결 관리: `PING`, `PONG`, `QUIT`

핵심은 **registration state consistency와 room lifecycle**이 명확하게 드러나는 것이다. IRC를 "완성"하는 것이 목표가 아니라, "앞서 분리한 두 계층이 실제 상태 머신으로 어떻게 연결되는지"를 보여주는 것이 목표다.

## 포함한 것과 제외한 것

포함:
- registration state (PASS → NICK → USER → registered)
- nickname/socket/channel index 관리
- room join/part lifecycle
- `PRIVMSG`/`NOTICE` delivery (채널 broadcast)
- keep-alive와 disconnect cleanup

제외:
- `TOPIC`, `MODE`, `KICK`, `INVITE`, `CAP` — 이건 capstone `ircserv`가 다룬다
- WebSocket — 이 저장소에서 다루지 않는다
- game logic — `ticklab`/`arenaserv`의 영역이다
- persistence/metrics — 범위 밖

이 경계가 중요한 이유: `roomlab`에 `TOPIC`이나 `MODE`까지 넣으면, "core IRC"와 "advanced IRC"의 구분이 사라진다. 그러면 `ircserv` capstone이 할 일이 없어진다.

## 참고한 자료

| 자료 | 경로 | 왜 봤는가 | 무엇을 알게 되었는가 |
| --- | --- | --- | --- |
| Legacy Server | `legacy/src/Server.cpp` | connection lifetime과 cleanup 확인 | event loop와 disconnect 흐름을 그대로 살릴 가치가 있었다 |
| Legacy Executor | `legacy/src/Executor.cpp` | registration과 message delivery 확인 | core IRC command path만 남겨도 독립 lab이 된다 |
| JOIN/PART 구현 | `legacy/src/execute_join.cpp` | room lifecycle 확인 | server index와 node index를 함께 갱신해야 한다는 점이 중요했다 |
