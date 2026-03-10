# eventlab — 이 과제에서 남긴 지식

작성일: 2026-03-08

## 핵심 개념 정리

### readiness-based I/O

커널이 "지금 읽을 수 있다" 또는 "지금 쓸 수 있다"는 **준비 상태**를 알려주는 모델이다. 애플리케이션은 커널이 "준비됐다"고 말할 때만 실제 `recv` 또는 `send`를 수행한다. 이 모델 덕분에 하나의 스레드로 수백 개의 연결을 동시에 관리할 수 있다.

### non-blocking socket

시스템 호출이 데이터를 기다리며 멈추지 않고 즉시 반환되는 소켓이다. 이벤트 루프와 함께 사용하지 않으면 busy waiting이나 복잡한 오류 처리 코드가 필연적으로 생긴다. `eventlab`에서는 `EventManager`가 이 복잡성을 감춰주고, `Server`는 "읽을 준비가 되면 읽고, 쓸 준비가 되면 쓴다"는 단순한 패턴만 따른다.

### 애플리케이션 레벨 keep-alive

여기서 말하는 keep-alive는 TCP keepalive 소켓 옵션이 아니라, **서버가 직접 보내는 heartbeat 메시지**다. 서버가 `PING :idle-check`를 보내고, 클라이언트 반응이 없으면 연결을 끊는다. 이 lab에서 이 기능이 중요한 이유는, keep-alive가 event loop cycle의 granularity에 영향을 받는다는 점을 직접 보여주기 때문이다.

### send queue

응답을 즉시 다 보내지 못할 수 있으므로, `sendbuf`에 모아 뒀다가 write readiness가 왔을 때 flush하는 구조다. `eventlab`에서는 `queue_reply()`가 문자열을 쌓고, `sendq`에 fd를 넣어 EventManager에게 "이 소켓에 쓸 게 있다"고 알린다.

## 이 과제에서 체화한 설계 원칙

- **새 연결은 accept 직후 read 대상으로 등록되어야 한다.** 등록하지 않으면 커널이 그 소켓의 readiness를 알려줄 방법이 없다.
- **disconnect는 fd 정리와 내부 인덱스 정리를 함께 처리해야 한다.** `close(fd)`만 호출하고 `clients` map에서 지우지 않으면, 이미 닫힌 fd에 대해 event가 들어올 수 있다.
- **timeout은 event loop cycle granularity에 영향을 받는다.** "3초 후에 ping을 보낸다"고 해도, event loop이 5초 동안 잠들어 있으면 실제로는 5초 후에 보내진다. 이 차이를 이해하는 것이 이 lab의 핵심 학습 포인트 중 하나였다.

## 다시 볼 만한 로컬 참고 자료

| 자료 | 경로 | 왜 봤는가 | 무엇을 배웠는가 | 프로젝트에 어떤 영향을 줬는가 |
| --- | --- | --- | --- | --- |
| Legacy README | `legacy/README.md` | 레거시 프로젝트의 큰 그림 확인 | event loop가 실제 제품의 기반이었다 | 이를 독립 lab으로 떼는 결정에 근거가 되었다 |
| EventManager 구현체 | `legacy/src/EventManager.cpp` | kqueue/epoll 구현 세부 확인 | 추상화 표면은 이미 충분히 정리되어 있었다 | 재작성 대신 재사용을 선택 |
| Legacy 서버 루프 | `legacy/src/Server.cpp` | accept/read/write/keep-alive 순서 파악 | event cycle의 뼈대는 그대로 살릴 가치가 있었다 | 새 `Server.cpp`의 골격 결정에 활용 |
| eventlab smoke test | `study/eventlab/cpp/tests/test_eventlab.py` | 실제 검증 포인트를 문서와 대조 | keep-alive는 wake-up 조건을 고려해야 했다 | 디버그 로그와 회고의 핵심 사례가 되었다 |

## 빠른 자가 점검 리스트

- [ ] event loop과 protocol logic이 한 함수에 섞여 있지 않은가?
- [ ] timeout이 strict timer처럼 보이도록 과장하지 않았는가?
- [ ] disconnect 시 fd와 내부 컨테이너를 함께 정리하는가?
- [ ] 새 연결을 accept한 뒤 read event 등록을 빠뜨리지 않았는가?
