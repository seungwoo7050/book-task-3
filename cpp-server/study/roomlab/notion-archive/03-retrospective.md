# roomlab — 회고: 10개 명령으로 state machine을 완성할 수 있는가

작성일: 2026-03-09

## 이 lab이 커리큘럼 안에서 하는 일

`roomlab`은 코드 크기로 보면 이 저장소에서 가장 큰 lab 중 하나지만, 기능 범위로 보면 의도적으로 좁다. PASS, NICK, USER, JOIN, PART, PRIVMSG, NOTICE, PING, PONG, QUIT — 이 10개의 명령만 처리한다.

이 좁음이 의미 있는 이유는 커리큘럼의 흐름 때문이다. `eventlab`에서 이벤트 루프를 분리했고, `msglab`에서 파서를 분리했다. 두 lab은 각각의 관심사를 고립시켜 학습하는 데 최적화되어 있었다. 하지만 실제 서버에서는 이벤트 루프와 파서 사이에 **상태 머신**이 있다. 소켓에서 데이터를 읽고, 파서가 메시지를 만들고, 그 메시지에 따라 서버 상태가 바뀌는 것 — 이 세 번째 층이 roomlab의 주제다.

10개의 명령만으로도 이 state machine은 충분히 복잡하다:

- **Registration state**: PASS → NICK → USER 순서가 맞아야 등록이 완료된다. 순서가 잘못되거나 비밀번호가 틀리면 거부된다.
- **Room membership**: JOIN은 채널을 생성하거나 기존 채널에 가입한다. PART는 나가고, 마지막 멤버가 나가면 채널이 삭제된다.
- **Cross-index consistency**: nickname은 서버 전역 `nickdb`에, 소켓은 `sockdb`에, 채널은 `chandb`에 인덱싱된다. 그리고 각 Connection은 자신이 속한 채널의 로컬 인덱스(`chandb`)를 갖는다. QUIT 시 이 모든 인덱스를 일관되게 정리해야 한다.

## 좋았던 것

**minimal command set이 오히려 학습 밀도를 높였다.** `TOPIC`이나 `MODE`가 없으니, 코드를 읽는 사람은 registration과 room lifecycle에만 집중할 수 있다. "이 command는 이 lab의 범위인가 아닌가"를 고민하지 않아도 된다.

그리고 **별도 lab으로 분리한 것이 capstone(`ircserv`) 진입 난이도를 낮추었다**. `ircserv`에서 TOPIC/MODE/KICK/INVITE를 추가할 때, registration과 room lifecycle은 이미 검증된 상태로 가져갈 수 있다. 두 층의 버그가 섞이지 않는다.

## 아쉬운 것

**실제 IRC 클라이언트와의 호환성을 주장하기에는 부족하다.** `irssi`나 `HexChat` 같은 클라이어트를 roomlab 서버에 연결하면, CAP negotiation 부재로 인해 바로 문제가 생긴다. 이건 roomlab의 목적상 허용 가능한 제한이지만, 문서에서 명시적으로 밝혀둘 필요가 있다.

또한 **numeric macro와 executor 구현이 거칠다**. `macros.hpp`의 BUILD_ERR_* 매크로들은 문자열 연결로 IRC numeric reply를 만드는데, 가독성이 좋지 않고 타입 안전성도 없다. 이건 legacy에서 가져온 것의 한계이고, 이 lab에서 리팩토링하는 것은 범위 밖이다.

## 최종 판단

이 단계를 건너뛰고 바로 `ircserv`로 가면, parser bug와 state bug가 한 번에 섞인다. eventlab과 msglab만으로는 "이벤트 루프 + 파서"까지는 검증했지만, "그 위의 state machine"은 검증하지 않은 상태다. roomlab은 이 빈 칸을 정확히 채운다. capstone 직전에 core state machine을 별도로 검증하는 단계로서 충분한 가치가 있다.
