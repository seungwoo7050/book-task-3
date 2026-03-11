# msglab — 파서를 떼어놓은 뒤 돌아보기

작성일: 2026-03-08

## 이 lab에서 가장 가치 있었던 것

이 lab의 가장 큰 성과는 **"파싱은 상태 머신과 다르다"는 점을 구조로 보여준 것**이다.

레거시 코드를 처음 읽는 사람은 다음 네 가지를 한꺼번에 따라가야 했다:
- socket read cycle
- message frame split
- command dispatch
- registration/channel state

이제는 parser만 떼어 보면서, 문법 계층("이 입력은 어떤 command이고, parameter는 무엇인가")과 상태 전이 계층("이 command를 받았을 때 서버 상태가 어떻게 바뀌는가")을 분리해서 이해할 수 있다.

이 분리가 왜 중요한가? `roomlab`에서 "JOIN이 왜 실패하지?"라는 문제가 생겼을 때, 원인이 파싱인지 상태 전이인지를 바로 구분할 수 있기 때문이다. `msglab`이 없으면 이 구분이 어렵다.

## 솔직한 품질 평가

**잘된 점:**
- 독립 빌드와 테스트가 가능하다. `make clean && make && make test` 한 줄이면 된다.
- prefix/trailing/partial line이라는 parser의 핵심 포인트를 실제 테스트가 커버한다.
- 레거시에 있던 non-IRC 흔적(WebSocket, game command 필드)을 완전히 제거했다.
- arena 커맨드의 토큰 validation helper(`is_integer`, `is_facing`, `is_binary_flag`)까지 포함해서, `ticklab`/`arenaserv`와의 연결고리가 생겼다.

**아쉬운 점:**
- numeric reply builder 자체는 이 lab의 테스트 범위에 없다.
- validator는 "실용적 subset"이라서, 이걸 RFC 완전 참조용으로 쓰기에는 부족하다.
- malformed line에 대한 세밀한 분류 테스트가 빠져 있다.

## 다시 한다면

- **malformed line에 대한 더 세밀한 분류 테스트**를 추가하고 싶다 — 예를 들어 command만 있고 아무 parameter도 없는 라인, trailing이 비어있는 경우(`PRIVMSG #ch :`), prefix만 있고 command가 없는 경우 등.
- **최대 길이 초과 토큰**에 대한 실패 기준을 명문화하고 싶다 — 현재는 길이 초과를 조용히 허용하는 부분이 있다.
- **case mapping 정책**을 더 명확히 문서화하고 싶다 — 현재는 command를 대문자로 정규화하지만, nickname은 case-preserving이다.

## 다음 과제와의 연결

`msglab` 다음은 `roomlab`이다. parser의 결과가 실제 registration/channel state에 어떻게 연결되는지를 보는 과제다.

이 순서가 자연스러운 이유: parser를 먼저 고립시키지 않으면, `roomlab`에서 state machine 문제를 디버그할 때 **원인이 파싱인지 상태 전이인지** 분리하기 어려워진다. `msglab`이 parser의 정확성을 보장해주기 때문에, `roomlab`에서는 "parser는 맞다"는 전제 위에서 state logic에 집중할 수 있다.
