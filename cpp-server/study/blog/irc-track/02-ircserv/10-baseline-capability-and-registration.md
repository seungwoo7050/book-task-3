# ircserv 1. baseline capability와 registration을 capstone 표면으로 열기

`ircserv`을 roomlab 뒤에 바로 읽으면 가장 먼저 눈에 들어오는 차이는 구조보다 dispatcher다. 같은 runtime과 parser, 비슷한 connection/channel database를 쓰지만, [`cpp/src/Executor.cpp`](../../../irc-track/02-ircserv/cpp/src/Executor.cpp)의 `process()`가 열어 두는 command 집합이 확연히 넓어진다.

```cpp
case Message::KICK:   _execute_kick(server, node, *it); break;
case Message::INVITE: _execute_invite(server, node, *it); break;
case Message::TOPIC:  _execute_topic(server, node, *it); break;
case Message::CAP:    _execute_cap(server, node, *it); break;
case Message::MODE:   _execute_mode(server, node, *it); break;
```

이 차이가 중요한 이유는, capstone의 경계가 helper 함수 개수보다 "실제로 노출된 command surface"에서 가장 분명하게 드러나기 때문이다. roomlab에도 일부 helper는 있었지만 dispatcher가 subset 범위만 열어 두고 있었다. ircserv에서는 그 문이 실제로 열린다.

그렇다고 registration이 완전히 새로워지지는 않는다. `PASS`, `NICK`, `USER` 흐름은 roomlab와 이어지고, `_execute_user()`도 여전히 `001`부터 `005 ISUPPORT`까지 묶어 보낸다. 대신 `_execute_cap()`이 `CAP LS 302`에 대해 `CAP * LS :`를 돌려주면서, raw TCP client가 "이 서버는 이제 capstone 표면을 갖고 있다"는 최소 신호를 먼저 볼 수 있게 된다.

이 설계는 [`tests/test_irc_join.py`](../../../irc-track/02-ircserv/cpp/tests/test_irc_join.py)에서 바로 드러난다. alice는 registration 전에 `CAP LS 302`를 보내고 응답을 확인한 뒤, alice, bob, carol 세 사용자가 모두 registration을 끝낸다. 즉 첫 장면의 핵심은 기능이 많아졌다는 인상이 아니라, baseline registration 위에 capability probe와 advanced routing이 자연스럽게 얹힌다는 점에 있다.

그래서 `ircserv`의 첫 글은 "더 큰 IRC 서버" 소개가 아니라, subset에서 capstone으로 넘어가는 문이 어디서 열리는지를 짚는 글로 읽는 편이 맞다. 그 문을 지나면, 다음엔 channel privilege와 mode state가 실제로 의미를 갖기 시작한다.

