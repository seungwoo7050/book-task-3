# eventlab — 끝나고 돌아보니

작성일: 2026-03-08

## 이 lab이 실제로 보여준 것

가장 큰 성과는 "이벤트 루프를 따로 볼 수 있게 되었다"는 점이다.

레거시 서버에서는 event loop가 IRC 상태 머신과 한 몸처럼 보였다. 처음 읽는 사람은 "이건 소켓 코드인가, 프로토콜 코드인가?"를 구분하기 어려웠다. 지금의 `eventlab`은 다음 네 가지 질문에 코드가 바로 답한다.

1. **새 연결은 어디서 받아들이는가?** — `accept_connection()`에서 `WELCOME`을 보내며 시작한다.
2. **읽기/쓰기 readiness는 어떻게 분기되는가?** — `run_event_loop()`의 event type 분기에서 한눈에 보인다.
3. **disconnect는 어떤 시점에 정리되는가?** — `disconnect()`에서 fd를 닫고, client map과 send queue에서 제거한다.
4. **keep-alive는 어디서 검사되는가?** — `keep_alive()`가 event loop cycle 시작 시점에 idle 시간을 확인한다.

이 네 질문이 명확해진 것만으로도 lab 분리의 가치가 충분했다.

## 좀 더 솔직한 평가

긍정적인 면:
- event loop의 책임 경계가 코드에 드러난다.
- 두 클라이언트의 동시 접속, echo, ping/pong, keep-alive, quit — 전부 smoke test로 재현된다.
- IRC 잔해가 하나도 없어서, 읽는 사람이 프로토콜 복잡도에 방해받지 않는다.

아직 약한 면:
- 타이머가 "독립된 개체"가 아니라 "다음 cycle에서 검사되는 조건"에 가깝다. 학습용으로는 괜찮지만, "정확한 heartbeat scheduler"로 이해하면 오해가 생길 수 있다.
- 프로토콜 표면이 너무 작아서, line buffering이나 partial write/backpressure의 복잡성이 충분히 드러나지 않는다.
- 프로토콜이 간단하다 보니 "이게 정말 서버인가?"라는 질문이 나올 수 있다 — 하지만 이건 lab의 설계 의도에 부합한다.

## 다시 한다면

- **timer event를 별도 추상화로 넣어 보고 싶다.** timerfd나 EVFILT_TIMER를 EventManager에 추가하면, "event loop과 timer의 관계"라는 질문에도 답할 수 있다.
- **write side의 partial flush 시나리오**를 테스트에 더 넣고 싶다. 현재는 `sendbuf`가 한 번에 다 나가는 행복한 경로만 검증한다.
- **event order transcript를 파일로 저장**하고 싶다. 현재 smoke test는 성공/실패만 알려주지, 실제 이벤트가 어떤 순서로 일어났는지는 기록하지 않는다.

## 다음 과제와의 연결

`eventlab` 다음에는 `msglab`이 온다. 이유는 단순하다:

이벤트 루프의 I/O cycle은 이제 분리해서 이해했다. 다음에는 socket에서 읽어 온 raw bytes가 **어떤 문법 규칙으로 의미 있는 메시지가 되는지**를 따로 보면 된다. 즉, networking complexity를 늘리는 것이 아니라 **parsing complexity를 따로 학습**하는 것이다.

이 순서가 자연스러운 이유는, parser를 먼저 고립시키지 않으면 `roomlab`에서 "이 에러가 파싱 문제인가 상태 전이 문제인가?"를 분리하기 어려워지기 때문이다.
