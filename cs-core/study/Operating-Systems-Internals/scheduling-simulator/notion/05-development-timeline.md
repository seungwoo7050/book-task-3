# 05 Development Timeline

## 재구축 순서

```bash
cd cs-core/study/Operating-Systems-Internals/scheduling-simulator/problem
make test
make run-demo
```

## 2026-03-11 재검증 기록

- `make test` 결과: `4 passed`
- `make run-demo` 결과:
  - `fcfs` 평균 waiting `6.67`
  - `sjf` 평균 waiting `2.67`
  - `rr` 평균 response `2.0`
  - `mlfq` 평균 response `1.0`

## 읽는 순서 메모

1. `problem/README.md`로 범위를 다시 잡는다.
2. `docs/`에서 metric과 policy tradeoff 용어를 맞춘다.
3. `tests/`를 읽어 어떤 fixture와 assertion이 고정됐는지 확인한다.
4. 마지막으로 demo를 돌려 replay와 summary shape를 눈으로 확인한다.
