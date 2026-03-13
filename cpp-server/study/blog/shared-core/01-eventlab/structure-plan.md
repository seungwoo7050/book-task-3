# eventlab structure plan

이 시리즈의 독자는 "작은 서버 하나를 설명하는 글"보다 "뒤의 프로젝트들이 재사용할 최소 runtime을 먼저 이해하고 싶은 사람"에 가깝다. 그래서 글도 기능 나열이 아니라, 왜 이 지점에서 책임을 멈췄는가가 드러나도록 설계한다.

## 10-runtime-surface-and-event-loop.md

첫 글은 `problem/README.md`가 요구하는 범위를 출발점으로 삼는다. 독자가 처음 붙잡아야 할 것은 `EventManager`와 `Server::run_event_loop()`가 만드는 accept/read/write 순서이며, 이 뼈대가 뒤의 parser나 state transition보다 먼저 나온다는 점이다. 코드는 `EventManager.hpp`, `EventManager::open_listenfd()`, `EventManager::retrieve_events()`, `Server::run()`을 중심으로 앵커를 잡는다.

## 20-line-protocol-and-keepalive.md

둘째 글은 바이트 스트림이 line protocol로 바뀌는 순간을 따라간다. `read_packet()`, `process_input()`, `handle_line()`, `keep_alive()`를 중심에 두고, `PING`/`PONG`, `ECHO`, `QUIT`, idle timeout이 한 runtime 위에 자연스럽게 얹히는 흐름을 보여 준다. 여기서는 다음 lab이 가져갈 parser 자리를 미리 암시해 두는 것이 중요하다.

## 30-smoke-verification-and-boundaries.md

마지막 글은 `tests/test_eventlab.py`를 단순 테스트 소개가 아니라 proof 장면으로 읽게 만든다. `make clean && make test`와 `eventlab smoke passed.`를 닫는 신호로 두고, accept/read/write/keep-alive/quit cleanup은 증명됐지만 parser와 도메인 상태 전이는 아직 일부러 남겨 뒀다는 점까지 분명히 적는다.

