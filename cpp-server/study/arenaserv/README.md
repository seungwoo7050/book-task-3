# arenaserv

2~4인 authoritative party arena를 pure TCP로 구현한 최종 game-server capstone이다.

## Focus

- `HELLO`, `QUEUE`, `READY`, `INPUT`, `REJOIN`, `LEAVE`
- room-based matchmaking
- fixed tick movement/combat
- snapshot broadcast
- reconnect grace
- draw와 last-survivor round end

## Open

- 문제 설명: [problem/README.md](problem/README.md)
- 구현: [cpp/README.md](cpp/README.md)
- 개념 노트: [docs/README.md](docs/README.md)
