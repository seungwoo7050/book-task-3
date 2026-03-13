# rollbacklab Source-First Blog

`rollbacklab`은 게임 서버 capstone이 아니다. 오히려 서버를 붙이기 전에 correction 메커니즘만 떼어 내어 읽는 중간 다리다. 여기서 먼저 확인하고 싶은 것은 "late input이 오면 어느 frame까지 되돌아가야 하는가"와 "같은 입력 세트로 다시 돌렸을 때 정말 같은 상태가 나오는가"다.

## 검증 명령

```sh
cd /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/02-rollbacklab/cpp
make clean && make test
```

## 읽는 순서

- [00-series-map.md](00-series-map.md)
- [evidence-ledger.md](evidence-ledger.md)
- [structure-plan.md](structure-plan.md)
- [10-engine-surface-and-prediction.md](10-engine-surface-and-prediction.md)
- [20-late-input-rollback-and-replay.md](20-late-input-rollback-and-replay.md)
- [30-convergence-proof-and-boundaries.md](30-convergence-proof-and-boundaries.md)
