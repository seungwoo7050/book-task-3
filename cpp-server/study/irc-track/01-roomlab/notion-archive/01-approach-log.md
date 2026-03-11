# roomlab — 접근 방식: "다 넣고 빼기" vs "핵심만 넣기"

작성일: 2026-03-09

## 어떤 방향을 택할 것인가

이 lab을 설계할 때 가장 먼저 부딪힌 질문은 "legacy 서버에서 어디까지 가져올 것인가"였다. legacy 코드에는 이미 완성된 IRC 서버가 있다. `TOPIC`, `MODE`, `KICK`, `INVITE`까지 전부 구현되어 있고, 그 위에 WebSocket과 게임 로직까지 얹혀 있다.

그래서 두 가지 접근이 가능했다.

## 접근 A: legacy 전체를 가져와서 기능을 숨긴다

이 방법은 구현량이 적다. 코드를 통째로 복사한 뒤 advanced command의 dispatch만 막으면 된다. 하지만 문제가 있었다 — 독자가 소스를 읽었을 때, "이 lab의 범위"와 "capstone의 범위"의 경계를 스스로 구분해야 한다. `Channel.hpp`에 `invitedb`, `privdb`, `key`, `topic` 같은 필드가 보이면, 이것이 이 lab에서 쓰이는 것인지 아닌지를 코드를 끝까지 따라가야 알 수 있다.

이건 학습 도구로서 좋지 않다고 판단했다.

## 접근 B: core command path만 남긴다

이 방법을 택했다. `PASS`, `NICK`, `USER`, `JOIN`, `PART`, `PRIVMSG`, `NOTICE`, `PING`, `PONG`, `QUIT` — 이 10개만으로도 registration state machine과 room lifecycle이라는 두 핵심 축을 완전하게 보여줄 수 있다.

대신 대가가 있었다. legacy에서 코드를 가져오되, **뼈대 구조(`Connection`, `Channel`, `Executor`, `Server`)는 유지하면서 내부 로직에서 advanced 경로를 전부 제거하는 작업이 필요했다**. 단순 삭제가 아니라, 남은 코드가 여전히 정합성을 유지하는지 하나하나 확인해야 했다. 이를테면 `Channel` 클래스에 `ibit`, `tbit`, `kbit` 같은 mode flag가 남아 있는데, `MODE` command를 제거했으므로 이 flag들은 기본적으로 0 상태에서 변하지 않는다. 코드에는 남아 있지만 실행 경로에서는 도달하지 않는다.

## 테스트 전략

"JOIN이 되면 된다"는 기준은 너무 약하다. 이 lab에서 state machine이 정확하게 동작하는지를 보려면 최소한 여섯 가지를 시험해야 한다:

1. **Registration 완료** — PASS → NICK → USER 후 001 welcome이 오는가
2. **Duplicate nick rejection** — 이미 등록된 nick으로 NICK을 보내면 433이 오는가
3. **JOIN/PART** — 채널 가입과 탈퇴가 정상적으로 작동하는가
4. **PRIVMSG/NOTICE broadcast** — 채널에 보낸 메시지가 다른 멤버에게 전달되는가
5. **QUIT cleanup** — QUIT을 보내면 같은 채널의 다른 멤버에게 통보되는가
6. **Not-on-channel error** — 채널에 가입하지 않은 상태에서 PART를 보내면 442가 오는가

이 여섯 시나리오를 `test_roomlab.py`에 담았고, 세 개의 소켓(alice, bob, dup)을 동시에 연결해서 multi-client 상황까지 커버한다.
