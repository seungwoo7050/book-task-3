# msglab — 파서를 떼어놓으니 비로소 보이는 것들

작성일: 2026-03-08

## 왜 파서만 따로 보려고 했는가

레거시 프로젝트에서 IRC 메시지 파싱은 서버 런타임 내부에 묻혀 있었다. `Message` 클래스가 있었지만, WebSocket JSON envelope과 게임 커맨드 흔적이 같은 계층에 섞여 있어서 "순수 IRC message parser"를 따로 읽기 어려운 상태였다.

`eventlab`에서 이벤트 루프를 분리한 뒤, 자연스럽게 떠오른 질문이 있었다 — "소켓에서 읽어 온 raw bytes가 어떤 규칙으로 의미 있는 메시지로 바뀌는가?" 이 질문에 답하려면 네트워크 I/O를 잠시 잊고, IRC line 자체를 해석하는 규칙만 떼어서 볼 필요가 있었다.

그래서 `msglab`의 범위를 매우 좁게 잡았다. 다루는 질문은 다섯 가지뿐이다.

1. 한 줄의 IRC 입력은 어떤 단위로 끊기는가?
2. prefix(`:nick!user@host`)는 어떻게 해석되는가?
3. command는 어떻게 정규화되는가?
4. trailing parameter(`:` 뒤의 공백 포함 텍스트)는 어떻게 보존되는가?
5. nickname과 channel token은 어떻게 유효성을 검증하는가?

## 재구성한 문제 정의

1. C++17로 `Message`와 `Parser`를 작성한다.
2. parser는 stream에서 `\n`으로 끝나는 완전한 메시지만 꺼내고, partial line은 남겨 둔다.
3. `:<prefix> COMMAND params... :trailing` 형태를 처리한다.
4. command token은 대문자로 정규화한다.
5. channel과 nickname validator를 제공한다.
6. **서버 없이** 동작하는 단위 테스트로 검증한다.

마지막 항목이 핵심이다 — 이 lab에서는 서버를 띄우지 않는다. parser가 올바르게 동작하는지를 socket I/O 없이 직접 확인할 수 있어야 한다.

## 포함한 것과 제외한 것

포함:
- line splitting (`Parser::make_messages`)
- command mapping (`Message::label` enum)
- prefix/trailing parameter extraction
- nickname/channel validation
- arena 커맨드(INPUT, HELLO, REJOIN)의 토큰 validation helper

제외:
- socket I/O — `eventlab`이 담당한다
- registration state machine — `roomlab`이 담당한다
- numeric reply 송신 — 실행기 계층의 일이다
- WebSocket JSON envelope — 이 저장소에서 다루지 않는다

## 성공 기준

- `PASS`, `NICK`, `USER`, `JOIN`, `PRIVMSG`, `TOPIC`, `MODE`, `KICK`, `INVITE` 예제가 기대한 command label로 분류된다.
- prefix와 trailing parameter가 손실 없이 유지된다.
- partial line이 `make_messages` 호출 뒤에도 stream에 남아 있다.
- invalid nickname/channel이 적절히 거절된다.
- arena 커맨드의 토큰(정수, 방향, 이진 플래그)이 올바르게 검증된다.

## 참고한 자료

| 자료 | 경로 | 왜 봤는가 | 무엇을 알게 되었는가 |
| --- | --- | --- | --- |
| Legacy Message parser | `legacy/src/Message.cpp` | raw line → Message 변환 구조 확인 | prefix, command, trailing 처리 골격이 이미 존재 — 구조는 유지하되 non-IRC 흔적 제거 |
| Legacy Parser helpers | `legacy/src/Parser.cpp` | line split과 helper 함수 원형 확인 | frame split과 string helper는 재사용 가치가 있었다 |
| Parser interface | `legacy/src/inc/Parser.hpp` | 공개 API 범위 정하기 | 필요한 표면이 작아서 최소 범위로 유지 가능 |
| Numeric macros | `legacy/src/inc/macros.hpp` | parser가 대상으로 하는 command 집합 확인 | golden transcript에 포함할 항목을 고르는 기준이 되었다 |
