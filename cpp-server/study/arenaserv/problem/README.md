# arenaserv Problem

이 문서는 원본 과제 문서가 없는 상태에서 `legacy/` 코드를 바탕으로 재구성한 문제 설명이다.

## Reconstructed Prompt

C++17 pure TCP authoritative game server `arenaserv`를 작성한다. 실행 표면은 다음과 같다.

```sh
./arenaserv <port>
```

서버는 다음 command/event 계약을 따라야 한다.

- client command: `HELLO <nick>`, `QUEUE`, `READY`, `INPUT <seq> <dx> <dy> <facing> <fire>`, `PING <ms>`, `REJOIN <token>`, `LEAVE`
- server event: `WELCOME <token>`, `ROOM <room_id> <phase>`, `COUNTDOWN <seconds>`, `SNAPSHOT <tick> <json>`, `HIT <tick> <attacker> <target> <hp>`, `ELIM <tick> <nick>`, `ROUND_END <winner|draw>`, `ERROR <code> <message>`

게임 규칙은 20x20 bounded tile arena, 2~4인 room, HP 3, 단일 action `FIRE`, 10초 reconnect grace로 고정한다.

## Deliverables

- authoritative TCP arena server
- bot/script 기반 2인, 3인, 4인 smoke test

## Provenance

| source | why it matters |
| --- | --- |
| `legacy/src/EventManager.cpp` | cross-platform event loop의 직접 출처 |
| `legacy/src/GameRoom.cpp` | room-based match ownership 아이디어의 참고 자료 |
| `legacy/src/GameLogic.cpp` | server-authoritative 판정 구조의 참고 자료 |
| `legacy/docs/game-protocol.md` | command/event 계약을 문서화하는 방식의 참고 자료 |
| `legacy/docs/portfolio-checklist.md` | 제출용 시연 시나리오가 어떤 이벤트를 요구하는지 보여 주는 참고 자료 |
