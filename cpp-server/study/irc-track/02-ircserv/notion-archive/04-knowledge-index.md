# ircserv — 지식 인덱스: capstone 통합에서 배운 네 가지

작성일: 2026-03-08

## 1. ISUPPORT (005 numeric)

서버가 registration 완료 시 `005` numeric으로 보내는 "서버 제약 광고"다. 완전한 협상 메커니즘은 아니지만, 클라이언트가 서버의 한계를 알 수 있게 해준다.

ircserv에서 광고하는 값들: `CHANTYPES=#`, `CHANLIMIT=#:10`, `NICKLEN=30`, `CHANNELLEN=32`, `KICKLEN=255`, `TOPICLEN=307` 등. 이 값들은 `Server` 클래스의 static 상수로 정의되어 있고, `Executor::_isupport()` 함수가 两 줄의 005 reply로 조합한다.

## 2. Capability Negotiation (CAP LS 302)

IRC 클라이언트는 연결 직후 `CAP LS 302`를 보내서 서버가 어떤 확장 기능을 지원하는지 물어볼 수 있다. 이 구현에서는 빈 capability list로 응답한다 — 즉, IRCv3 extension을 하나도 지원하지 않는다고 선언한다.

이것이 필요한 이유: `irssi` 같은 실제 IRC 클라이언트는 CAP이 없으면 연결을 거부하거나 비정상 동작할 수 있다. 최소한의 CAP 응답이라도 있어야 클라이언트 호환성이 확보된다.

## 3. Channel Privilege와 Stale State

KICK 버그에서 배운 핵심: **서버 전역 상태와 connection 로컬 상태를 항상 함께 갱신해야 한다.**

이 원칙은 roomlab의 "이중 인덱스 갱신" 지식과 동일하지만, ircserv에서는 KICK/MODE/INVITE가 추가되면서 더 많은 곳에서 적용된다:

- `KICK`: channel의 clientdb/privdb/invitedb를 정리하고, **target connection의 chandb도 정리해야 한다**.
- `MODE +o/-o`: channel의 privdb를 변경하고, 변경 결과를 채널 전체에 broadcast해야 한다.
- `INVITE`: channel의 invitedb에 target을 추가하고, **target에게 INVITE 이벤트를 보내야 한다**.

세 경우 모두, 한쪽만 갱신하면 이후 동작(재입장 판단, 권한 체크, cleanup)에서 불일치가 생긴다.

## 4. Test Stabilization과 Server Semantics는 구분해서 기록해야 한다

ircserv의 debg log에서 문제 2, 3은 서버 버그가 아니라 테스트 타이밍 문제였다. 이 구분이 중요한 이유: 서버 코드를 고친 것과 테스트를 안정화한 것은 성격이 다르다. 두 가지를 구분하지 않으면, 나중에 "이 커밋이 서버 동작을 바꿨나?"를 추적할 때 혼란이 생긴다.

기록 원칙:
- 서버 로직 수정 → 서버 버그로 분류, 코드 변경 내역 명시
- 테스트 안정화 → 테스트 변경으로 분류, `time.sleep()` 추가 같은 구체적 조치 명시
- 하위 lab 포팅 → 출처 lab과 원본 버그 번호를 참조

## 참고 자료

| 자료 | 경로 | 왜 봤는가 | 무엇을 알게 되었는가 |
| --- | --- | --- | --- |
| Legacy README | `legacy/README.md` | pure IRC 범위의 경계 확인 | game/web/store를 capstone에서 제외하는 기준 |
| Legacy Executor | `legacy/src/Executor.cpp` | advanced command 흐름 확인 | TOPIC/MODE/INVITE/KICK의 구현 근거 |
| Legacy Server loop | `legacy/src/Server.cpp` | runtime lifecycle 확인 | pure TCP 서버의 연결 수명주기 |
| ircserv smoke test | `study/ircserv/cpp/tests/test_irc_join.py` | 검증 범위 기록 | 11개 시나리오가 capstone의 최소 보장 범위 |

## 체크리스트

- KICK이 target connection 로컬 상태(chandb)까지 정리하는가?
- INVITE 후 JOIN 경로가 invite-only 채널에서 통과하는가?
- MODE +i 설정 후 비초대 사용자의 JOIN이 473으로 거절되는가?
- 하위 lab(msglab, roomlab)에서 수정한 parser/validator 버그가 ircserv에도 반영되었는가?
