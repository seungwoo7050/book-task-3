# 01 Mini LSM Store 시리즈 맵

이 프로젝트는 Python `database-internals` 트랙의 첫 진입점이지만, 실제로는 memtable, flush, SSTable, reopen까지 한 번에 묶어 보여 주는 꽤 압축된 슬롯이다. 읽을 때도 "간단한 key-value store"로 보기보다 `active memtable -> immutable snapshot -> newest-first SSTable read`가 어떤 순서로 잠기는지 먼저 붙드는 편이 맞다.

## 먼저 보고 갈 질문

- threshold를 넘는 write가 정확히 언제 active memtable을 SSTable로 내리는가?
- tombstone `None`은 memtable과 SSTable을 가로질러 어떻게 삭제 의미를 유지하는가?
- reopen 이후에는 왜 `000002.sst`가 `000001.sst`보다 먼저 읽혀야 하는가?

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md)
   파일 구조와 테스트 이름을 먼저 보면서 이 슬롯이 단순 CRUD가 아니라 flush/reopen까지 포함한다는 사실을 잡는다.
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md)
   `force_flush`, `get`, `open`, `_replace_memtable_value`가 실제로 어떤 invariant를 고정하는지 따라간다.
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md)
   pytest와 demo, 추가 보조 재실행으로 현재 공개 표면과 빠진 범위를 정리한다.

## 재검증 명령

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/01-mini-lsm-store
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m mini_lsm_store
```

## 이번 시리즈의 근거

- `database-systems/python/database-internals/projects/01-mini-lsm-store/README.md`
- `database-systems/python/database-internals/projects/01-mini-lsm-store/problem/README.md`
- `database-systems/python/database-internals/projects/01-mini-lsm-store/docs/README.md`
- `database-systems/python/database-internals/projects/01-mini-lsm-store/docs/concepts/flush-lifecycle.md`
- `database-systems/python/database-internals/projects/01-mini-lsm-store/docs/concepts/read-path.md`
- `database-systems/python/database-internals/projects/01-mini-lsm-store/src/mini_lsm_store/store.py`
- `database-systems/python/database-internals/projects/01-mini-lsm-store/src/mini_lsm_store/__main__.py`
- `database-systems/python/database-internals/projects/01-mini-lsm-store/tests/test_mini_lsm_store.py`

## 보조 메모

작업 메모가 필요할 때만 [_evidence-ledger.md](_evidence-ledger.md)와 [_structure-outline.md](_structure-outline.md)를 펼치면 된다. 공개 시리즈는 `00 -> 10 -> 20 -> 30`만 읽어도 충분하다.
