# "같은 데이터를 여러 눈으로 보는 법" — Python으로 MVCC 만들기

## 데이터베이스의 근본 문제

두 트랜잭션이 동시에 같은 키를 읽고 쓴다. 하나가 쓰는 도중에 다른 하나가 읽으면 어떻게 될까? 락을 걸면 간단하지만 동시성이 죽는다. MVCC(Multi-Version Concurrency Control)는 **각 트랜잭션에게 데이터의 다른 버전을 보여주는** 방식으로 이 문제를 해결한다.

이 프로젝트는 Python database-internals 트랙의 마지막이다. 01에서 만든 저장소, 02의 WAL, 03의 인덱스, 04의 buffer pool 위에 올라가는 **트랜잭션 관리 계층**을 만든다.

## Version과 Version Chain

모든 것은 Version에서 시작한다:

```python
@dataclass(slots=True)
class Version:
    value: object
    tx_id: int
    deleted: bool
```

하나의 키에 여러 버전이 존재할 수 있다. 이 버전들은 리스트로 연결되어 **version chain**을 형성한다. tx_id가 큰(최신) 버전이 앞에 온다.

### 삽입 정렬로 순서 유지

```python
def append(self, key: str, value: object, tx_id: int, deleted: bool) -> None:
    chain = self.store.setdefault(key, [])
    index = 0
    while index < len(chain) and chain[index].tx_id > tx_id:
        index += 1
    chain.insert(index, Version(value, tx_id, deleted))
```

새 버전을 체인에 삽입할 때 tx_id 내림차순 위치를 찾아 넣는다. 이렇게 하면 가시성 검사에서 앞에서부터 순회하면 자연스럽게 최신 버전부터 확인한다.

Go 버전과 동일한 삽입 정렬 방식이다. 트랜잭션 수가 적은 학습 환경에서는 O(n) 삽입이 충분하다.

## Snapshot Isolation

### begin: 스냅샷 시점 결정

```python
def begin(self) -> int:
    tx_id = self.next_tx_id
    self.next_tx_id += 1
    snapshot = max(self.committed, default=0)
    self.transactions[tx_id] = Transaction(snapshot=snapshot, status="active")
    return tx_id
```

`snapshot = max(self.committed, default=0)` — 가장 최근에 커밋된 트랜잭션의 ID가 스냅샷 경계가 된다. 이 시점 이후에 커밋된 변경은 이 트랜잭션에게 보이지 않는다.

### 가시성 규칙

```python
def get_visible(self, key: str, snapshot: int, committed: dict[int, bool]) -> Version | None:
    for version in self.store.get(key, []):
        if version.tx_id <= snapshot and committed.get(version.tx_id, False):
            return Version(version.value, version.tx_id, version.deleted)
    return None
```

두 가지 조건이 모두 만족해야 보인다:
1. **`version.tx_id <= snapshot`**: 스냅샷 시점 이전에 생성된 버전
2. **`committed.get(version.tx_id, False)`**: 해당 트랜잭션이 실제로 커밋됨

version chain이 tx_id 내림차순이므로, 앞에서부터 순회하다가 첫 번째로 두 조건을 만족하는 버전이 **가장 최신의 가시적 버전**이다.

테스트가 이를 명확히 보여준다:

```python
def test_snapshot_isolation():
    t1 = manager.begin()
    manager.write(t1, "x", 100)
    manager.commit(t1)

    t2 = manager.begin()       # snapshot = t1
    t3 = manager.begin()       # snapshot = t1
    manager.write(t3, "x", 200)
    manager.commit(t3)          # t3 커밋 후에도...
    assert manager.read(t2, "x") == 100  # t2는 여전히 100을 본다
```

t2의 snapshot은 t1이다. t3가 커밋되어도 t3의 tx_id > t2의 snapshot이므로 t2에게는 보이지 않는다.

## Read-Your-Own-Write

스냅샷 이전 버전만 보인다면, 내가 방금 쓴 값도 안 보일까? MVCC에서는 **자신이 쓴 값은 항상 보여야** 한다:

```python
def read(self, tx_id: int, key: str):
    tx = self._active_tx(tx_id)
    if key in tx.write_set:
        for version in self.version_store.store.get(key, []):
            if version.tx_id == tx_id:
                return None if version.deleted else version.value
    version = self.version_store.get_visible(key, tx.snapshot, self.committed)
```

write_set에 키가 있으면 version chain에서 **자신의 tx_id와 일치하는 버전**을 직접 찾는다. 스냅샷 규칙을 우회하는 유일한 경우다.

## Write-Write Conflict: First-Committer-Wins

두 트랜잭션이 같은 키를 수정하면 충돌이다. 하나만 커밋할 수 있다:

```python
def commit(self, tx_id: int) -> None:
    tx = self._active_tx(tx_id)
    for key in tx.write_set:
        for version in self.version_store.store.get(key, []):
            if version.tx_id > tx.snapshot and version.tx_id != tx_id and self.committed.get(version.tx_id, False):
                self._abort_internal(tx_id, tx)
                raise ValueError(f'write-write conflict on key "{key}"')
    tx.status = "committed"
    self.committed[tx_id] = True
```

커밋 시점에 write_set의 모든 키를 확인한다:
- 스냅샷 이후에 생성되었고 (`version.tx_id > tx.snapshot`)
- 자기 자신이 아니고 (`version.tx_id != tx_id`) 
- 이미 커밋된 (`committed.get(version.tx_id, False)`)

버전이 있으면 → **충돌**. 자동으로 abort하고 ValueError를 던진다.

이것이 "first-committer-wins" 정책이다. 먼저 커밋한 쪽이 승리하고, 늦게 커밋하려는 쪽이 롤백된다.

```python
def test_write_write_conflict():
    t1 = manager.begin()
    t2 = manager.begin()
    manager.write(t1, "x", "alpha")
    manager.write(t2, "x", "beta")
    manager.commit(t1)        # t1 먼저 커밋 → 성공
    manager.commit(t2)        # t2 커밋 시도 → ValueError
```

다른 키를 수정하면 충돌이 없다:

```python
def test_different_keys_no_conflict():
    manager.write(t1, "x", 1)
    manager.write(t2, "y", 2)
    manager.commit(t1)  # 성공
    manager.commit(t2)  # 성공 — 다른 키이므로
```

## Abort: 깨끗한 롤백

```python
def _abort_internal(self, tx_id: int, tx: Transaction) -> None:
    for key in tx.write_set:
        self.version_store.remove_by_tx_id(key, tx_id)
    tx.status = "aborted"
```

abort 시 write_set의 모든 키에서 해당 tx_id의 버전을 제거한다. version chain에 흔적을 남기지 않는다. 이것이 MVCC에서 abort가 간단한 이유다 — 커밋 표시만 하지 않으면 다른 트랜잭션에게 보이지 않지만, 버전을 지워야 GC 부담이 줄어든다.

## Delete: 삭제도 버전이다

```python
def delete(self, tx_id: int, key: str) -> None:
    tx = self._active_tx(tx_id)
    self.version_store.append(key, None, tx_id, True)
    tx.write_set.add(key)
```

삭제는 `deleted=True`인 버전을 추가하는 것이다. 물리적 삭제가 아니라 **논리적 삭제(tombstone)**다. 읽기 시 `deleted` 플래그를 확인하여 None을 반환한다.

## Garbage Collection

커밋된 오래된 버전은 계속 쌓인다. GC가 정리해야 한다:

```python
def gc(self) -> None:
    min_snapshot = self.next_tx_id
    for tx in self.transactions.values():
        if tx.status == "active" and tx.snapshot < min_snapshot:
            min_snapshot = tx.snapshot
    self.version_store.gc(min_snapshot)
```

활성 트랜잭션 중 가장 오래된 스냅샷을 찾는다. 이 시점 이전의 버전은 더 이상 아무도 필요하지 않다.

VersionStore의 GC:

```python
def gc(self, min_snapshot: int) -> None:
    for key, chain in list(self.store.items()):
        recent = [v for v in chain if v.tx_id >= min_snapshot]
        old = [v for v in chain if v.tx_id < min_snapshot]
        if old:
            recent.append(old[0])  # 가장 최신 old 버전 하나만 유지
```

`min_snapshot` 이전의 버전 중 **가장 최신 하나만** 남긴다. 이 버전이 있어야 `min_snapshot` 시점의 읽기가 여전히 동작한다.

## Go 버전과의 비교

| 항목 | Go 08-mvcc | Python 05-mvcc |
|------|-----------|----------------|
| version chain | `[]Version` 삽입 정렬 | `list[Version]` 삽입 정렬 |
| conflict 검사 | first-committer-wins | first-committer-wins |
| GC 전략 | 동일 (oldest active snapshot) | 동일 |
| write_set | `map[string]struct{}` | `set[str]` |
| 외부 의존성 | 없음 | 없음 |
| 코드량 | ~200줄 | ~120줄 |
| 테스트 수 | 7개 | 7개 |

동일한 설계를 거의 그대로 Python으로 옮겼다. 핵심 알고리즘은 같고, 언어 관용구만 다르다.

## 마무리

MVCC는 "읽기는 쓰기를 차단하지 않는다"는 원칙의 구현이다. 각 트랜잭션은 자신의 스냅샷 시점을 기준으로 데이터를 보고, 쓰기 충돌만 커밋 시점에 검사한다. first-committer-wins 정책은 단순하지만 대부분의 워크로드에서 충분하다.

소스코드에서 드러나지 않는 핵심 통찰: **version chain의 정렬 순서가 모든 것을 결정한다.** tx_id 내림차순으로 유지하면 가시성 검사가 "앞에서부터 찾아서 처음 만족하는 것을 반환"하는 단순한 순회가 된다. 정렬 불변식 하나가 읽기, 쓰기, GC 모든 연산의 복잡도를 결정한다.
