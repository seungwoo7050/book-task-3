# rollbacklab series map

`rollbacklab`을 세 편으로 나눈 이유는 rollback의 질문을 세 덩어리로 나눠야 설명이 깔끔하기 때문이다.

1. 공개 표면과 prediction이 무엇인가
2. late input이 오면 어떻게 rollback / resimulation 하는가
3. replay가 deterministic하다는 것을 어떻게 증명하는가

## 재검증 명령

```sh
cd /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/02-rollbacklab/cpp
make clean && make test
```

## 근거 파일

- `study/game-track/02-rollbacklab/cpp/include/inc/RollbackSession.hpp`
- `study/game-track/02-rollbacklab/cpp/src/RollbackSession.cpp`
- `study/game-track/02-rollbacklab/cpp/tests/test_rollbacklab.cpp`
- `study/game-track/02-rollbacklab/problem/data/late-input-timeline.txt`
