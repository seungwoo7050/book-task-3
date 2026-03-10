# msglab — 파서를 독립시키기까지의 선택들

작성일: 2026-03-08

## 처음 정한 원칙

이 lab은 반드시 **parser 자체만 검증 가능**해야 했다. 서버를 띄우지 않아도 command tokenization과 validation이 실패하는지 바로 확인할 수 있어야 한다. 이 원칙은 이후의 모든 결정을 지배했다.

이 원칙 때문에 세 가지를 먼저 결정했다:
- `Server` 의존성을 parser에서 완전히 떼어낸다.
- WebSocket/Protocol 흔적을 parser에서 제거한다.
- 테스트는 executable 하나로 끝낼 수 있게 만든다 — Python test runner도 필요 없다.

## 첫 번째 시도: 레거시 parser를 그대로 복사하기

가장 빠른 길은 레거시의 `Message.cpp`와 `Parser.cpp`를 복사한 뒤, 컴파일 에러가 나는 의존성만 stub으로 처리하는 것이었다.

그런데 이 접근은 시작하자마자 불쾌해졌다. `Parser.cpp`가 `Server.hpp`에 정의된 상수(channel maximum length 등)에 매달려 있었고, 더 나쁜 건 WebSocket/Protocol 흔적이 parser 계층에 남아 있다는 것이었다. 이 상태로는 "msglab은 parser 과제"라고 말하기 어려웠다.

## 두 번째 선택: parser가 자기 것은 스스로 정의한다

레거시에서 `Server`가 들고 있던 `channel_types`나 길이 제한 같은 상수를, `Parser` 클래스 자체로 옮기기로 했다. 이건 단순한 코드 이동이 아니라 **설계적 판단**이었다 — channel prefix와 nickname 길이 제한은 parser의 **문법 규칙**에 더 가깝기 때문이다.

이 결정이 가져온 효과:
- parser lab이 독립 과제처럼 보인다.
- 서버 없이도 파서를 빌드하고 테스트할 수 있다.
- 이후 `roomlab`에서 same parser를 가져다 쓸 때도 서버 종속 없이 재사용할 수 있다.

## 고려했지만 버린 선택: validator를 실행기에 남기기

일부 IRC 구현체에서는 nickname/channel validation을 Executor(실행기) 계층에 두기도 한다. 등록 시점에서 검사하는 게 자연스러워 보이기 때문이다.

이번에는 선택하지 않았다. 이유가 두 가지 있었다:
1. **invalid token은 가능한 빨리 드러나는 편이 학습에 유리하다.** 파싱 시점에서 걸러지면 "왜 거절됐는지"가 바로 보인다.
2. **`msglab`이 너무 빈약해지는 것을 피하고 싶었다.** validator까지 뺴면 parser lab에 남는 게 line split과 command mapping뿐이라, 독립 과제라고 부르기 민망해진다.

## 최종 구현 전략

- `Message`는 한 줄의 구문 해석만 담당한다 (prefix, command, params 추출).
- `Parser::make_messages`는 stream에서 `\n`으로 끝나는 완전한 line만 추출한다.
- `Parser::is_channel`, `Parser::is_nickname`는 최소 validator를 제공한다.
- `Parser::is_integer`, `Parser::is_facing`, `Parser::is_binary_flag`는 arena 커맨드용 helper다.
- command coverage는 실제 상위 lab(`roomlab`, `ircserv`)이 쓸 transcript 위주로 맞춘다.

## 테스트를 네 종류로 나눈 이유

테스트는 의도적으로 네 카테고리로 분리했다:

1. **prefix와 trailing parameter parsing** — 가장 기본적인 IRC line 해석
2. **validator 통과/실패 케이스** — 문법 계층의 거절 능력
3. **partial line 보존** — stream parser로서의 핵심 계약
4. **golden transcript command mapping** — 실제 사용될 IRC 명령들의 커버리지

이렇게 나눈 이유는 단순하다. parser에 버그가 생기면 **어느 층에서 잘못됐는지 바로 좁힐 수 있기 때문이다.** "command mapping이 실패했다"와 "partial line이 손실됐다"는 완전히 다른 종류의 문제이고, 테스트가 이걸 구분해줘야 한다.

## 의도적으로 하지 않은 것

- numeric reply builder 테스트 — parser lab의 영역이 아니다
- full RFC compliance matrix — 실용적 subset으로 충분했다
- socket read loop 통합 테스트 — 이건 `eventlab`이 이미 다뤘다
