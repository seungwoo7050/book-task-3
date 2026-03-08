# Verification

## Commands

```bash
cd 01-backend-core/06-go-api-standard
make -C problem test
make -C problem build
```

## Result

- 2026-03-07 기준 `make -C problem test`가 통과했다.
- 2026-03-07 기준 `make -C problem build`가 통과했다.

## Remaining Checks

- `healthcheck` 런타임 검증은 legacy 라운드에서 확인됐고, study 라운드에서는 test/build를 우선 기준으로 사용했다.

