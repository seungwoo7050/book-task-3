# 10 Runtime And Socket Surface

## Day 1
### Session 1

- 목표: `eventlab`이 parser 실험이 아니라 `runtime-only` lab이라는 점을 먼저 소스에서 확인한다.
- 진행: `README`, `problem/README.md`, `cpp/README.md`, `main.cpp`, `Server.hpp`, `EventManager.hpp`를 한 화면에서 대조했다.
- 이슈: 처음엔 `Server.cpp` 한 파일이 lab 전체처럼 보였지만, 실제 entrypoint는 signal 처리와 port validation까지 묶은 process surface였다.
- 판단: 이 시점의 핵심은 `ECHO` 기능이 아니라 "어디까지를 runtime으로 설명할 것인가"였다.

CLI:

```bash
$ cd study/shared-core/01-eventlab
$ sed -n '1,160p' README.md
$ sed -n '1,160p' problem/README.md
$ sed -n '1,160p' cpp/README.md
$ sed -n '1,200p' cpp/include/inc/Server.hpp
$ sed -n '1,160p' cpp/src/main.cpp
```

이 시점의 핵심 코드는 아래였다.

```cpp
struct Client
{
    int         fd;
    std::string ipaddr;
    std::string recvbuf;
    std::string sendbuf;
    std::time_t timestamp;
    bool        pinged;
    bool        doomed;
};
```

처음엔 단순 socket wrapper 정도로 봤는데, `recvbuf`, `sendbuf`, `timestamp`, `pinged`, `doomed`가 한 구조에 모여 있는 순간 이 lab이 read/write 자체보다 "연결 수명주기 상태를 어떻게 쥘 것인가"를 먼저 다룬다는 점이 분명해졌다.

entrypoint도 같은 방향으로 최대한 작다.

```cpp
if (ac != 2)
{
    std::cerr << "usage: " << av[0] << " <port>" << std::endl;
    return 1;
}
```

처음엔 signal 처리 코드가 더 눈에 들어왔지만, 나중에 보니 이 usage surface가 먼저 고정돼 있기 때문에 `eventlab`은 password나 추가 protocol state 없이도 독립 lab으로 읽힐 수 있었다.

다음 질문:

- listening socket과 client socket을 같은 event manager 위에 어떻게 올리는가
- idle detection은 kernel timeout이 아니라 application state로 어떻게 유지하는가
