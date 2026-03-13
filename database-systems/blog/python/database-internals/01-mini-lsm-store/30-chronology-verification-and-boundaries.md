# 30 reopen이 되는 이유, 그리고 WAL 없는 세계의 한계

## Day 2
### Session 1

어제 끝에 남겼던 질문 — `open()`으로 다시 열 때도 newest-first 순서가 유지되는가. 코드를 열어봤다.

```python
def open(self) -> None:
    self.data_dir.mkdir(parents=True, exist_ok=True)
    self.sstables = []
    sequences: list[int] = []
    for path in sorted(self.data_dir.glob("*.sst")):
        table = SSTable(path)
        table.load()
        self.sstables.append(table)
        sequences.append(int(path.stem))
    self.sstables.reverse()
```

파일명이 `000001.sst`, `000002.sst` 같은 sequence 번호다. `sorted()` → `append()` → `reverse()`. 오름차순으로 읽은 다음 뒤집으니까 결국 높은 sequence가 앞에 온다. flush할 때 `insert(0, ...)` 했던 것과 같은 newest-first 순서가 reopen 후에도 복원된다.

이 시점에서 `test_persistence_after_reopen`을 실행해서 확인했다.

```bash
cd python/database-internals/projects/01-mini-lsm-store
PYTHONPATH=src python3 -m pytest tests/test_mini_lsm_store.py::test_persistence_after_reopen -v
```

```text
tests/test_mini_lsm_store.py::test_persistence_after_reopen PASSED
```

통과는 하는데, 여기서 한 가지 불편한 점이 보인다. `close()`가 `force_flush()`를 호출한다. 즉, `close()` 없이 프로세스가 죽으면? memtable에만 있던 데이터는 사라진다. WAL이 없으니까.

이건 버그가 아니라 이 프로젝트의 의도적인 경계다. persistence는 "flush된 것까지만" 보장한다. 다음 프로젝트(02-wal-recovery)가 이 빈자리를 메꿔줘야 하는 이유가 여기서 나온다.

### Session 2

전체 테스트를 한번 돌렸다.

```bash
cd python/database-internals/projects/01-mini-lsm-store
PYTHONPATH=src python3 -m pytest -v
```

```text
tests/test_mini_lsm_store.py::test_put_and_get PASSED
tests/test_mini_lsm_store.py::test_missing_key PASSED
tests/test_mini_lsm_store.py::test_update PASSED
tests/test_mini_lsm_store.py::test_delete PASSED
tests/test_mini_lsm_store.py::test_flush_creates_sstable PASSED
tests/test_mini_lsm_store.py::test_read_after_force_flush PASSED
tests/test_mini_lsm_store.py::test_memtable_wins_over_sstable PASSED
tests/test_mini_lsm_store.py::test_tombstone_across_levels PASSED
tests/test_mini_lsm_store.py::test_persistence_after_reopen PASSED

9 passed in 0.03s
```

demo도 확인했다.

```bash
PYTHONPATH=src python3 -m mini_lsm_store
```

```text
{'key': 'alpha', 'found': True, 'value': '3', 'sstables': 1}
```

demo가 보여주는 것: `alpha`에 먼저 `"1"`을 넣고 flush한 뒤 `"3"`을 memtable에 덮어쓴다. `get("alpha")`가 `"3"`을 반환한다. memtable이 SSTable보다 우선한다는 규칙이 demo 한 줄에 압축돼 있다.

이 프로젝트를 닫으면서 정리하면:
- 한 파일이라서 얕아 보이지만, `get`의 조회 순서 하나가 LSM read path의 본질을 담고 있다
- tombstone은 `None`으로 표현하고, `found=True`로 하위 계층 차단
- newest-first는 flush 시 `insert(0, ...)`, reopen 시 `reverse()`로 유지
- 이 프로젝트의 durability 경계는 flush까지. crash 전 memtable은 날아간다
