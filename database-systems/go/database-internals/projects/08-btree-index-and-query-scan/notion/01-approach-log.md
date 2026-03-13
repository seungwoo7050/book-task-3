# Approach Log

- `BTreeIndex`와 `QueryScanExecutor`를 분리해 index invariant와 planner 판단을 따로 검증한다.
- leaf split -> duplicate lookup -> range cursor -> planner 순서로 작은 신호를 쌓는다.
