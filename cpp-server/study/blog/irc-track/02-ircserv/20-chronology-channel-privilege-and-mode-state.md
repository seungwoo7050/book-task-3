# 20 Channel Privilege And Mode State

## Day 1
### Session 2

- 목표: `ircserv`가 `roomlab`과 달라지는 핵심이 무엇인지 channel state 구조에서 확인한다.
- 진행: `Channel.hpp`, `Channel.cpp`, `_execute_mode`, `_execute_topic`를 이어서 읽었다.
- 이슈: 처음엔 command 개수가 capstone 차이라고 생각했지만, 실제로는 operator privilege와 mode bit를 별도 상태로 들고 다니는 점이 더 큰 변화였다.
- 판단: `ircserv`의 두 번째 답은 "channel을 메시지 대상"에서 "권한과 정책을 가진 객체"로 올리는 것이다.

CLI:

```bash
$ cd study/irc-track/02-ircserv/cpp
$ sed -n '1,200p' include/inc/Channel.hpp
$ rg -n "_execute_mode|_execute_topic|ibit|tbit|kbit|lbit" src/Executor.cpp include/inc/Channel.hpp
$ sed -n '656,860p' src/Executor.cpp
```

이 시점의 핵심 코드는 `Channel`이 들고 있는 mode bit 집합이었다.

```cpp
static unsigned lbit;
static unsigned ibit;
static unsigned tbit;
static unsigned kbit;
```

처음엔 `MODE +i`나 `MODE +k`가 단순 명령 처리처럼 보였는데, 실제로는 invite-only, topic restriction, key, user limit를 전부 channel state에 비트로 접어 넣기 때문에 이후 `JOIN`, `TOPIC`, `INVITE`, `KICK`가 모두 같은 상태를 참조하게 된다.

이 선택은 topic 변경 권한에서도 그대로 드러난다.

```cpp
if (chan->state & Channel::tbit && chan->privdb.find(node) == chan->privdb.end())
{
    dispatch_packet(server, node, BUILD_ERR_CHANOPRIVSNEEDED(server.servername, channame));
    return;
}
```

나중에 보니 `ircserv`의 capstone성은 command 수보다도 "같은 상태를 여러 명령이 공유한다"는 설계에서 나온다.

