# 30 Input Rejoin And Room Events

## Day 2
### Session 1

- 목표: input parsing과 rejoin failure path가 server와 engine 사이에서 어떻게 나뉘는지 본다.
- 진행: `handle_input`, `handle_rejoin`, `MatchEngine::rejoin_player`, test의 duplicate nick, invalid input, stale sequence, expired session 시나리오를 함께 읽었다.
- 이슈: 처음엔 모든 validation이 engine 안에 있을 줄 알았지만, 실제로는 `seq/dx/dy/fire`가 정수인지 같은 텍스트 수준 검사는 server가 먼저 자르고, 상태 의미 검사는 engine이 맡는다.
- 판단: `arenaserv`의 세 번째 답은 "server는 parse와 ownership, engine은 state legality"라는 분담이다.

CLI:

```bash
$ cd study/game-track/02-arenaserv/cpp
$ rg -n "handle_input|handle_rejoin|send_error|rejoin_player|stale_sequence|expired_session" src/Server.cpp src/MatchEngine.cpp tests/test_arenaserv.py
$ sed -n '300,420p' src/Server.cpp
$ sed -n '260,360p' src/MatchEngine.cpp
$ sed -n '60,180p' tests/test_arenaserv.py
```

이 시점의 핵심 코드는 server와 engine이 서로 다른 종류의 오류를 처리하는 경계였다.

```cpp
long seq = std::strtol(seq_token.c_str(), &endptr, 10);
if (*endptr != '\0')
{
    this->send_error(client, "invalid_input", "seq must be an integer");
    return;
}
```

처음엔 `INPUT` 전체를 engine에 넘겨 버리는 편이 더 간단해 보였는데, 실제 server는 텍스트 protocol의 기초 parsing을 먼저 끝낸 뒤에만 엔진을 호출한다. 그래서 `invalid_input`과 `stale_sequence`가 같은 오류처럼 보여도 출처는 다르다.

```cpp
MatchEngine::Error error;
MatchEngine::Input input(static_cast<int>(seq), static_cast<int>(dx), static_cast<int>(dy), facing_token.empty() ? 'N' : facing_token[0], fire != 0);
if (!this->engine.submit_input(client.token, input, error))
{
    this->send_error(client, error.code, error.message);
    return;
}
```

rejoin도 같은 식으로 갈라진다.

```cpp
if (!this->engine.rejoin_player(token, error))
{
    this->send_error(client, error.code, error.message);
    return;
}

client.token = token;
this->token_to_fd[token] = client.fd;
```

나중에 보니 `REJOIN`은 socket 복구가 아니라 token ownership을 새 연결로 옮기는 작업이었고, grace window의 실질 판단은 이미 engine이 들고 있었다.
