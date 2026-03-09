# Curriculum Map

## Why This Shape Exists

`legacy/`는 한 번에 너무 많은 것을 보여 줬다. 새 `study/`는 이를 “독립 과제처럼 읽히는 미니 프로젝트 + 서로 다른 두 capstone”으로 다시 정리한 것이다.

핵심 원칙은 세 가지다.

1. 각 lab은 독립 빌드/테스트가 가능해야 한다.
2. `ircserv`는 pure TCP IRC server capstone이어야 한다.
3. `arenaserv`는 C++ game-server 포트폴리오에 직접 쓰일 수 있는 authoritative capstone이어야 한다.

## Lab Sequence

1. `eventlab`
   - 주제: non-blocking socket, event loop, accept/read/write, keep-alive
2. `msglab`
   - 주제: line framing, parser, validation, IRC + arena fixture parsing
3. `roomlab`
   - 주제: session registration, IRC subset, room lifecycle
4. `ticklab`
   - 주제: authoritative fixed-step simulation, reconnect grace, snapshot correctness
5. `ircserv`
   - 주제: modern IRC command surface와 state-machine completeness
6. `arenaserv`
   - 주제: 2~4인 authoritative party arena server

## Why This Order

- `eventlab`은 소켓과 커널 이벤트 모델을 먼저 고립시킨다.
- `msglab`은 네트워크 I/O와 무관하게 parser와 validation을 검증한다.
- `roomlab`은 registration과 room lifecycle을 실제 TCP 서버에서 다룬다.
- `ticklab`은 게임서버의 핵심인 fixed-step state advance를 headless로 검증한다.
- `ircserv`는 pure protocol/server completeness를 별도의 capstone으로 남긴다.
- `arenaserv`는 최종적으로 authoritative state, room matchmaking, reconnect, snapshot을 한 서버로 묶는다.

## What Was Deliberately Removed

- Omok 규칙과 `GAME ...` 이벤트
- WebSocket JSON envelope
- React 클라이언트
- Nginx, Docker Compose, MySQL/Redis, Metrics

이 요소들은 `legacy/` 참고 범위에는 남아 있지만, 현재 `study/`의 공식 커리큘럼에는 포함하지 않는다.
