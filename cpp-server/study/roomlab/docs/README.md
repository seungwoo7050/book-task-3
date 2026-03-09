# roomlab Docs

## Key Concepts

- registration 완료 전과 후의 command surface는 다르다.
- room membership은 서버 전역 인덱스와 connection 로컬 인덱스를 함께 갱신해야 한다.
- `QUIT`과 `disconnect`는 비슷해 보여도 broadcast 시점이 다르다.

## Reference Pointers

- `legacy/src/Executor.cpp`
- `legacy/src/execute_join.cpp`
- `legacy/src/Server.cpp`
