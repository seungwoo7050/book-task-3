# rollbacklab 2. late input이 오면 어디까지 되감는가

rollback의 핵심은 [`submit_input()`](../../../game-track/02-rollbacklab/cpp/src/RollbackSession.cpp)에 있다. 미래 frame의 입력이면 버퍼에만 쌓고 끝내지만, 이미 지난 frame의 입력이 바뀌면 그 frame 직전 snapshot으로 되돌아간 뒤 현재 frame까지 다시 계산한다.

이때 중요한 자료구조가 두 개다.

- `snapshots_`: frame별 world state 기준점
- `applied_inputs_`: 각 frame에서 실제로 사용한 input 기록

두 맵이 같은 frame key를 쓰기 때문에 rollback window를 `input.frame -> current_frame`으로 딱 잘라 다시 돌릴 수 있다.
