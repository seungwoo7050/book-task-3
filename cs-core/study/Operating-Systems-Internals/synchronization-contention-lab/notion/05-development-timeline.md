# 05 Development Timeline

## 재구축 순서

```bash
cd cs-core/study/Operating-Systems-Internals/synchronization-contention-lab/problem
make test
make run-demo
```

## 2026-03-11 재검증 기록

- `make test` 결과: C binary build + shell invariant test 통과
- `make run-demo` 결과:
  - `counter` final count `160000 / 160000`
  - `gate` max concurrency `2 / 2`
  - `buffer` produced `20000`, consumed `20000`, overflow `0`

## 읽는 순서 메모

1. `problem/README.md`로 세 시나리오의 성공 조건을 다시 본다.
2. `docs/`에서 primitive와 invariant를 먼저 맞춘다.
3. `c/tests/test_cases.sh`를 읽어 pass/fail 기준이 timing이 아니라 invariant인지 확인한다.
4. demo를 돌려 metrics block shape를 눈으로 확인한다.
