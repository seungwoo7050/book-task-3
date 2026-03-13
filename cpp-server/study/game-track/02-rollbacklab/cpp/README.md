# rollbacklab cpp

`RollbackSession` 하나만 공개 표면으로 두는 headless simulation lab이다. 네트워크, 세션 관리, room queue는 넣지 않고 late input 때문에 이미 계산한 frame을 다시 돌리는 핵심만 남겼다.

## 핵심 타입

- `PlayerInput`: frame-stamped input
- `FrameInputBuffer`: explicit input을 frame별로 보관하는 버퍼
- `StateSnapshot`: rollback 기준점
- `ResimResult`: rollback 범위와 convergence 결과
- `RollbackSession`: prediction, rollback, resimulation을 묶는 엔진

## 검증

```sh
cd /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/02-rollbacklab/cpp
make clean && make test
```
