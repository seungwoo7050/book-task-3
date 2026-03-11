# eventlab — 어떤 길을 골랐고, 왜 다른 길은 버렸는가

작성일: 2026-03-08

## 첫 번째 충동: "그냥 복사해서 깎자"

레거시 프로젝트에는 이미 완성된 `Server.cpp`가 있었다. accept, read, write, keep-alive, disconnect까지 전부 한 파일 안에 들어 있었으니, "거기서 IRC 부분만 지우면 되지 않을까?"라는 생각이 자연스럽게 떠올랐다.

실제로 이 접근(접근 A)을 잠깐 시도해 봤다. 하지만 곧 포기했다. 이유는 세 가지였다.

- `Server`가 원래 IRC 명령 파서와 executor를 전제로 설계되어 있어서, 단순히 코드를 지우면 빈 구멍이 어색하게 남았다.
- 학습자가 event loop를 읽다가 곧바로 IRC 상태 머신의 잔해를 만나게 되어, "이건 왜 있는 거지?"라는 혼란이 생겼다.
- lab의 목적이 "동작하는 최소 event loop"에서 "레거시 축소판"으로 미끄러질 위험이 있었다.

## 두 번째 생각: "EventManager만 살리고 위는 새로 짜자"

이 접근(접근 B)이 최종 선택이 되었다. 핵심 이유는 명확했다 — **학습 대상과 비학습 대상의 경계를 코드 레벨에서 물리적으로 나눌 수 있다**는 점이었다.

- `EventManager`는 kqueue/epoll 추상화라는 "이미 검증된 인프라"다. 이걸 다시 짤 필요는 없다.
- 그 위의 `Server`는 "이 lab만의 고유한 질문"에 답하는 코드여야 한다. echo, ping/pong, keep-alive, quit — 이게 전부다.
- 테스트도 작은 텍스트 프로토콜 위에서 돌릴 수 있어서, socket 연결 → 메시지 송수신 → 결과 확인이라는 직관적인 흐름이 가능했다.

## 고려했지만 버린 세 번째 길

서버를 아예 만들지 않고 `EventManager` 자체의 단위 테스트만 작성하는 접근(접근 C)도 떠올렸다. 구현량으로만 보면 가장 가볍다. 하지만 이 길은 금방 한계가 보였다.

- 커널 이벤트 API는 실제 socket과 함께 써야 동작이 눈에 보인다. fake fd로 테스트하면 "그래서 이게 실제로 어떻게 쓰이는데?"라는 질문에 답하지 못한다.
- accept → read → write → disconnect라는 전체 수명 주기를 관찰할 수 없다.
- "독립 과제처럼 보이는 lab"이라는 설계 목표에도 맞지 않았다.

## 그래서 만들어진 최종 구조

결정을 내린 뒤 구조를 이렇게 잡았다.

- **`EventManager`**: `legacy/` 구현을 그대로 재사용한다. 손대지 않는다.
- **`Server`**: `eventlab` 전용으로 새로 작성한다. IRC는 한 줄도 없다.
- **프로토콜**: `WELCOME`, `ECHO`, `PING/PONG`, `BYE` — 이 네 가지가 전부다.
- **keep-alive**: timeout을 smoke test용으로 짧게 둔다 (idle 2초, cutoff 5초).

이 결정의 가장 중요한 효과는, event loop가 책임지는 영역이 코드에서 눈에 보이게 되었다는 것이다. accept는 어디서 일어나고, read readiness는 어디서 분기되고, write queue는 어디서 flush되고, disconnect는 어디서 정리되는지 — 이 네 질문이 코드 안에서 직접 답을 가리킨다.

## 의식적으로 넣지 않은 것들

- IRC command parsing — `msglab`이 다룬다.
- channel state — `roomlab`이 다룬다.
- WebSocket framing — 이 저장소에서 아예 다루지 않기로 했다.
- 복잡한 timer abstraction — 이 lab의 목표가 아니다.

이것들은 전부 흥미로운 주제지만, 넣는 순간 event loop 자체가 흐려진다. lab의 가치는 **빠져 있는 것**에서도 나온다.

## 테스트를 어떻게 설계했는가

단위 테스트보다 **socket smoke test**를 우선했다. 이유는 이 lab의 핵심이 parser correctness가 아니라 실제 event cycle이기 때문이다.

smoke test는 다음 순서를 따른다.

1. 서버를 실행한다.
2. 두 클라이언트가 접속한다.
3. 양쪽 모두 `WELCOME`을 수신하는지 확인한다.
4. 한쪽에서 메시지를 보내 `ECHO`가 돌아오는지 확인한다.
5. explicit `PING`/`PONG` 경로를 확인한다.
6. idle keep-alive `PING`이 도달하는지 확인한다.
7. `QUIT` → `BYE` 종료 경로를 확인한다.

이 순서는 event loop의 전체 수명 주기를 한 번 통과하도록 설계된 것이다.

## 남겨 둔 불확실성

- strict timer semantics가 필요하면 현재 구조는 부족하다 — "다음 event loop cycle이 돌아올 때 검사"하는 방식이기 때문이다.
- 진짜 운영용 heartbeat라면 별도 timer event(timerfd, EVFILT_TIMER)가 더 적절할 가능성이 높다.
- 이 한계는 디버그 과정에서 실제로 부딪혔고, 02-debug-log에서 자세히 다룬다.
