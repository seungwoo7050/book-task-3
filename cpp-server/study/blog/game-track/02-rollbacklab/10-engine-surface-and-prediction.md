# rollbacklab 1. engine 표면과 prediction부터 고정하기

첫 장면에서 중요한 것은 `RollbackSession`이 공개하는 표면을 줄이는 일이다. [`RollbackSession.hpp`](../../../game-track/02-rollbacklab/cpp/include/inc/RollbackSession.hpp)는 `FrameInputBuffer`, `StateSnapshot`, `ResimResult`를 밖으로 드러내지만, 네트워크나 room lifecycle은 아예 넣지 않는다.

prediction은 [`predicted_input_for()`](../../../game-track/02-rollbacklab/cpp/src/RollbackSession.cpp)에서 드러난다. 현재 frame의 explicit input이 없으면 직전 frame의 applied input을 복제해 같은 방향으로 한 번 더 밀어 본다. 이게 local prediction의 가장 작은 형태다.
