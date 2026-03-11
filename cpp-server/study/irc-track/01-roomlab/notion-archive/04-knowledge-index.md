# roomlab — 지식 인덱스: 상태 머신이 가르쳐준 세 가지

작성일: 2026-03-09

## 1. Registration은 단순한 소켓 연결이 아니라 프로토콜 상태다

TCP 소켓이 열렸다고 해서 사용자가 "등록된" 것이 아니다. IRC에서 등록은 PASS → NICK → USER 세 명령이 올바른 순서로 완료되어야 성립하는 **프로토콜 레벨 상태 전이**다.

이것이 코드에 어떻게 드러나는가: `Connection` 클래스에는 `is_authed`(PASS 완료)와 `is_registered`(USER 완료) 두 개의 boolean flag가 있다. `Executor`의 각 command handler는 이 flag를 확인하고, 등록 전인 connection에 대해서는 `ERR_NOTREGISTERED`를 반환한다.

이 개념은 `ircserv`에서 CAP negotiation이 추가될 때도 동일하게 적용된다. registration state machine의 상태가 하나 더 늘어날 뿐, 구조는 같다.

## 2. Room membership은 서버 전역 인덱스와 connection 로컬 인덱스를 함께 갱신해야 한다

채널에 가입한다는 것은 두 곳에 기록된다:
- **서버 측**: `Server::chandb` (채널 이름 → Channel 객체)와 `Channel::clientdb` (소켓 fd → Connection)
- **클라이언트 측**: `Connection::chandb` (채널 이름 → Channel)

JOIN 시에는 양쪽 모두에 추가하고, PART 시에는 양쪽 모두에서 제거해야 한다. 그리고 QUIT나 disconnect 시에는 해당 connection이 속한 **모든 채널**에서 이 정리를 수행해야 한다. 한쪽만 정리하면 dangling pointer나 ghost member가 생긴다.

이 이중 인덱스 구조는 `arenaserv`에서도 동일하게 나타난다. room 기반 시스템이면 어디서든 만나는 패턴이다.

## 3. QUIT broadcast와 disconnect cleanup은 타이밍이 다르다

- `QUIT :gone away` → 같은 채널의 다른 멤버에게 `:alice QUIT :gone away`를 **먼저 보내고**, 그 다음에 자원을 정리한다.
- EOF disconnect → broadcast 없이 **바로 자원을 정리**한다.

이 차이가 중요한 이유: broadcast는 send buffer에 데이터를 쓰는 것이고, 자원 정리는 소켓을 닫고 인덱스를 제거하는 것이다. 순서가 뒤바뀌면, 이미 닫힌 소켓에 쓰려고 시도하게 된다. `to_doom()` 패턴은 이 순서를 보장한다 — connection을 doomed로 표시만 하고, 실제 정리는 send buffer가 비워진 뒤에 수행한다.

## 참고 자료

| 자료 | 경로 | 왜 봤는가 | 무엇을 알게 되었는가 |
| --- | --- | --- | --- |
| Legacy Executor | `legacy/src/Executor.cpp` | registration과 message path 확인 | core IRC command path는 별도 lab으로 분리해도 충분히 의미 있다 |
| JOIN/PART logic | `legacy/src/execute_join.cpp` | room lifecycle 확인 | create/join/part/cleanup 순서가 중요하고, server-Channel-Connection 삼중 인덱스 갱신이 핵심이다 |
| Roomlab smoke test | `study/roomlab/cpp/tests/test_roomlab.py` | 검증 범위 기록 | 6개 시나리오(registration, duplicate nick, JOIN/PART, broadcast, QUIT cleanup, not-on-channel)가 최소 검증 범위다 |
