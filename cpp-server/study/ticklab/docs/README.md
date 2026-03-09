# ticklab Docs

## Key Concepts

- authoritative server는 입력을 즉시 반영하지 않고 tick 경계에서 적용한다.
- reconnect는 transport 문제가 아니라 session/state continuity 문제다.
- snapshot은 디버깅 출력이 아니라 state recovery 계약이다.

## Reference Pointers

- `legacy/src/GameRoom.cpp`
- `legacy/src/GameLogic.cpp`
- `legacy/docs/game-protocol.md`
