# eventlab evidence ledger

시간 정보가 공개돼 있지 않아서 ledger는 `Phase 1`부터 `Phase 4`까지의 복원형 chronology로 적었다. 다만 각 phase는 임의로 나눈 덩어리가 아니라, 실제 코드 의존 순서와 테스트 장면이 바뀌는 지점을 기준으로 묶었다. 처음엔 runtime 뼈대를 세우고, 그다음 연결 수명주기를 돌리고, 이어서 line protocol을 붙이고, 마지막에 keep-alive와 smoke verification으로 닫히는 흐름이다.

## Phase 1

이 phase는 "서버가 무엇을 처리할 것인가"보다 "그 처리를 어떤 인터페이스 뒤에 숨길 것인가"를 먼저 정한 시점으로 읽는 편이 자연스럽다. `EventManager`가 생기면서 커널 이벤트 API 차이가 서버 본문 밖으로 밀려난다.

- 순서: 1
- 시간 표지: Phase 1
- 당시 목표: listening socket과 readiness abstraction을 먼저 세운다.
- 변경 단위: `cpp/include/inc/EventManager.hpp`, `cpp/src/EventManager.cpp`, `cpp/src/Server.cpp`
- 처음 가설: accept/read/write를 한 함수에 다 넣기보다 `EventManager`가 커널 차이를 숨겨 주면 이후 서버가 단순해진다.
- 실제 조치: `EventManager::listen_event()`, `open_listenfd()`, `accept_node()`, `retrieve_events()`를 만들고 `Server::run()`에서 `SIGINT`와 listen socket을 등록한다.
- CLI: `make clean && make test`
- 검증 신호: 빌드 후 `python3 tests/test_eventlab.py`까지 도달한다.
- 핵심 코드 앵커: `EventManager::open_listenfd()`, `EventManager::retrieve_events()`, `Server::run()`
- 새로 배운 것: 이 lab의 핵심은 프로토콜이 아니라 "새 연결을 `newq`, 보낼 소켓을 `sendq`, 보낸 소켓을 `sentq`로 분리하는 런타임 계약"이다.
- 다음: 연결 객체를 받아 실제 읽기/쓰기와 종료 처리를 `Server::run_event_loop()`에 붙인다.

## Phase 2

런타임 표면이 잡히고 나면, 그다음 일은 결국 모든 연결을 한 자리에서 순환시키는 것이다. 여기서부터 `Client` 구조체와 accept/read/write 분기가 실제 의미를 갖기 시작한다.

- 순서: 2
- 시간 표지: Phase 2
- 당시 목표: 연결 수명주기를 한 곳에서 순환시킨다.
- 변경 단위: `cpp/src/Server.cpp`
- 처음 가설: event loop는 `listenfd`, client read, client write 세 갈래만 잘 유지하면 된다.
- 실제 조치: `Server::run_event_loop()`에서 accept -> `accept_connection()` -> read -> `process_input()` -> write -> `disconnect()` 흐름을 만든다.
- CLI: `make clean && make test`
- 검증 신호: 테스트가 두 클라이언트를 붙여도 `WELCOME`을 각각 받는다.
- 핵심 코드 앵커: `Server::run_event_loop()`, `Server::accept_connection()`, `Server::disconnect()`
- 새로 배운 것: 이 lab의 `Client`는 도메인 상태가 아니라 `recvbuf`, `sendbuf`, `timestamp`, `pinged`, `doomed`만 가진다.
- 다음: 소켓 바이트를 줄 단위 프로토콜로 자른다.

## Phase 3

이 시점부터 서버는 단순한 소켓 루프를 넘어서, 사람이 읽을 수 있는 line protocol을 다루기 시작한다. 그래도 parser를 붙이지는 않는다. 아직은 경계를 자르는 책임만 먼저 드러내는 단계다.

- 순서: 3
- 시간 표지: Phase 3
- 당시 목표: 네트워크 바이트를 사람이 읽는 line protocol로 바꾼다.
- 변경 단위: `cpp/src/Server.cpp`
- 처음 가설: 최소 서버라도 `read_packet()`과 `process_input()`을 분리해야 나중에 parser를 떼어낼 수 있다.
- 실제 조치: `read_packet()`이 `recvbuf`를 누적하고 `process_input()`이 `\n` 경계를 자르며 `handle_line()`이 `QUIT`, `PING`, 기본 `ECHO`를 나눈다.
- CLI: `make clean && make test`
- 검증 신호: smoke test가 `ECHO hello eventlab`, `PONG keepalive`, `BYE`를 순서대로 확인한다.
- 핵심 코드 앵커: `Server::read_packet()`, `Server::process_input()`, `Server::handle_line()`
- 새로 배운 것: parser가 없어도 "경계 자르기"는 이미 별도 책임이며, 다음 lab이 이 자리를 차지한다.
- 다음: idle keep-alive를 붙여 연결 정리를 런타임 문제로 고정한다.

## Phase 4

마지막 phase는 연결을 얼마나 잘 살리는가보다, 응답 없는 연결을 얼마나 오래 붙잡지 않는가에 가까운 장면이다. keep-alive와 smoke test가 여기서 한 번에 만난다.

- 순서: 4
- 시간 표지: Phase 4
- 당시 목표: 응답이 없는 연결을 살아 있는 세션처럼 보지 않게 만든다.
- 변경 단위: `cpp/src/Server.cpp`, `cpp/tests/test_eventlab.py`
- 처음 가설: keep-alive는 별도 command가 아니라 event loop 앞단에서 주기적으로 검사해야 한다.
- 실제 조치: `keep_alive()`가 `timeout` 이후 `PING :idle-check`를 보내고 `cutoff` 이후 끊으며, 테스트는 두 번째 클라이언트를 idle 상태로 남겨 실제 ping 도착을 확인한다.
- CLI: `make clean && make test`
- 검증 신호: `eventlab smoke passed.`
- 핵심 코드 앵커: `Server::keep_alive()`, `tests/test_eventlab.py`
- 새로 배운 것: smoke test 하나로도 accept/read/write/idle timeout/quit cleanup까지 모두 묶어 볼 수 있다.
- 다음: 메시지 구조화와 validation을 분리한 [`../02-msglab/README.md`](../02-msglab/README.md)로 넘어간다.

