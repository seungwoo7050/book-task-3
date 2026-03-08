# Verification

## Commands

```bash
cd 01-backend-core/10-concurrency-patterns
make -C problem test
make -C problem bench
```

## Result

- 2026-03-07 기준 `make -C problem test`가 통과했다.
- 2026-03-07 기준 `make -C problem bench`가 통과했다.

## Remaining Checks

- 실서비스 queue/backpressure 정책은 별도 과제로 남겼다.

