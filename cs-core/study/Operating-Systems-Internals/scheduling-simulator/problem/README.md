# Problem Guide

## 문제 핵심

- 입력 fixture는 JSON 배열 `[{ "pid": "...", "arrival": <int>, "burst": <int> }]` 형식으로 고정한다.
- 단일 CPU, 정수 tick, 단일 CPU burst만 다룬다.
- FCFS, non-preemptive SJF, RR(quantum 2), MLFQ(3 queues, quanta 1/2/4, dispatch-boundary boost 10 ticks)를 구현한다.
- 정책별 평균 waiting time, response time, turnaround time과 ASCII replay를 출력한다.

## 이번 범위에서 일부러 뺀 것

- multi-core scheduling
- I/O burst와 blocking
- context switch overhead
- dynamic priority aging beyond the fixed MLFQ boost

## 제공 자료

- `data/convoy.json`: classic convoy-like workload
- `data/interactive-mix.json`: 짧은 interactive job이 섞인 workload

## canonical 검증

```bash
make test
make run-demo
```

## 성공 기준

- fixture가 policy별 deterministic timeline을 만든다.
- FCFS/SJF/RR/MLFQ 결과가 tests의 golden expectation과 일치한다.
- `run-demo`가 policy별 replay와 metrics table을 같은 shape로 출력한다.
