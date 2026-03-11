# ircserv — 접근 방식: legacy 복원이 아니라 커리큘럼 통합

작성일: 2026-03-08

## 이 capstone의 정체성

이 capstone을 시작할 때 가장 먼저 해야 했던 것은, "이것이 무엇이냐"를 정의하는 것이었다. 두 가지 해석이 가능했다:

1. "legacy 서버의 pure IRC 부분을 복원하는 것"
2. "앞선 세 lab의 개념을 실제 서버로 통합하는 것"

첫 번째 해석을 따르면, legacy 코드를 최대한 가져와서 비-IRC 부분만 제거하면 된다. 빠르지만, 학습 트랙으로서의 의미가 약하다. 이미 존재하는 코드를 정리한 것에 불과하다.

두 번째 해석을 따르면, capstone의 구조가 "eventlab(event loop) + msglab(parser) + roomlab(state machine) + advanced IRC commands"로 읽혀야 한다. 이것이 더 어렵지만, 커리큘럼의 흐름이 살아난다.

두 번째를 택했다.

## 실제로 한 일: roomlab 코어 위에 advanced commands를 얹다

`ircserv`의 파일 구조는 `roomlab`과 동일하다. 같은 11개의 소스 파일, 같은 10개의 헤더. 차이점은 다음 네 가지다:

1. **Executor**에 `_execute_topic()`, `_execute_mode()`, `_execute_kick()`, `_execute_invite()` handler가 추가되었다.
2. **Channel**의 mode flag(`ibit`, `tbit`, `kbit`, `lbit`)가 **활성화**되었다. roomlab에서는 이 flag들이 코드에 있었지만 0 상태에서 변하지 않았다. ircserv에서는 `MODE` command가 이 flag들을 실제로 변경한다.
3. **CAP LS 302** 처리가 추가되었다. 클라이언트가 연결 시 capability를 물어보면 응답한다.
4. **005 ISUPPORT**가 registration 완료 시 전송된다. CHANTYPES, NICKLEN, CHANNELLEN 등의 서버 제약을 광고한다.

## 의도적으로 하지 않은 것

- **IRCv3 capability 전체 구현**: `CAP LS 302`에 빈 capability list로 응답하는 것이 이 capstone의 최소 범위다. `sasl`, `message-tags` 같은 확장은 넣지 않았다.
- **Services**: NickServ, ChanServ 같은 서비스 봇은 범위 밖이다.
- **TLS**: 암호화는 이 학습 트랙의 관심사가 아니다.
- **Feature maximalism**: capstone이라고 해서 기능을 최대한 많이 넣을 이유가 없다. 오히려 "앞선 lab의 통합"이라는 정체성을 유지하는 것이 학습 아카이브로서 더 가치 있다.

## 테스트 전략

smoke test 범위를 `roomlab`의 6개 시나리오에서 11개로 확장했다:

1. `CAP LS 302` 응답 확인
2. alice, bob, carol 세 클라이언트 registration + 005 ISUPPORT
3. alice JOIN #ops
4. bob JOIN #ops
5. alice `MODE #ops +i` — invite-only 설정 및 broadcast 확인
6. alice `INVITE carol #ops` — 초대 acknowledgment(341)과 carol에게 INVITE 이벤트
7. carol JOIN #ops — invite 후 가입 성공
8. alice `TOPIC #ops :control room` — topic broadcast 확인
9. alice `PRIVMSG #ops :hello capstone` — channel message broadcast
10. alice `KICK #ops bob :bye` — bob에게 KICK 이벤트 전달
11. bob `JOIN #ops` 재시도 → 473 ERR_INVITEONLYCHAN — invite-only 채널 재입장 거절
12. alice `PING capstone` → PONG 응답

테스트에서 세 클라이언트를 사용하는 이유: operator(alice), 일반 member(bob), invited guest(carol)이라는 세 가지 역할이 있어야 invite/kick 시나리오가 완전해진다.
