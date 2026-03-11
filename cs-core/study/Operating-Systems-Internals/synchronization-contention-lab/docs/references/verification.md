# Synchronization Contention Lab 검증 기록

## canonical 명령

```bash
cd problem
make test
make run-demo
```

## 테스트가 고정하는 것

- counter에서 `final_count == expected_count`
- gate에서 `max_concurrency <= permit_limit`
- buffer에서 `produced == consumed`
- buffer에서 `underflow == 0`, `overflow == 0`

## demo에서 확인할 것

- 각 시나리오가 `scenario=...` 형식의 metrics block을 출력한다
- `ok=1`이 모든 시나리오에서 유지된다
- elapsed time은 출력되지만 pass/fail 기준은 invariant다
