# ircserv — 회고: capstone은 "기능의 끝"이 아니라 "구조 통합의 시작"이다

작성일: 2026-03-08

## 가장 만족스러운 것

이 capstone을 완성하고 나서 가장 만족스러운 점은, 코드를 읽는 사람이 **커리큘럼의 흐름을 따라갈 수 있다**는 것이다.

- event loop 코드를 보면 "이건 eventlab에서 다룬 것"이라는 것을 알 수 있다.
- parser 코드를 보면 "이건 msglab에서 다룬 것"이라는 것을 알 수 있다.
- registration/JOIN/PART/PRIVMSG를 보면 "이건 roomlab에서 다룬 것"이라는 것을 알 수 있다.
- TOPIC/MODE/KICK/INVITE를 보면 "이것이 capstone에서 추가된 것"이라는 것을 알 수 있다.

이 경계가 명확하다는 것은, 커리큘럼이 제대로 작동했다는 증거다. 각 lab이 하나의 관심사를 분리했기 때문에, capstone에서 합칠 때 "어디서부터 어디까지가 새로운 것인가"가 분명하다.

## 구현 품질에 대한 현재 판단

**pure TCP boundary가 깨끗하다.** WebSocket, game, Store, Metrics — legacy에 있던 모든 비-IRC 코드가 제거되었다. 소스를 열었을 때 IRC 프로토콜 처리 이외의 것이 보이지 않는다.

**CAP, MODE, INVITE, TOPIC, KICK이 실제 smoke로 확인된다.** 문서에만 "지원합니다"라고 쓴 것이 아니라, 자동화된 테스트가 11개 시나리오를 재현한다.

반면, **아쉬운 점도 분명하다.** numeric reply를 생성하는 `macros.hpp`의 `BUILD_*` 매크로들은 문자열 연결로 되어 있어 가독성이 낮고 타입 안전성이 없다. Executor도 monolithic dispatch — 하나의 `process()` 안에서 switch로 분기하는 구조다. 이건 legacy에서 가져온 것의 한계이고, 이 capstone에서 리팩토링하는 것은 범위 밖으로 판단했다.

**Linux 재검증이 빠져 있다.** event loop은 `#ifdef __APPLE__` / `#ifdef __linux__`로 kqueue와 epoll을 분기하는데, 이번 턴에서는 macOS에서만 검증했다. cross-platform 주장을 강하게 하려면 Linux CI가 필요하다.

## 다시 한다면 바꾸고 싶은 것

- **command별 transcript fixture**: 현재 smoke test는 하나의 함수에서 모든 시나리오를 순차적으로 실행한다. 각 command별로 독립적인 fixture를 두면, 실패 원인을 더 빠르게 분리할 수 있다.
- **MODE parsing의 분리**: `_execute_mode()`는 현재 하나의 큰 함수다. mode 문자 파싱, 대상 식별, 권한 체크를 별도 함수로 분리하면 읽기가 훨씬 나아진다.
- **numeric reply builder**: 매크로 대신 구조체 기반 builder를 사용하면 타입 안전성과 가독성이 동시에 좋아진다.

## 이 capstone을 어떻게 평가하는가

목적은 "pure TCP C++17 modern IRC 학습용 capstone"이다. 이 기준에서는 **성공했다**. 서버가 실행되고, 세 클라이언트가 동시에 접속해서 채널을 만들고, invite하고, topic을 설정하고, kick하고, ping/pong을 주고받는다.

하지만 "완전한 IRC 제품"이라는 기준에서는 **의도적으로 빠진 부분이 많다**. TLS, services, IRCv3 extension, 다중 서버 연동 — 이런 것들은 이 학습 트랙의 관심사가 아니다.

이 두 기준을 혼동하지 않는 것이 중요하다. capstone은 "기능을 최대한 많이 넣은 서버"가 아니라, "분리해서 학습한 개념을 다시 합쳐본 서버"다.
