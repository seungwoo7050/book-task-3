# eventlab — 부딪힌 문제들과 거기서 배운 것

작성일: 2026-03-08

## 문제 1. 처음 가져온 코드가 lab 범위를 넘어섰다

### 무슨 일이 있었는가

작업 초반에는 빠른 속도를 위해 기존 프로젝트 구조를 그대로 복사한 뒤 필요 없는 부분을 지우는 방식으로 시작했다. 그런데 복사해 온 코드에는 `Connection` 클래스의 흔적, IRC 전용 자료구조, 게임 관련 상수 등이 군데군데 남아 있었다.

처음에는 "나중에 다 지우면 되지"라고 생각했지만, 실제로 뼈대를 세우고 나니 "이건 event loop lab인가, 아니면 레거시 요약판인가?"라는 의문이 생겼다. lab의 목적과 코드의 내용이 정면으로 충돌하고 있었다.

### 어떻게 해결했는가

결국 복사 전략을 버리고, `EventManager`와 `utils`만 가져온 뒤 상위 `Server`를 새로 작성하기로 결정했다. IRC와 관련된 자료구조는 모두 제거하고, 프로토콜은 `WELCOME`, `ECHO`, `PING/PONG`, `BYE`의 네 가지만 남겼다.

### 이 경험에서 배운 것

"빨리 복사해서 나중에 깎자"는 접근은 학습용 프로젝트에서 특히 위험하다. 남은 잔해가 "이건 무시해도 되는 건가?"라는 불확실성을 만들기 때문이다. 결과적으로 이 수정 이후 lab의 경계가 훨씬 선명해졌고, README와 구현이 같은 이야기를 하게 되었다.

## 문제 2. idle keep-alive smoke test가 실패했다

### 무슨 일이 있었는가

smoke test에서 기대한 시점에 keep-alive `PING :idle-check`가 도달하지 않았다. 테스트 로그에는 "idle keep-alive ping did not arrive"라는 메시지만 남았다.

처음에는 keep-alive 로직 자체에 버그가 있다고 생각했다. 하지만 코드를 다시 읽어보니 로직은 맞았다. 문제는 **타이밍에 대한 잘못된 기대**였다.

### 왜 그런 일이 발생했는가

`keep_alive()` 함수는 event loop cycle 시작 시점에만 실행된다. 즉, 서버가 새 이벤트를 처리하기 위해 `epoll_wait`/`kevent`에서 깨어나야 idle 시간을 재평가할 수 있다. 그런데 idle 클라이언트만 연결된 상태에서는 아무런 이벤트가 발생하지 않으므로, 서버가 timeout까지 잠들어 있을 수 있다.

나는 "시간이 지나면 자동으로 정확히 그 순간 keep-alive가 나갈 것"이라고 기대했지만, 실제 구조는 "다음 cycle이 돌아올 때" 검사하는 방식이었다.

### 어떻게 해결했는가

서버 구조를 복잡하게 만드는 대신, 테스트 쪽에서 해결했다.

- 잠시 기다린 뒤 다른 연결에서 작은 `PING wakeup` 요청을 보내 서버를 한 번 더 깨운다.
- 그 다음 idle 클라이언트에서 keep-alive `PING :idle-check`를 수신하는지 확인한다.

이 선택의 이유: 이번 lab의 목표는 timer abstraction 자체가 아니라 event loop 책임을 보여주는 것이다. 서버를 억지로 더 복잡하게 만드는 것보다, **현재 구조의 의미를 드러내는 쪽**으로 테스트를 조정한 것이다.

### 여기서 얻은 교훈

이벤트 루프 기반 서버에서 "시간 기반 동작"은 event loop cycle granularity에 묶인다. 운영형 heartbeat가 필요하다면 timerfd(Linux)나 EVFILT_TIMER(macOS) 같은 별도 타이머를 커널 이벤트로 등록해야 한다. 이 차이를 체감한 것이 이 lab에서 가장 값진 디버깅 경험이었다.

## 문제 3. graceful shutdown을 signal 기반으로 유지할지 고민했다

### 무슨 일이 있었는가

가장 단순한 서버라면 `Ctrl+C`에 그냥 죽으면 된다. 하지만 레거시 코드에는 `SIGINT`를 event loop 종료 조건으로 쓰고, `SIGPIPE`/`SIGQUIT`/`SIGTSTP`를 무시하는 패턴이 있었다. 이걸 이 lab에서도 유지할 필요가 있을까?

### 어떻게 결정했는가

유지하기로 했다. 이유는 두 가지다.

1. signal 처리가 event loop와 어떻게 상호작용하는지 관찰할 기회가 된다.
2. 이후 `roomlab`과 `ircserv`로 넘어갈 때 진입점 패턴이 크게 바뀌지 않는다.

구체적으로는 `SIGPIPE`, `SIGQUIT`, `SIGTSTP`를 무시하고, `SIGINT`는 `EventManager`에 signal event로 등록해서 event loop 내부에서 `interrupt = true`로 전환하는 방식을 사용했다.

## 이 시점에서 아직 남아있는 약점

- timeout 정밀도는 낮다 (event loop cycle에 의존).
- write backpressure를 적극적으로 다루지 않는다 — `sendbuf`에 모아두고 write readiness가 오면 한꺼번에 flush하는 수준이다.
- IPv6와 고급 소켓 옵션은 다루지 않는다.

이 약점들은 이 lab의 범위 밖이라서 의도적으로 열어두었지만, 존재한다는 사실 자체는 기록해둘 가치가 있다.
