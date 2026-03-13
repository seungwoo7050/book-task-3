# eventlab 1. 런타임 표면과 event loop부터 고정하기

`eventlab`의 문제 정의는 애초에 좁다. [`problem/README.md`](../../../shared-core/01-eventlab/problem/README.md)가 요구하는 것은 "도메인 규칙 없이 연결 수명주기만 관찰할 수 있는 최소 non-blocking TCP 서버"다. 그래서 이 lab의 첫 단계는 명령어를 늘리는 일이 아니라, accept/read/write를 어떤 순서와 인터페이스로 묶을지 먼저 정하는 일이 된다.

이 역할을 맡는 것이 [`cpp/include/inc/EventManager.hpp`](../../../shared-core/01-eventlab/cpp/include/inc/EventManager.hpp)다. 공개 메서드는 많지 않다. `listen_event()`, `open_listenfd()`, `accept_node()`, `retrieve_events()` 네 개가 전부인데, 바로 이 네 함수 덕분에 서버 본문은 epoll이든 kqueue든 직접 신경 쓰지 않아도 된다.

```cpp
int EventManager::retrieve_events(std::deque<int> &newq,
    std::set<int> &sendq,
    std::deque<int> &sentq,
    std::vector<Event> &events);
```

이 시그니처를 보면 서버가 어떤 상태를 kernel event 계층에 넘기는지가 한 번에 드러난다. 새로 accept한 소켓은 `newq`, 지금 보낼 소켓은 `sendq`, 방금 보낸 소켓은 `sentq`로 나뉜다. 런타임 계약이 함수 이름보다 데이터 구조 모양으로 먼저 보이는 셈이다.

[`cpp/src/Server.cpp`](../../../shared-core/01-eventlab/cpp/src/Server.cpp)는 이 계약을 그대로 따른다. 생성자는 포트를 검증하고 `EventManager::open_listenfd()`로 listening socket만 연다. 그리고 `run()`은 `SIGINT`와 listen socket만 등록한 채, 인터럽트가 들어오기 전까지 event loop를 반복한다.

```cpp
void Server::run()
{
    if (this->manager.listen_event(SIGINT, EventManager::EventType::Signal) < 0
        || this->manager.listen_event(this->listenfd, EventManager::EventType::Read) < 0)
        throw std::runtime_error("failed to register eventlab events: ");

    while (!this->interrupt)
        this->run_event_loop();
}
```

정작 중요한 장면은 [`Server::run_event_loop()`](../../../shared-core/01-eventlab/cpp/src/Server.cpp) 안에서 열린다. 이벤트 하나를 받으면 서버는 세 갈래로만 반응한다. listen socket의 read 이벤트면 새 연결을 받아들이고, client read 이벤트면 바이트를 읽어 입력 처리를 준비하고, client write 이벤트면 `sendbuf`를 비우다가 필요하면 연결을 끊는다.

여기엔 아직 parser도 없고, room도 없고, 게임 규칙도 없다. `Client` 구조체가 들고 있는 것도 `recvbuf`, `sendbuf`, `timestamp`, `pinged`, `doomed` 정도뿐이다. 이 단출함이 중요한 이유는, 뒤쪽 lab들이 커지더라도 "지금 보고 있는 문제가 런타임인지, parser인지, 상태 전이인지"를 계속 분리해서 읽게 해 주기 때문이다.

결국 `eventlab`의 첫 장면은 "서버가 뭘 할 수 있는가"보다 "서버가 어떤 순서로만 움직이도록 먼저 묶였는가"에 가깝다. 다음 단계의 line protocol도 이 뼈대 위에서만 의미를 얻는다.

