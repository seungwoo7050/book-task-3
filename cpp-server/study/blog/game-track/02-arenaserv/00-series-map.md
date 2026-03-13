# arenaserv series map

`arenaserv`을 세 편으로 나눈 이유는 engine 설명과 server 설명을 섞지 않기 위해서다. 이 capstone에서 새로 보는 것은 rule set보다 timed event loop, session token handshake, engine event fan-out, raw TCP command surface다. 그래서 시리즈도 그 축을 따라 나눠 읽히게 했다.

첫 글은 `EventManager`와 `Server`가 fixed tick을 잃지 않도록 루프를 어떻게 바꿨는지, 그리고 `HELLO`로 세션 토큰을 어떤 앞면에 올렸는지 다룬다. 둘째 글은 `QUEUE`, `READY`, `dispatch_engine_events()`를 중심으로 engine과 TCP 사이의 bridge를 따라간다. 마지막 글은 `INPUT`, `REJOIN`, `LEAVE`와 duel/rejoin, room_full, draw timeout 시나리오를 묶어 capstone proof를 정리한다.

## 글 순서

1. [10-server-surface-and-session-handshake.md](10-server-surface-and-session-handshake.md)
2. [20-queue-ready-and-engine-bridge.md](20-queue-ready-and-engine-bridge.md)
3. [30-input-rejoin-and-room-events.md](30-input-rejoin-and-room-events.md)

