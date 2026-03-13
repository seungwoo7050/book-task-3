# 20 get의 조회 순서가 전부였다

## Day 1
### Session 2

`store.py`를 위에서부터 읽기 시작했다. `put`과 `delete`는 별로 놀랄 게 없었다. `put`은 memtable dict에 넣고, `delete`는 `None`을 넣는다. 그런데 `get`에서 멈췄다.

```python
def get(self, key: str) -> tuple[str | None, bool]:
    if key in self.memtable:
        return self.memtable[key], True
    if self.immutable_memtable is not None and key in self.immutable_memtable:
        return self.immutable_memtable[key], True
    for table in self.sstables:
        value, found = table.get(key)
        if found:
            return value, True
    return None, False
```

이 함수가 이 프로젝트의 전부였다. memtable → immutable → SSTable 순서로 훑고, 처음 찾은 결과를 그대로 돌려준다. 이때까지는 "당연히 최신 값을 먼저 찾겠지"라고 가볍게 넘기고 있었다.

그런데 `test_tombstone_across_levels`를 읽다가 의문이 생겼다.

```bash
grep -A 8 "def test_tombstone_across_levels" tests/test_mini_lsm_store.py
```

```text
def test_tombstone_across_levels(tmp_path):
    store = open_store(tmp_path, 1024)
    store.put("key", "value")
    store.force_flush()
    store.delete("key")
    value, found = store.get("key")
    assert found is True
    assert value is None
```

`delete` 후에도 `found`가 `True`다. 삭제했는데 "찾았다"를 반환한다? 당시에는 이게 버그인 줄 알았다. 그런데 `get`의 구조를 다시 보니 이유가 보였다. memtable에 `key: None`이 들어가 있으니, `key in self.memtable`이 참이고 `(None, True)`를 반환한다. SSTable에 남아 있는 옛날 `"value"`까지는 절대 내려가지 않는다.

이게 tombstone이다. 삭제를 별도 연산으로 만들지 않고 `None`이라는 값으로 표현한다. 그래서 "키는 존재하지만 값은 없다"가 된다. 이전 계층의 값이 되살아나는 것을 막는 장치였다.

### Session 3

`force_flush()`는 처음 읽었을 때 예상보다 단순했는데, 한 가지 순서가 눈에 걸렸다.

```python
def force_flush(self) -> None:
    if not self.memtable:
        return
    self.immutable_memtable = dict(self.memtable)
    self.memtable.clear()
    self._byte_size = 0
    records = sorted(self.immutable_memtable.items())
    table = SSTable(SSTable.file_name(self.data_dir, self._next_sequence))
    self._next_sequence += 1
    table.write(records)
    self.sstables.insert(0, table)
    self.immutable_memtable = None
```

`self.sstables.insert(0, table)` — 리스트 맨 앞에 넣는다. 그래서 `get`에서 `for table in self.sstables`로 돌 때 가장 최근에 flush된 테이블이 먼저 나온다. newest-first가 `insert(0, ...)`으로 보장되는 거다.

처음엔 "왜 append가 아니라 insert(0)이지?" 하고 지나쳤는데, `test_memtable_wins_over_sstable`과 연결하니 이게 핵심이었다. memtable에도 해당 키가 없고 immutable에도 없으면, SSTable 중에서도 가장 최근 것부터 뒤져야 올바른 최신 값이 나온다.

이 시점에서 새로 떠오른 의문: `open()`으로 다시 열 때도 이 순서가 유지될까?
