# Approach Log

- `RollbackSession` 하나를 공개 표면으로 두고 내부에 buffer / snapshots / applied input map을 묶는다.
- prediction과 replay를 같은 simulation 함수로 돌려 deterministic check를 단순하게 만든다.
