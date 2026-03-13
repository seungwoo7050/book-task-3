# 10 파일 하나짜리 저장 엔진을 처음 열었을 때

## Day 1
### Session 1

`find src -type f`를 쳤을 때 나온 파일이 세 개였다. `__init__.py`, `__main__.py`, 그리고 `store.py`. 이게 전부다.

```bash
cd python/database-internals/projects/01-mini-lsm-store
find src tests -type f | sort
```

```text
src/mini_lsm_store/__init__.py
src/mini_lsm_store/__main__.py
src/mini_lsm_store/store.py
tests/test_mini_lsm_store.py
```

README에는 "최소 LSM 저장 엔진"이라고 적혀 있는데, 한 파일 안에 `SSTable`과 `MiniLSMStore`가 같이 들어 있다. 이 시점에서는 솔직히 이게 저장 엔진 흐름을 보여주기엔 너무 작아 보였다. LSM이라면 최소한 WAL도 있어야 하고, compaction도 있어야 하지 않나.

- 목표: 이게 진짜 저장 엔진 학습 슬롯인지, 아니면 dict wrapper인지 판단한다
- 진행: README → problem/README → 테스트 이름 순서로 훑었다

테스트 이름을 보니 생각이 바뀌기 시작했다.

```bash
grep -n "def test_" tests/test_mini_lsm_store.py
```

```text
4:def test_put_and_get(tmp_path):
9:def test_missing_key(tmp_path):
14:def test_update(tmp_path):
19:def test_delete(tmp_path):
26:def test_flush_creates_sstable(tmp_path):
32:def test_read_after_force_flush(tmp_path):
39:def test_memtable_wins_over_sstable(tmp_path):
46:def test_tombstone_across_levels(tmp_path):
53:def test_persistence_after_reopen(tmp_path):
```

`test_memtable_wins_over_sstable`, `test_tombstone_across_levels`, `test_persistence_after_reopen` — 이 이름들은 dict wrapper라면 나올 수 없는 테스트다. "계층 사이의 우선순위"를 검증하고 있다.

이 시점에서 가설을 수정했다. 이 프로젝트는 자료구조를 깊이 파는 게 아니라, `memtable → immutable → SSTable`이라는 계층 전환 흐름을 한 화면 안에서 통째로 보여주려는 구성이다.

```python
@dataclass(slots=True)
class SSTable:
    path: Path
    index: dict[str, str | None] | None = None
```

`SSTable`이 이렇게 작은 이유가 여기 있었다. 독립 모듈로 분리하면 구현은 깔끔해지지만, "flush가 memtable을 SSTable로 바꾸는 순간"을 한 곳에서 따라갈 수 없게 된다. 의도적으로 한 파일에 넣은 거다.

이 시점에서 아직 모르는 것:
- `force_flush()`가 어떤 순서로 memtable을 떼어내는지
- `get()`이 여러 SSTable을 어떤 순서로 훑는지
- 삭제가 `None`으로만 표현되는데 이전 계층의 값이 다시 올라오진 않는지
