# arenaserv Docs

## Key Concepts

- authoritative game server는 transport보다 session/state continuity가 중요하다.
- reconnect는 token 발급만으로 끝나지 않고 snapshot regeneration이 따라와야 한다.
- room queue와 match loop를 분리하지 않으면 game rule bug와 session bug가 섞이기 쉽다.

## Reference Pointers

- `legacy/src/EventManager.cpp`
- `legacy/src/GameRoom.cpp`
- `legacy/src/GameLogic.cpp`
- `legacy/docs/game-protocol.md`
