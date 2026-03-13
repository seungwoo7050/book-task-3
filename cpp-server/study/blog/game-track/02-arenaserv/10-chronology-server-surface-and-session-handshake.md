# 10 Server Surface And Session Handshake

## Day 1
### Session 1

- 목표: `arenaserv`가 임의의 raw TCP server가 아니라 token-based session handshake를 가진 game capstone인지 먼저 확인한다.
- 진행: `problem/README.md`, `cpp/README.md`, `Server.hpp`, `main.cpp`, `Server::handle_line`, `handle_hello`를 함께 읽었다.
- 이슈: 처음엔 `HELLO`가 단순 welcome command처럼 보였지만, 실제로는 이후 `QUEUE`, `READY`, `INPUT`, `REJOIN` 전부를 여는 세션 토큰 발급 지점이었다.
- 판단: 이 프로젝트의 첫 질문은 projectile rule이 아니라 "connection이 session을 언제 소유하게 되는가"다.

CLI:

```bash
$ cd study/game-track/02-arenaserv/cpp
$ sed -n '1,200p' README.md
$ sed -n '1,220p' include/inc/Server.hpp
$ rg -n "handle_line|handle_hello|token_to_fd" src/Server.cpp include/inc/Server.hpp
$ sed -n '210,340p' src/Server.cpp
```

이 시점의 핵심 코드는 command dispatcher에서 `HELLO`를 별도 핸드셰이크로 빼는 부분이었다.

```cpp
if (command == "HELLO")
{
    if (tokens.size() != 2)
        this->send_error(client, "invalid_input", "usage: HELLO <nick>");
    else
        this->handle_hello(client, tokens[1]);
    return;
}
```

처음엔 raw line parser만 있으면 충분할 것 같았는데, 실제 server surface는 첫 명령부터 `QUEUE`와 동등하지 않다. `HELLO`가 세션 토큰을 만들고 `token_to_fd`를 채운 뒤에야 이후 command들이 의미를 갖기 때문이다.

이 handshake는 `Server`의 내부 상태에도 그대로 남는다.

```cpp
std::map<int, Client>      clients;
std::map<std::string, int> token_to_fd;
MatchEngine                engine;
```

나중에 보니 `arenaserv`의 capstone성은 socket 연결과 game session을 명시적으로 분리해 놓은 데서 먼저 드러났다.

