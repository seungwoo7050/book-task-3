# 05 Development Timeline

## 재구축 순서

```bash
cd cs-core/study/Operating-Systems-Internals/virtual-memory-lab/problem
make test
make run-demo
```

## 2026-03-11 재검증 기록

- `make test` 결과: `4 passed`
- `make run-demo` 결과:
  - `fifo` faults `9`
  - `lru` faults `10`
  - `clock` faults `9`
  - `opt` faults `7`

## 읽는 순서 메모

1. `problem/README.md`로 trace 계약을 확인한다.
2. `docs/`에서 locality와 policy 용어를 맞춘다.
3. `tests/`를 읽어 anomaly/locality/dirty assertion이 무엇인지 본다.
4. demo를 돌려 replay와 summary 형식을 눈으로 확인한다.
