# 03 Index Filter 시리즈 맵

이 프로젝트는 앞선 슬롯들이 "어떻게 안전하게 저장할 것인가"를 붙잡았다면, 이제는 "어떻게 덜 읽고 찾을 것인가"로 질문을 옮긴다. 읽을 때도 Bloom filter와 sparse index를 따로 외우기보다 `negative lookup을 빨리 거르고, positive lookup은 작은 block만 읽는다`는 두 단계 최적화를 먼저 붙드는 편이 정확하다.

## 먼저 보고 갈 질문

- miss를 전체 SSTable scan 없이 끝내려면 Bloom filter가 어떤 역할을 해야 하는가?
- hit일 때도 왜 전체 data section을 읽지 않고 bounded block만 읽게 되는가?
- footer metadata는 filter와 index를 어떻게 다시 찾아오게 만드는가?

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md)
   테스트와 문제 정의를 다시 보며 이 슬롯의 초점이 "정확도"보다 "bytes read 경계"라는 점을 먼저 잡는다.
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md)
   `BloomFilter`, `SparseIndex`, `SSTable.write/load/get_with_stats()`가 lookup 비용을 어디서 줄이는지 본다.
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md)
   pytest, demo, 보조 재실행으로 bloom reject, bounded scan, footer 복원이 실제로 어떤 숫자로 보이는지 정리한다.

## 재검증 명령

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/03-index-filter
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m index_filter
```

## 이번 시리즈의 근거

- `database-systems/python/database-internals/projects/03-index-filter/README.md`
- `database-systems/python/database-internals/projects/03-index-filter/problem/README.md`
- `database-systems/python/database-internals/projects/03-index-filter/docs/README.md`
- `database-systems/python/database-internals/projects/03-index-filter/docs/concepts/bloom-filter-sizing.md`
- `database-systems/python/database-internals/projects/03-index-filter/docs/concepts/sparse-index-scan.md`
- `database-systems/python/database-internals/projects/03-index-filter/src/index_filter/table.py`
- `database-systems/python/database-internals/projects/03-index-filter/src/index_filter/__main__.py`
- `database-systems/python/database-internals/projects/03-index-filter/tests/test_index_filter.py`

## 보조 메모

작업 메모는 [_evidence-ledger.md](_evidence-ledger.md)와 [_structure-outline.md](_structure-outline.md)에 남긴다. 공개 시리즈는 `00 -> 10 -> 20 -> 30`만 읽어도 충분하다.
