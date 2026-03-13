# 10 Registration And Server Surface

## Day 1
### Session 1

- 목표: `roomlab`이 단순 채팅 서버가 아니라 registration gate를 가진 IRC subset인지 먼저 확인한다.
- 진행: `problem/README.md`, `cpp/README.md`, `main.cpp`, `Server.hpp`, `Executor::_execute_pass/_execute_nick/_execute_user`를 순서대로 읽었다.
- 이슈: 처음엔 `JOIN`부터 보는 편이 더 자연스러워 보였지만, 실제 smoke test도 `PASS -> NICK -> USER`가 선행되지 않으면 아무 room state도 만들 수 없다.
- 판단: 이 프로젝트의 첫 질문은 channel 기능이 아니라 "registered client만 어떤 surface를 열어 줄 것인가"다.

CLI:

```bash
$ cd study/irc-track/01-roomlab/cpp
$ sed -n '1,200p' README.md
$ sed -n '1,200p' include/inc/Server.hpp
$ sed -n '1,220p' src/main.cpp
$ rg -n "_execute_pass|_execute_nick|_execute_user|_isupport" src/Executor.cpp
$ sed -n '1,220p' src/Executor.cpp
```

이 시점의 핵심 코드는 registration 완료 시점에 붙는 welcome surface였다.

```cpp
rpl = BUILD_RPL_WELCOME(server.servername, "localhost", node->nickname, node->username, node->hostname);
rpl += BUILD_RPL_YOURHOST(server.servername, node->nickname, server.version);
rpl += BUILD_RPL_CREATED(server.servername, node->nickname);
rpl += BUILD_RPL_MYINFO(server.servername, node->nickname, server.version, "", "");
rpl += _isupport(server, node);
```

처음엔 `001` welcome만 오면 등록이 끝난다고 생각했는데, 실제로는 `005 ISUPPORT`까지 같은 흐름에 붙어 있기 때문에 client 입장에서는 "이 서버가 어떤 IRC subset을 약속하는가"까지 registration의 일부로 받게 된다.

같은 이유로 서버 내부 DB도 등록 중심으로 잡혀 있다.

```cpp
std::map<int, std::list<Connection *>::iterator>            sockdb;
std::map<std::string, std::list<Connection *>::iterator>    nickdb;
std::list<Channel *>                                        chans;
std::map<std::string, std::list<Channel *>::iterator>       chandb;
```

나중에 보니 `roomlab`은 room command 이전에 "연결을 닉네임과 channel membership으로 인덱싱하는 법"을 먼저 고정한 프로젝트였다.

