# 40 Verification And Boundaries

## Day 1
### Session 6

최종 확인은 flush/close 경계였다.

```python
def close(self) -> None:
    self.flush_all()
    for handle in self.file_handles.values():
        handle.close()
```

close가 단순 핸들 정리가 아니라 `flush_all()`을 먼저 호출한다. 즉 dirty 페이지는 explicit flush를 놓쳐도 close에서 마지막으로 디스크에 반영된다.

CLI:

```bash
cd python/database-internals/projects/04-buffer-pool
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m buffer_pool
```

검증 신호:

- `7 passed`
- demo 출력의 `pin_count: 1`, `prefix: 'page-0'`

demo는 간단하지만 의미가 있다. disk-backed page를 fetch하면 곧바로 pin된 프레임이 반환된다는 걸 보여 준다.

이 단계의 boundary:

- 다루는 것:
  - LRU 기반 후보 선택
  - pin/dirty 기반 eviction safety
  - close 시 flush 보장
- 다루지 않는 것:
  - concurrent buffer pool access
  - multi-victim retry policy
  - page replacement benchmarking

다음 질문:

- MVCC 버전 체인이 page 단위 storage와 결합되면 flush/granularity는 어떻게 바뀌나
- WAL이 있는 엔진에서 dirty page flush 순서는 어떤 제약을 가져야 하나