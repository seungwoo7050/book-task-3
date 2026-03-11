# arenaserv — 지식 인덱스: game server 통합에서 배운 세 가지

작성일: 2026-03-09

## 1. Rule engine을 먼저 검증하고 transport를 나중에 붙여라

이 교훈이 이 저장소 전체를 관통하는 원칙이기도 하다. eventlab → msglab → roomlab → ticklab 순서로 각 계층을 분리해서 검증한 뒤, ircserv/arenaserv에서 합치는 구조다.

arenaserv에서 이 원칙이 가장 극적으로 드러났다. 네트워크 통합 과정에서 세 가지 버그(이벤트 flush 타이밍, fd 매핑 정리, overflow 테스트 부재)가 나왔는데, 세 가지 모두 시뮬레이션 로직과는 무관했다. ticklab에서 MatchEngine을 이미 검증했기 때문에, 디버깅 범위를 "Server와 MatchEngine 사이의 접착 코드"로 즉시 좁힐 수 있었다.

만약 ticklab 없이 바로 arenaserv를 만들었다면, 같은 버그를 디버깅할 때 "MatchEngine의 로직이 잘못된 것인가, 네트워크 코드가 잘못된 것인가"를 따로 구분해야 했을 것이다.

## 2. Reconnect에서는 token ownership과 socket ownership을 분리해야 한다

reconnect가 가능한 시스템에서는 두 가지 소유권이 있다:

- **Token ownership**: 플레이어의 세션을 식별하는 토큰. disconnect 후에도 grace window 동안 유지된다.
- **Socket ownership**: 실제 TCP 연결을 나타내는 fd. disconnect 시 즉시 닫힌다.

이 두 가지를 분리하는 것이 핵심이다:

- `disconnect()` 시: 소켓은 닫지만 token은 유지한다. `token_to_fd`에서 fd 매핑만 제거한다.
- `REJOIN` 시: 새 소켓이 기존 token에 연결된다. `token_to_fd`에 새 fd를 등록한다.

이렇게 하면 MatchEngine은 token으로만 플레이어를 식별하고, Server는 token↔fd 매핑만 관리한다. 두 계층이 깔끔하게 분리된다.

arenaserv의 debug log 2번(fd 매핑 정리 버그)이 정확히 이 분리가 불완전했기 때문에 발생한 것이다.

## 3. Room event를 즉시 flush하지 않으면, state mutation이 일어났는데도 클라이언트는 모른다

이건 headless engine(ticklab)에서는 문제가 되지 않았다. 테스트 코드가 `drain_events()`를 원할 때 호출하면 되니까. 하지만 네트워크 서버에서는 상황이 다르다.

`QUEUE`를 처리하면 MatchEngine이 `ROOM arena-1 lobby` 이벤트를 생성한다. 하지만 이 이벤트가 MatchEngine 내부 큐에만 있고 소켓에 쓰이지 않으면, 클라이언트는 100ms(다음 tick)까지 기다려야 응답을 받는다. 이건 "서버는 상태가 바뀌었는데 클라이언트는 모르는" 상태다.

해결: state mutation이 일어나는 모든 지점에서 `dispatch_engine_events()`를 호출한다. 이렇게 하면 이벤트가 즉시 클라이언트의 send buffer에 들어간다.

이 패턴은 "ticker와 event-driven의 혼합"이라는 arenaserv의 본질과 관련이 있다. tick은 일정 간격으로 시뮬레이션을 전진시키지만, 클라이언트 명령에 대한 응답은 즉시 보내야 한다. 두 가지 타이밍이 공존하는 것이다.

## 참고 자료

| 자료 | 경로 | 왜 봤는가 | 무엇을 알게 되었는가 |
| --- | --- | --- | --- |
| arenaserv smoke test | `study/arenaserv/cpp/tests/test_arenaserv.py` | 시연 범위 기록 | duel, party lobby, reconnect, draw timeout의 4개 시나리오가 최소 보장 범위 |
| ticklab MatchEngine | `study/ticklab/cpp/src/MatchEngine.cpp` | simulation core의 출처 기록 | copy 방식으로 가져왔으며, 시뮬레이션 규칙은 ticklab에서 검증 완료 |
| EventManager impl | `legacy/src/EventManager.cpp` | event loop runtime 출처 기록 | short timeout polling으로 tick scheduler를 single-threaded loop에서 구현 |
