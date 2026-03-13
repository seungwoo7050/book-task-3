# rollbacklab 3. convergence proof와 현재 경계

마지막 장면은 replay가 deterministic한지 확인하는 부분이다. [`verify_replay()`](../../../game-track/02-rollbacklab/cpp/src/RollbackSession.cpp)는 rollback 후 남은 `applied_inputs_`를 같은 순서로 한 번 더 시뮬레이션해 최종 상태가 같은지 본다.

[`test_rollbacklab.cpp`](../../../game-track/02-rollbacklab/cpp/tests/test_rollbacklab.cpp)는 네 가지 경계를 고정한다.

- future input fast path
- late input rollback
- identical late input no-op fast path
- two-player resimulation convergence

현재 범위 밖은 분명하다. UDP transport, client-side reconciliation, anti-cheat, rollback netcode 전체는 아직 넣지 않았다. 이 프로젝트는 correction engine만 먼저 분리한 lab이다.
