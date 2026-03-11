# Problem Guide

## 문제 핵심

- trace 형식은 줄 단위 `<R|W> <page>`로 고정한다.
- page replacement policy는 FIFO, LRU, Clock, OPT로 고정한다.
- frame 수와 trace가 주어졌을 때 hits, faults, dirty evictions를 계산한다.
- `--replay`는 각 접근 뒤 frame 상태를 표 형태로 출력한다.

## 이번 범위에서 일부러 뺀 것

- TLB
- process address space와 page table walking
- huge page, NUMA, swap daemon

## 제공 자료

- `data/belady.trace`
- `data/locality.trace`
- `data/dirty.trace`

## canonical 검증

```bash
make test
make run-demo
```

## 성공 기준

- classic Belady anomaly 예제가 FIFO에서 재현된다.
- locality trace에서 LRU/OPT가 FIFO보다 나쁘지 않다.
- dirty trace에서 dirty eviction이 정확히 계산된다.
