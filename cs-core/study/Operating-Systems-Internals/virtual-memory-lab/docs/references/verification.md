# Virtual Memory Lab 검증 기록

## canonical 명령

```bash
cd problem
make test
make run-demo
```

## 테스트가 고정하는 것

- `belady.trace`에서 FIFO 3-frame faults `9`, 4-frame faults `10`
- `locality.trace`에서 `opt <= lru <= fifo` fault 비교
- `dirty.trace`에서 dirty eviction count
- Clock replay가 deterministic하게 유지되는지

## demo에서 확인할 것

- policy별 step replay가 `idx / access / hit / evicted / dirty / snapshot` 형식으로 나온다
- summary 표에 `faults / hits / dirty_evictions`가 함께 나온다
