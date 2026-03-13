# 30 Integration And Tradeoffs

## Day 1
### Session 5

통합 지점은 `SSTable.get_with_stats()` 하나로 모인다.

```python
if not self.filter.might_contain(key):
    return None, False, LookupStats(bloom_rejected=True), None

block_range, ok = self.index.find_block(key, self.data_size)
...
handle.seek(start)
block = handle.read(end - start)
```

파이프라인이 명확하다.

1. Bloom filter로 "아예 없을 가능성 높은 키"를 빠르게 거절
2. sparse index로 scan할 byte range 축소
3. 해당 구간에서만 ordered decode scan

여기서 tradeoff도 드러난다.

- Bloom bit budget을 키우면 false positive는 줄지만 metadata 크기 증가
- block_size를 키우면 index는 작아지지만 block read 단위가 커짐

이 프로젝트는 최적 파라미터를 자동 튜닝하지 않는다. 대신 조정 가능한 knobs를 코드에 노출해 두고, lookup cost를 `LookupStats`로 관측 가능하게 만든다.

CLI:

```bash
cd python/database-internals/projects/03-index-filter
PYTHONPATH=src python3 -m pytest -q
PYTHONPATH=src python3 -m index_filter
```

다음 단계 연결:

`04-buffer-pool`은 여기서 줄인 point lookup range를 page cache 관점으로 다시 다룬다. 03이 "무엇을 읽을지"를 줄였다면, 04는 "읽은 것을 언제 내보낼지"를 관리한다.