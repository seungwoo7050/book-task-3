# eventlab — 이벤트 루프를 따로 볼 수 있게 만들기까지

작성일: 2026-03-08

## 시작점: "이 서버는 왜 이렇게 읽기 어려운가"

레거시 프로젝트(`legacy/`)를 처음 열었을 때, 가장 먼저 눈에 들어온 건 `EventManager`였다. kqueue(macOS)와 epoll(Linux)을 하나의 인터페이스로 감싸는 이 클래스는 서버의 심장 같은 존재였다. 그런데 실제 서버 코드를 따라 읽어 보면, 이 심장이 IRC 명령 실행기, 채널 상태 머신, WebSocket 프레임 처리, 심지어 게임 로직까지 전부 한 몸에 달고 뛰고 있었다.

그래서 이런 의문이 생겼다 — "이벤트 루프 자체는 얼마나 단순한가? 프로토콜을 전부 벗겨내면 뼈대만으로도 학습할 가치가 있을까?"

이 질문에 답하려고 `eventlab`을 만들었다.

## 문제를 이렇게 좁혔다

IRC 서버를 만드는 것이 아니라, **이벤트 루프의 동작을 직접 관찰할 수 있는 최소한의 TCP 서버**를 만드는 것으로 범위를 잡았다. 구체적으로 재구성한 과제는 이렇다.

1. C++17로 단일 프로세스 TCP 서버를 작성한다.
2. 서버는 non-blocking socket과 `EventManager`를 사용한다.
3. 텍스트 기반 line protocol을 쓴다.
4. 일반 입력은 `ECHO <line>`으로 되돌린다.
5. `PING <token>` 입력은 `PONG <token>`으로 응답한다.
6. `QUIT` 입력은 `BYE`를 보내고 연결을 종료한다.
7. 일정 시간 유휴 상태인 연결에는 서버가 `PING :idle-check`를 보내고, 반응이 없으면 끊는다.

결정적으로, 이 문제 정의는 RFC 프로토콜 구현이 아니라 **event loop 관찰을 위한 최소 표면**을 제공하는 데 목적이 있다.

## 포함한 것과 의도적으로 제외한 것

포함:
- socket open/bind/listen/accept/read/write
- 커널 이벤트 등록과 처리 (kqueue/epoll)
- keep-alive와 disconnect 정리
- signal 기반 graceful shutdown (`SIGINT`)

제외:
- IRC parser — 이건 다음 과제 `msglab`이 맡는다
- channel state, user registration — `roomlab`의 영역이다
- TLS — 학습 범위 밖
- timerfd/EVFILT_TIMER — 정밀 타이머는 이 과제의 목표가 아니다

이 경계를 정하는 데 시간이 꽤 걸렸다. 처음에는 "조금만 더 넣으면 좋겠다"는 유혹이 있었지만, 넣는 순간 event loop 관찰이라는 핵심 목표가 흐려진다는 걸 깨달았다.

## 내가 정한 성공 기준

- `make clean && make && make test`가 현재 작업 머신(macOS)에서 통과한다.
- 둘 이상의 클라이언트가 동시에 접속해 `WELCOME`을 받는다.
- 한 클라이언트의 입력이 echo 경로를 통과한다.
- `PING`/`PONG` 경로가 분리되어 동작한다.
- idle connection에 keep-alive ping이 실제로 도달한다.

## 시작하기 전에 알아야 하는 것

이 문서와 프로젝트를 이해하려면 다음 개념이 필요하다.

- **blocking vs non-blocking socket**: 시스템 호출이 데이터를 기다리며 멈추느냐, 즉시 반환하느냐의 차이
- **readiness-based I/O**: 커널이 "지금 읽을 수 있다" 또는 "지금 쓸 수 있다"를 알려주는 모델
- `accept`, `recv`, `send`, `close`의 기본 동작
- signal이 event loop 종료 조건으로 쓰일 때의 패턴

## 남겨둔 전제와 불확실성

- macOS에서 검증했다. `EventManager`는 Linux(epoll)도 지원하지만, 이번 과제에서 Linux 재검증은 하지 않았다.
- keep-alive 타이밍은 strict timer precision을 목표로 하지 않는다. event loop cycle 경계의 영향을 받는 구조이며, 이 점은 디버그 과정에서 중요하게 부각되었다.

## 어떤 자료를 보고 결정했는가

| 자료 | 경로 | 왜 봤는가 | 무엇을 알게 되었는가 |
| --- | --- | --- | --- |
| Legacy README | `legacy/README.md` | 전체 저장소의 원래 목적 확인 | event loop가 레거시 제품의 핵심 기반이라는 점을 재확인 — 별도 lab으로 떼는 결정의 근거가 되었다 |
| EventManager 구현체 | `legacy/src/EventManager.cpp` | kqueue/epoll 추상화의 실제 코드 확인 | cross-platform 이벤트 추상화가 이미 충분히 정리되어 있어 재사용 가능했다 |
| EventManager 헤더 | `legacy/src/inc/EventManager.hpp` | 공개 API 표면 확인 | `listen_event`, `accept_node`, `retrieve_events` 세 함수면 lab에 충분했다 |
| Legacy 서버 루프 | `legacy/src/Server.cpp` | accept/read/write/disconnect 흐름 파악 | keep-alive와 send queue 관리가 이미 정리되어 있었다 — full IRC server를 복사하지 않고 핵심 event cycle만 남기기로 했다 |
| Legacy utils | `legacy/src/utils.cpp` | socket read/write helper 확인 | `full_recvn`/`full_sendn` helper는 lab에서도 그대로 재사용 가능했다 |
