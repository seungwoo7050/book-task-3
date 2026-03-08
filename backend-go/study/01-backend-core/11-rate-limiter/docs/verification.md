# Verification

## Commands

```bash
cd 01-backend-core/11-rate-limiter
make -C problem test
make -C problem bench
```

## Result

- 2026-03-07 기준 `make -C problem test`가 통과했다.
- 2026-03-07 기준 `make -C problem bench`가 통과했다.

## Remaining Checks

- Redis-backed shared limiter는 이 과제 범위에 포함하지 않았다.

